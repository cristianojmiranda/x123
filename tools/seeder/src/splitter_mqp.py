print("seeder-splitter-mqp")
import json
#import logging
import api_client, rabbitmq
#from rabbitmq import get_connection, publish


conn = rabbitmq.get_connection()
channel = conn.channel()
channel.basic_qos(prefetch_count=1)

queue_name = 'seeder-split'
rabbitmq.create_queue(queue_name, 'seeder', 'split', conn)

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	jm = json.loads(body.decode("utf-8"))
	raw_data = api_client.get_file(jm['id']).text

	chunkies = raw_data.split('---')
	for data in chunkies:
		message = dict(jm)
		message['data'] = data
		rabbitmq.publish('seeder', 'transform', message, conn)

	print("=")
	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback, queue=queue_name, no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
