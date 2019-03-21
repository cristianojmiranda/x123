from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from sanic.response import text

import os
import fstore
import rabbitmq, utils

exchange = utils.env('EXCHANGE', 'seeder')
output_routing_key = utils.env('OUTPUT_RK', 'split')
KUBE_BOUNCE_COMMAND = utils.env('KUBE_BOUNCE_COMMAND', '''kubectl set env deployment/%s --env="LAST_MANUAL_RESTART=$(date +%%s)"''')

rabbitmq.create_exchange(exchange);
app = Sanic()

@app.route("/seed/<store>/<flavor>", methods=['POST'])
async def seed(request, store, flavor):
	id = fstore.save(request.files["file"][0].body)
	extension = request.files["file"][0].name.split('.')[-1]
	name = request.files["file"][0].name.split('.')[0]
	message = { 'id': id,
				'storage': store,
				'name': name,
				'type': extension if extension not in ['yaml', 'yml'] else 'yaml',
				'flavor': flavor
			  }
	logger.info("send '%s' to be split" % str(message))
	rabbitmq.publish(exchange, output_routing_key, message)
	return json(message)

@app.route("/storage/file/<id>", methods=['GET'])
async def get_file(request, id):
	f = fstore.get(id)
	return text(f)

@app.route("/storage/file/<id>", methods=['DELETE'])
async def get_file(request, id):
	fstore.delete(id)
	return text("DELETED")

@app.route("/health")
async def health(request):
	return text('OK')

@app.route("/k8s/bounce/<app>", methods=['GET'])
async def get_file(request, app):
	logger.info("Bouncing app %s" % app)
	#kubectl --insecure-skip-tls-verify  get pods
	#cat ~/.kube/config (/root/.kube)
	out = os.popen(KUBE_BOUNCE_COMMAND % app)
	logger.debug("bounce output=%s" % out.read())
	logger.debug("bounce output=%s" % out.close())
	return text("DONE")

if __name__ == "__main__":

	APP_PORT = int(utils.env("APP_PORT", 8000))
	APP_WORKERS = int(utils.env("APP_WORKERS", 2))

	app.run(host="0.0.0.0", port=APP_PORT, workers=APP_WORKERS)
