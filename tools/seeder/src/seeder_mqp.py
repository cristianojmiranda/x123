import api_client
import consul, vault
from rabbitmq import channel

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	if body['storage'] == 'consul':
		consul.put(body['name'], body['data'])
		api_client.delete_file(body['id'])
	elif body['storage'] == 'vault':
		vault.put(body['name'], body['data'])
		api_client.delete_file(body['id'])
	else:
		print('Invalid storage')

channel.basic_consume(callback, queue='seed')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
