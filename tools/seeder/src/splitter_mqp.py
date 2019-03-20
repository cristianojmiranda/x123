import utils, json, api_client, rabbitmq

queue_name = 'seeder-split'

conn = rabbitmq.get_connection()
rabbitmq.create_exchange("seeder", conn);
rabbitmq.create_queue(queue_name, 'seeder', 'split', conn)

def callback(ch, method, properties, body):

	try:
		p_body = json.loads(body)
		resp = api_client.get_file(p_body['id'])

		if resp.status_code == 200:
			print("Failed to get file %i" % resp.status_code)
			#ch.basic_nack(delivery_tag = method.delivery_tag, requeue=True)
			rabbitmq.publish('seeder', 'seeder-split-retry', body, conn)
			ch.basic_ack(delivery_tag = method.delivery_tag)
			return

		raw_data = resp.text
		print("raw_file=[%s]" % raw_data)
		for data in raw_data.split('---'):
			message = dict(p_body)
			#message['data'] = utils.encode(data)
			message['data'] = data
			rabbitmq.publish('seeder', 'transform', message, conn)

		api_client.delete_file(p_body['id'])
		ch.basic_ack(delivery_tag = method.delivery_tag)
	except Exception as e:
		print("Failed", e)
		rabbitmq.publish('seeder', 'split-dl', body, conn)
		#ch.basic_nack(delivery_tag = method.delivery_tag, requeue=True)

rabbitmq.consumer(queue_name, callback, conn)
