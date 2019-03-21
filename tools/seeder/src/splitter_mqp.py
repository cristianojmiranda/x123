import logging, json
import utils, api_client, rabbitmq

exchange = utils.env('EXCHANGE', 'seeder')
queue_name = utils.env('QUEUE', 'seeder-split')
input_routing_key = utils.env('INPUT_RK', 'split')
output_routing_key = utils.env('OUTPUT_RK', 'transform')

conn = rabbitmq.get_connection()
rabbitmq.create_exchange(exchange, conn);
rabbitmq.create_queue(queue_name, exchange, input_routing_key, conn)

def callback(ch, method, properties, body):

	p_body = json.loads(body)
	id = p_body['id']
	type = p_body['type']
	message = dict(p_body)

	# get file by id
	resp = api_client.get_file(id)
	if resp.status_code != 200:
		error_msg = "Failed to get file %s. [HTTP_STATUS=%i] - %s" % (id, resp.status_code, resp.text)
		rabbitmq.send_to_retry(error_msg, properties)

	raw_data = resp.text
	logging.info("raw_file=[%s]" % raw_data)

	if type == 'yaml':
		for data in raw_data.split('---'):
			message['data'] = data
			rabbitmq.publish(exchange, output_routing_key, message, conn)

	elif type == 'json':

		j_body = json.loads(raw_data)
		if utils.has_key('seeder.splitter-key', j_body):
			s_key = utils.get_key('seeder.splitter-key', j_body)
			for data in j_body[s_key]:
				message['data'] = data
				rabbitmq.publish(exchange, output_routing_key, message, conn)

		else:
			message['data'] = raw_data
			rabbitmq.publish(exchange, output_routing_key, message, conn)

	else:
		message['data'] = raw_data
		rabbitmq.publish(exchange, output_routing_key, message, conn)


	api_client.delete_file(id)

rabbitmq.consumer(queue_name, callback, conn)
