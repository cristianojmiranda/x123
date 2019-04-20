import logging, json
import utils, rabbitmq, island

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# rabbit config
exchange = utils.env('EXCHANGE', 'octopus')
queue_name = utils.env('QUEUE', 'island_file_gen')
routing_key = utils.env('INPUT_RK', 'file_generate')

rabbit_conn = rabbitmq.get_connection()
rabbitmq.create_exchange(exchange, rabbit_conn);
rabbitmq.create_queue(queue_name, exchange, routing_key, rabbit_conn)

def file_generate_callback(ch, method, properties, body):
	logger.info("Generating file [%s]" % body)
	p_body = json.loads(body)
	map_gen_id = p_body['map_gen_id']
	file_map_id = p_body['file_map_id']

	try:
		gen_id = island.generate_file(map_gen_id, file_map_id)
		logger.info("map_gen_file_id: %s", gen_id)
	except Exception as e:
		logger.error(e)
		rabbitmq.send_to_retry("Failed", properties)

rabbitmq.consumer(queue_name, file_generate_callback, rabbit_conn)
