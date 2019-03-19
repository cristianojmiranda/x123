import json
import consul_client, vault_client
import rabbitmq, utils

conn = rabbitmq.get_connection()
channel = conn.channel()

exchange = 'seeder'
queue_name = 'seed'

rabbitmq.create_exchange(exchange, conn);
rabbitmq.create_queue(queue_name, exchange, 'seed', conn)
rabbitmq.create_queue('restart-app', exchange, 'seeded', conn)

def notify_seed_app(app):
	rabbitmq.publish(exchange, 'seeded', {'app': app}, conn)

def seed(ch, method, message):

	key = message['key']
	#key = utils.decode(message['key'])
	value = message['value']
	storage = message['storage']
	app = message['app']

	if storage == 'consul':
		consul_client.put(key, value)
		notify_seed_app(app)
		ch.basic_ack(delivery_tag = method.delivery_tag)

	elif storage == 'vault':
		vault_client.put(app, key, value)
		notify_seed_app(app)
		ch.basic_ack(delivery_tag = method.delivery_tag)

	else:
		print("Invalid storage type '%s'" % storage)
		ch.basic_nack(delivery_tag = method.delivery_tag, requeue=True)

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	p_body = json.loads(body.decode("UTF-8"))
	seed(ch, method, p_body)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name, no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
