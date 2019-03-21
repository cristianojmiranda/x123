import rabbitmq, utils
import json, yaml, logging

SPRING_PROFILE=utils.env("SPRING_PROFILE", "")

# json with prefix/sufix by flavor
PREFIX_BAG = utils.env("PREFIX_BAG", '''{ "spring": { "prefix": "spring/", "sufix": "/data"} }''')
_prefix_bag = json.loads(PREFIX_BAG)
logging.info("prefix_bag=%s" % str(_prefix_bag))

# json with output format by storage (you can have a .yaml that seed consul as json)
STORAGE_OUTPUT = utils.env("STORAGE_OUTPUT", '''{ "consul": "yaml", "vault": "json" }''')
_storage_output = json.loads(STORAGE_OUTPUT)
logging.info("storage_outputs=%s", str(_storage_output))

exchange = utils.env('EXCHANGE', 'seeder')
queue_name = utils.env('QUEUE', 'seeder-transform')
input_routing_key = utils.env('INPUT_RK', 'transform')
output_routing_key = utils.env('OUTPUT_RK', 'seed')

conn = rabbitmq.get_connection()
rabbitmq.create_exchange(exchange, conn);
rabbitmq.create_queue(queue_name, exchange, input_routing_key, conn)

def load_custom_transformer():
	tb, ta = None, None

	try:
		from transformer import transform_before_parse as tb
	except Exception as e:
		logging.error("Not found transform_before_parse", e)

	try:
		from transformer import transform_after_parse as ta
	except Exception as e:
		logging.error("Not found transform_after_parse", e)

	return (tb, ta)

# load customizer
t_before_parse, t_after_parse = load_custom_transformer()

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

def output_type(type, storage):
	if storage in _storage_output:
		return _storage_output[storage]
	return type

def transform(message, data):
	logging.info("Transforming: message=[%s] data=[%s]" % (message, data))

	t_data = data
	storage = message['storage']
	data_type = message['type']

	out_type = output_type(data_type, storage)
	logging.info("output type: %s" % out_type)

	if out_type == 'yaml':
		t_data = yaml.dump(data)

	elif out_type == 'json':
		t_data = json.dumps(data)

	message['app'] = message['name']
	message['data'] = t_data

	# flavor spring?
	if utils.has_key('spring.profiles', data):
		spring_profile = utils.get_key('spring.profiles', data)
		n_pattern = "%s/%s" if storage == 'vault' else "%s-%s"
		message['name'] = n_pattern % (message['name'], spring_profile)

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
	rabbitmq.publish(exchange, output_routing_key, s_message, conn)

def callback(ch, method, properties, body):

	# parse to json
	message = json.loads(body)

	# custom transformer (before parse)
	if 'data' in message and t_before_parse:
		data = t_before_parse(message['data'])
		logging.info("[custom transformer] [%s] => [%s]", message['data'], data)
		message['data'] = data

	# parse and filter
	data = filter(message)

	if data is None:
		logging.warning("Message discarted by filter")
	else:

		# custom transformer (after parse)
		if t_after_parse:
			_data = t_after_parse(data)
			logging.info("[custom transformer] [%s] => [%s]", str(data), str(_data))
			data = _data

		t_message = transform(message, data)
		send_to_seed(t_message)

rabbitmq.consumer(queue_name, callback, conn)
