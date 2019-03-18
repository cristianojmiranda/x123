import os, pika, json
import utils

MQ_HOST = utils.env("MQ_HOST", "localhost")
MQ_PORT = utils.env("MQ_PORT", 5672)
MQ_USER = utils.env("MQ_USER", "guest")
MQ_PASS = utils.env("MQ_PASS", "guest")

credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
connection_params =pika.ConnectionParameters(MQ_HOST, MQ_PORT, '/', credentials)

def get_connection():
	return pika.BlockingConnection(connection_params)

connection = get_connection()
channel = connection.channel()

# exchange
channel.exchange_declare(exchange='seeder', exchange_type='direct')

# queues
#channel.queue_declare(queue='seeder-split', durable=True)
#channel.queue_declare(queue='seeder-transform', durable=True)
channel.queue_declare(queue='seed', durable=True)

#channel.queue_declare(queue='seeder-split-retry', durable=True)
#channel.queue_declare(queue='seeder-transform-retry', durable=True)
channel.queue_declare(queue='seed-retry', durable=True)

#channel.queue_declare(queue='seeder-split-dl', durable=True)
#channel.queue_declare(queue='seeder-transform-dl', durable=True)
channel.queue_declare(queue='seed-dl', durable=True)

# binds
#channel.queue_bind(exchange='seeder', queue="seeder-split", routing_key="split")
#channel.queue_bind(exchange='seeder', queue="seeder-transform", routing_key="transform")
channel.queue_bind(exchange='seeder', queue="seed", routing_key="seed")
connection.close()

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
