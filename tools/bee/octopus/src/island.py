import utils, requests

ISLAND_URL = utils.env("ISLAND_URL", "http://localhost:8000")

def generate_file(map_gen_id, file_map_id):
    resp = requests.post("%s/mapa/generate/%s/file/%s" % (ISLAND_URL, map_gen_id, file_map_id))
    if resp.status_code == 200:
        return resp.json()['id']
    raise Exception("Generation failed: [%s] - %s" % (resp.status_code, resp.text))
