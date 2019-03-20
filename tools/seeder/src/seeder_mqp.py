import json, logging
import rabbitmq, utils
import consul_client, vault_client

exchange = 'seeder'
queue_name = 'seed'

conn = rabbitmq.get_connection()
rabbitmq.create_exchange(exchange, conn);
rabbitmq.create_queue(queue_name, exchange, 'seed', conn)

def notify_seed_app(app):
	rabbitmq.publish(exchange, 'seeded', {'app': app}, conn)

def seed(message):

	key = message['key']
	value = message['value']
	storage = message['storage']
	app = message['app']

	if storage == 'consul':
		consul_client.put(key, value)
		notify_seed_app(app)

	elif storage == 'vault':
		vault_client.put(key, value)
		notify_seed_app(app)

	else:
		raise Exception("Invalid storage type '%s'" % storage)

def callback(ch, method, properties, body):
	p_body = json.loads(body)
	seed(p_body)

rabbitmq.consumer(queue_name, callback, conn)
