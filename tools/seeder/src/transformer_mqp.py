import json, yaml, rabbitmq, utils
SPRING_PROFILE=utils.env("SPRING_PROFILE", "")

conn = rabbitmq.get_connection()
channel = conn.channel()

queue_name='seeder-transform'
rabbitmq.create_exchange("seeder", conn);
rabbitmq.create_queue(queue_name, 'seeder', 'transform', conn)

'''
Parse data by type
'''
def parse(data, data_type='yaml'):
	#data = message['data']
	#data = utils.decode(data)
	if data_type == 'yaml':
		return yaml.load(data, Loader=yaml.CLoader)

	elif data_type == 'json':
		return json.loads(data)

	return data

def is_spring_valid_profile(data):
	has_profile = utils.has_key('spring.profiles', data)
	return has_profile is False or (has_profile and data['spring']['profiles'] == SPRING_PROFILE)

'''
Filter the message and return parsed data
'''
def filter(message):
	# data parse
	data = parse(message['data'], message['type'])
	return data if is_spring_valid_profile(data) else None

def transform(message, data):
	print("Transforming: message=", message, ",data=", data)

	t_data = data
	data_type = message['type']
	if data_type == 'yaml':
		t_data = yaml.dump(data)

	elif data_type == 'json':
		t_data = json.dumps(data)

	message['app'] = message['name']
	message['data'] = t_data

	if utils.has_key('spring.profiles', data):
		spring_profile = data['spring']['profiles']
		message['name'] = "%s-%s" % (message['name'], spring_profile)

	return message

def send_to_seed(message):
	s_message = {
				 	'key': message['name'],
				 	'value': message['data'],
				 	'storage': message['storage'],
				 	'app': message['app']
				}
	rabbitmq.publish('seeder', 'seed', s_message, conn)

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	s_body = body.decode("UTF-8")
	message = json.loads(s_body)

	data = filter(message)
	if data is None:
		print("Message discarted by filter")
	else:
		t_message = transform(message, data)
		send_to_seed(t_message)

	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name, no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
