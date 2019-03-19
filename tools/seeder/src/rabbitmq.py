import os, pika, json
import utils

MQ_HOST = utils.env("MQ_HOST", "localhost")
MQ_PORT = int(utils.env("MQ_PORT", 5672))
MQ_USER = utils.env("MQ_USER", "guest")
MQ_PASS = utils.env("MQ_PASS", "guest")
MQ_VHOST = utils.env("MQ_VHOST", "/")

credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
connection_params =pika.ConnectionParameters(MQ_HOST, MQ_PORT, MQ_VHOST, credentials)

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
	channel.queue_declare(queue=name, durable=True)
	channel.queue_declare(queue="%s-retry" % name, durable=True)
	channel.queue_declare(queue="%s-dl" % name, durable=True)
	channel.queue_bind(exchange=exchange, queue=name, routing_key=routing_key)

def publish(exchange, routing, message, conn=None):
	print("publish [%s] to '%s' exchange with routing '%s'" % (str(message), exchange, routing))
	channel = get_channel(conn)
	channel.basic_publish(exchange=exchange, routing_key=routing, body=json.dumps(message))
	print("published")
