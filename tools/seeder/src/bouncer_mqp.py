import json, logging
import rabbitmq,  api_client

exchange = 'seeder'
queue_name = 'restart-app'

conn = rabbitmq.get_connection()
rabbitmq.create_exchange(exchange, conn);
rabbitmq.create_queue(queue_name, exchange, 'seeded', conn)

def callback(ch, method, properties, body):
	p_body = json.loads(body)
	api_client.k8s_bounce_app(p_body['app'])

rabbitmq.consumer(queue_name, callback, conn)
