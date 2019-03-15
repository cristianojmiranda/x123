import api_client
from rabbitmq import connection, publish

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	raw_data = api_client.get_file(body['id'])
	chunkies = raw_data.split('---')
	for data in chunkies:
		message = dict(body)
		message['data'] = data
		publish('seeder-exchange', 'seeder-transform', message)

channel = connection.channel()
channel.basic_consume(callback, queue='seeder-split')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
