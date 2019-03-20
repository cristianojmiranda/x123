import os, pika, json
import utils

MQ_HOST = utils.env("MQ_HOST", "localhost")
MQ_PORT = int(utils.env("MQ_PORT", 5672))
MQ_USER = utils.env("MQ_USER", "guest")
MQ_PASS = utils.env("MQ_PASS", "guest")
MQ_VHOST = utils.env("MQ_VHOST", "/")

MQ_TTL_RETRY = int(utils.env("MQ_TTL_RETRY", 60000))
MQ_MAX_RETRIES = int(utils.env("MQ_MAX_RETRIES", 10))
MQ_PRE_FETCH = int(utils.env("MQ_PRE_FETCH", 1))

credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
connection_params =pika.ConnectionParameters(MQ_HOST, MQ_PORT, MQ_VHOST, credentials)

class RetryException(Exception):
	pass

def get_connection():
	return pika.BlockingConnection(connection_params)

def get_channel(conn=None):
	if conn is None:
		conn = get_connection()
	return conn.channel()

def create_exchange(name, conn=None):
	channel = get_channel(conn)
	channel.exchange_declare(exchange=name, exchange_type='direct')

def create_queue(name, exchange, routing_key, conn=None):
	channel = get_channel(conn)

	# queues
	channel.queue_declare(queue=name, durable=True)
	channel.queue_declare(queue="%s-dl" % name, durable=True)

	# retry queue
	retry_args = { "x-message-ttl": MQ_TTL_RETRY, "x-dead-letter-exchange": exchange, "x-dead-letter-routing-key": routing_key }
	channel.queue_declare(queue="%s-retry" % name, durable=True, arguments=retry_args)

	# bind's
	channel.queue_bind(exchange=exchange, queue=name, routing_key=routing_key)
	channel.queue_bind(exchange=exchange, queue="%s-retry" % name, routing_key="%s-retry" % name)
	channel.queue_bind(exchange=exchange, queue="%s-dl" % name, routing_key="%s-dl" % name)

def publish(exchange, routing, message, conn=None):
	print("publish [%s] to '%s' exchange with routing '%s'" % (str(message), exchange, routing))
	channel = get_channel(conn)
	_body = json.dumps(message) if type(message) is dict else message
	channel.basic_publish(exchange=exchange, routing_key=routing, body=_body)
	print("published")

def consumer(queue, callback, conn=None):

	def _callback(ch, method, properties, body):
		print(" [x] Received {%r} at '%s'" % (body, queue))
		s_body = body.decode("UTF-8")
		try:
			if callback:
				callback(ch, method, properties, s_body)
		except RetryException as r:
			print("Failed with retry", e)
			publish("", "%s-retry" % queue, s_body, conn)
		except Exception as e:
			print("Failed moving to dead-leatter", e)
			publish("", "%s-dl" % queue, s_body, conn)

		ch.basic_ack(delivery_tag = method.delivery_tag)

 	channel = get_channel(conn)
	channel.basic_qos(prefetch_count=MQ_PRE_FETCH)
	channel.basic_consume(_callback, queue=queue, no_ack=False)

	print(" [*] Waiting for messages, queue '%s'. To exit press CTRL+C" % queue)
	channel.start_consuming()
