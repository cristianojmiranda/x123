from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from sanic.response import text

import os
import utils
import template

app = Sanic()

@app.route("/<id>", methods=['POST'])
async def update(request, id):
	template.save(id, request.body)
	return json({'id': id})

@app.route("/<id>", methods=['GET'])
async def get(request, id):
	logger.info("Get template %s " % id)
	_t = template.get(id)
	logger.info("template: %s" % _t)
	return text(_t)

@app.route("/<id>", methods=['DELETE'])
async def delete(request, id):
	template.delete(id)
	return text('OK')

@app.route("/<id>/compile", methods=['POST'])
async def compile(request, id):
	version = request.args['version'][0] if 'version' in request.args else '0'
	if version == '1':
		return text(template.compile_v1(id, request.json))
	return text(template.compile_v2(id, request.json))

if __name__ == "__main__":

	APP_PORT = utils.env("APP_PORT", 8000, int)
	APP_WORKERS = utils.env("APP_WORKERS", 2, int)

	app.run(host="0.0.0.0", port=APP_PORT, workers=APP_WORKERS)
