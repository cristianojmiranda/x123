import utils, json, api_client, rabbitmq

conn = rabbitmq.get_connection()
channel = conn.channel()

queue_name = 'seeder-split'
rabbitmq.create_exchange("seeder", conn);
rabbitmq.create_queue(queue_name, 'seeder', 'split', conn)

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	s_body = body.decode("UTF-8")
	p_body = json.loads(s_body)
	raw_data = api_client.get_file(p_body['id']).text
	print("raw_file=[%s]" % raw_data)
	for data in raw_data.split('---'):
		message = dict(p_body)
		#message['data'] = utils.encode(data)
		message['data'] = data
		rabbitmq.publish('seeder', 'transform', message, conn)

	api_client.delete_file(p_body['id'])
	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name, no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
