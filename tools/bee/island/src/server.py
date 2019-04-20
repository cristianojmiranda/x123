from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from sanic.response import text
from sanic.exceptions import NotFound

import mapa
import utils

app = Sanic()

@app.route("/mapa", methods=['POST'])
async def save_mapa(request):
	id = mapa.save_mapa(request.json)
	return json({'id': id})

@app.route("/mapa", methods=['GET'])
async def save_mapa(request):
	return json(mapa.find_mapa_by_name(request.args['name'][0]))

@app.route("/mapa/<id>", methods=['GET'])
async def get_mapa(request, id):
	data = mapa.get_mapa(id)
	if data is None:
		raise NotFound("Mapa '%s' not found" % id)
	return json(data)

@app.route("/mapa/<id>/templars", methods=['GET'])
async def get_mapa(request, id):
	return json(mapa.get_templars(id))

@app.route("/mapa/<id>", methods=['DELETE'])
async def delete(request, id):
	mapa.delete(id)
	return text('OK')

@app.route("/mapa/<id>/generate", methods=['POST'])
async def delete(request, id):
	mapa.start_map_generation(id, request.json)
	return text('OK')

@app.route("/mapa/generate/<map_gen_id>/file/<file_map_id>", methods=['POST'])
async def delete(request, map_gen_id, file_map_id):
	return json({'id': mapa.generate_file(map_gen_id, file_map_id)})

if __name__ == "__main__":

	APP_PORT = utils.env("APP_PORT", 8000, int)
	APP_WORKERS = utils.env("APP_WORKERS", 2, int)

	app.run(host="0.0.0.0", port=APP_PORT, workers=APP_WORKERS)
