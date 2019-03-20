import rabbitmq, utils
import json, yaml, logging

SPRING_PROFILE=utils.env("SPRING_PROFILE", "")

# json with prefix/sufix by flavor
PREFIX_BAG = utils.env("PREFIX_BAG", '''{ "spring": { "prefix": "spring/", "sufix": "/data"} }''')
_prefix_bag = json.loads(PREFIX_BAG)
logging.debug("prefix_bag=%s" % str(_prefix_bag))

exchange = "seeder"
queue_name = "seeder-transform"

conn = rabbitmq.get_connection()
rabbitmq.create_exchange("seeder", conn);
rabbitmq.create_queue(queue_name, exchange, 'transform', conn)

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
	logging.info("Transforming: message=[%s] data=[%s]" % (message, data))

	t_data = data
	data_type = message['type']
	if data_type == 'yaml':
		t_data = yaml.dump(data)

	elif data_type == 'json':
		t_data = json.dumps(data)

	message['app'] = message['name']
	message['data'] = t_data

	# flavor spring?
	if utils.has_key('spring.profiles', data):
		spring_profile = utils.get_key('spring.profiles', data)
		message['name'] = "%s-%s" % (message['name'], spring_profile)

	return message

def compose_key(key, flavor):
	if flavor in _prefix_bag:
		pre = _prefix_bag[flavor]['prefix']
		suf = _prefix_bag[flavor]['sufix']
		return "%s%s%s" % (pre, key, suf)
	return key

def send_to_seed(message):
	s_message = {
				 	'key': compose_key(message['name'], message['flavor']),
				 	'value': message['data'],
				 	'storage': message['storage'],
				 	'app': message['app']
				}
	rabbitmq.publish(exchange, 'seed', s_message, conn)

def callback(ch, method, properties, body):
	message = json.loads(body)
	data = filter(message)
	if data is None:
		logging.warn("Message discarted by filter")
	else:
		t_message = transform(message, data)
		send_to_seed(t_message)

rabbitmq.consumer(queue_name, callback, conn)
