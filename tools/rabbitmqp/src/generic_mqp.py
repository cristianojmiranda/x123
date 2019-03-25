import rabbitmq, utils
import json, logging, requests

# load configs
exchange = utils.env('EXCHANGE', 'rabbitmqp')
output_exchange = utils.env('OUTPUT_EXCHANGE')

queue = utils.env('QUEUE', 'my-queue')
input_rk = utils.env('INPUT_RK', 'input')
output_rk = utils.env('OUTPUT_RK')
post_url = utils.env('POST_URL')

# get rabbit connection
conn = rabbitmq.get_connection()

# create exchanges
rabbitmq.create_exchange(exchange, conn)
if output_exchange and output_exchange != exchange:
	rabbitmq.create_exchange(output_exchange, conn)

# create queue's and bind's
rabbitmq.create_queue(queue, exchange, input_rk, conn)

# message consumer callback
def callback(ch, method, properties, body):

	# call backend
	if post_url is not None:
		logging.info("Posting message to url %s" % post_url)

		resp = requests.post(post_url, data=body)
		if resp.status_code not in [200, 201, 202, 204]:
			exception = "Failed to post message [%s]. Reason: %i %s" % (body, resp.status_code, resp.text)
			if resp.status_code < 500:
				# retry workflow: retry => long_retry => dead_letter
				rabbitmq.send_to_retry(exception, properties)
			else:
				# raise to go to dead letter
				raise Exception(exception)

		logging.info("Message posted! %i %s" % (resp.status_code, resp.text))

	# fowarding the message
	if output_rk is not None:
		_exchange = output_exchange if output_exchange else exchange
		rabbitmq.publish(_exchange, output_rk, body, conn)

# start rabbit consumer
rabbitmq.consumer(queue, callback, conn)
