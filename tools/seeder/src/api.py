from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from sanic.response import text

import fstore
import rabbitmq

app = Sanic()

@app.route("/seed/<store>/<profile>", methods=['POST'])
async def seed(request, store, profile):
	id = fstore.save(request.files["file"][0].body)
	extension = request.files["file"][0].name.split('.')[-1]
	message = { 'id': id,
				'storage': store,
				'name': request.files["file"][0].name,
				'type': extension,
				'profile': profile
			  }
	logger.info("send '%s' to be splitted" % str(message))
	rabbitmq.publish("seeder", "split", message)
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

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)
