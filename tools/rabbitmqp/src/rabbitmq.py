import os, pika, json
import utils, logging

MQ_HOST = utils.env("MQ_HOST", "localhost")
MQ_PORT = int(utils.env("MQ_PORT", 5672))
MQ_USER = utils.env("MQ_USER", "guest")
MQ_PASS = utils.env("MQ_PASS", "guest")
MQ_VHOST = utils.env("MQ_VHOST", "/")

MQ_TTL_RETRY = int(utils.env("MQ_TTL_RETRY", 30000)) # 30s
MQ_TTL_LONG_RETRY = int(utils.env("MQ_TTL_LONG_RETRY", 10 * MQ_TTL_RETRY)) # 10x30s = 300s = 5min
MQ_MAX_RETRIES = int(utils.env("MQ_MAX_RETRIES", 10)) # 5min retries
MQ_MAX_LONG_RETRIES = int(utils.env("MQ_MAX_LONG_RETRIES", 10)) # + 50min long retries
MQ_PRE_FETCH = int(utils.env("MQ_PRE_FETCH", 1))

credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
connection_params =pika.ConnectionParameters(MQ_HOST, MQ_PORT, MQ_VHOST, credentials)

class RetryException(Exception):
	pass

class LongRetryException(Exception):
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

	# long retry queue
	retry_args = { "x-message-ttl": MQ_TTL_LONG_RETRY, "x-dead-letter-exchange": exchange, "x-dead-letter-routing-key": routing_key }
	channel.queue_declare(queue="%s-long-retry" % name, durable=True, arguments=retry_args)

	# bind's
	channel.queue_bind(exchange=exchange, queue=name, routing_key=routing_key)
	channel.queue_bind(exchange=exchange, queue="%s-retry" % name, routing_key="%s-retry" % name)
	channel.queue_bind(exchange=exchange, queue="%s-dl" % name, routing_key="%s-dl" % name)

def publish(exchange, routing, message, conn=None, headers=None):
	logging.info("publishing [%s] to '%s' exchange with routing '%s'" % (str(message), exchange, routing))
	channel = get_channel(conn)
	_body = json.dumps(message) if type(message) is dict else message
	props=pika.spec.BasicProperties(headers=headers)
	channel.basic_publish(exchange=exchange, routing_key=routing, body=_body, properties=props)
	logging.info("published")

def send_to_retry(exception, properties=None):
	if properties and properties.headers and 'long_retry_count' in properties.headers:
		raise LongRetryException(exception)
	raise RetryException(exception)

def consumer(queue, callback, conn=None):

	def _callback(ch, method, properties, body):
		logging.info(" [x] Received %r. Queue %s" % (body, queue))
		s_body = body.decode("UTF-8")

		try:

			if callback:
				callback(ch, method, properties, s_body)

		except RetryException as r:
			logging.error(r)
			retry_count = 1
			if properties.headers and 'retry_count' in properties.headers:
				retry_count = int(properties.headers['retry_count']) + 1

			if retry_count >= MQ_MAX_RETRIES:
				logging.warning("Exceeded retries!!! %i" % retry_count)
				publish("", "%s-long-retry" % queue, s_body, conn, {'long_retry_count': 1})
			else:
				publish("", "%s-retry" % queue, s_body, conn, {'retry_count': retry_count})

		except LongRetryException as lr:
			logging.error(lr)
			retry_count = 1
			if properties.headers and 'long_retry_count' in properties.headers:
				retry_count = int(properties.headers['long_retry_count']) + 1

			if retry_count >= MQ_MAX_LONG_RETRIES:
				logging.warning("Exceeded loooong retries!!! %i" % retry_count)
				publish("", "%s-dl" % queue, s_body, conn)
			else:
				publish("", "%s-long-retry" % queue, s_body, conn, {'long_retry_count': retry_count})

		except Exception as e:
			logging.error("Failed moving to dead-leatter", e)
			publish("", "%s-dl" % queue, s_body, conn)

		ch.basic_ack(delivery_tag = method.delivery_tag)

	channel = get_channel(conn)
	channel.basic_qos(prefetch_count=MQ_PRE_FETCH)
	channel.basic_consume(_callback, queue=queue, no_ack=False)

	logging.info(" [*] Waiting for messages, queue '%s'. To exit press CTRL+C" % queue)
	channel.start_consuming()
