import json
import utils
import requests

TEMPLAR_URL = utils.env("TEMPLAR_URL", "http://localhost:8001")

def compile(id, config):
    resp = requests.post("%s/%s/compile" % (TEMPLAR_URL, id), data=json.dumps(config))
    if resp.status_code == 200:
        return resp.text
    raise Exception("Failed to compile template '%s. %s - %s" % (id, resp.status_code, resp.text))
