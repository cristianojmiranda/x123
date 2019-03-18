import json
import api_client
import consul, vault
from rabbitmq import get_connection

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	jm = json.loads(body.decode("utf-8"))

	if jm['storage'] == 'consul':
		consul.put(jm['name'], jm['data'])
		api_client.delete_file(jm['id'])
		ch.basic_ack(delivery_tag = method.delivery_tag)
	elif jm['storage'] == 'vault':
		vault.put(jm['name'], jm['data'])
		api_client.delete_file(jm['id'])
		ch.basic_ack(delivery_tag = method.delivery_tag)
	else:
		print('Invalid storage')

channel = get_connection().channel()
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='seed', no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
