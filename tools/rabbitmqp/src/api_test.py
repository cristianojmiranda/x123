import rabbitmq
from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from sanic.response import text

app = Sanic()

@app.route("/log", methods=['POST'])
async def log(request):
	logger.info("received => [%s]" % request.body)
	return text('OK')

@app.route("/rabbitmq/<exchange>/<routing_key>", methods=['POST'])
async def log(request, exchange, routing_key):
	rabbitmq.publish(exchange, routing_key, request.body)
	return text('OK')

@app.route("/health")
async def health(request):
	return text('OK')

if __name__ == "__main__":

	import utils

	APP_PORT = int(utils.env("APP_PORT", 8000))
	APP_WORKERS = int(utils.env("APP_WORKERS", 1))

	exchange = utils.env('EXCHANGE')
	if exchange:
		rabbitmq.create_exchange(exchange)


	app.run(host="0.0.0.0", port=APP_PORT, workers=APP_WORKERS)
