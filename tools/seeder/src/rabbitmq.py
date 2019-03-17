import os, pika

MQ_HOST="localhost"
if "MQ_HOST" in os.environ:
	MQ_HOST = os.environ["MQ_HOST"]

def get_connection():
	return pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))

connection = get_connection()
channel = connection.channel()

# exchange
channel.exchange_declare(exchange='seeder', exchange_type='topic')

# queues
channel.queue_declare(queue='seeder-split', durable=True)
channel.queue_declare(queue='seeder-transform', durable=True)
channel.queue_declare(queue='seed', durable=True)

channel.queue_declare(queue='seeder-split-retry', durable=True)
channel.queue_declare(queue='seeder-transform-retry', durable=True)
channel.queue_declare(queue='seed-retry', durable=True)

channel.queue_declare(queue='seeder-split-dl', durable=True)
channel.queue_declare(queue='seeder-transform-dl', durable=True)
channel.queue_declare(queue='seed-dl', durable=True)

# binds
channel.queue_bind(exchange='seeder', queue="seeder-split", routing_key="split")
channel.queue_bind(exchange='seeder', queue="seeder-transform", routing_key="transform")
channel.queue_bind(exchange='seeder', queue="seed", routing_key="seed")

def publish(exchange, routing, message):
	channel = get_connection().channel()
	channel.basic_publish(exchange=exchange, routing_key=routing, body=str(message))
