import utils, hvac, logging

S_VAULT_HOST = utils.env("S_VAULT_HOST", 'localhost')
S_VAULT_SCHEMA = utils.env("S_VAULT_SCHEMA", 'http')
S_VAULT_PORT = int(utils.env("S_VAULT_PORT", 8200))
S_VAULT_TOKEN = utils.env("S_VAULT_TOKEN")

vault_url = "%s://%s:%i" % (S_VAULT_SCHEMA, S_VAULT_HOST, S_VAULT_PORT)
client = hvac.Client(url=vault_url, token=S_VAULT_TOKEN)

def put(key, value):
	logging.info("vault_put: [%s] => [%s]" % (key, value))
	client.secrets.kv.v2.create_or_update_secret(path=key, secret=dict(data=value))
