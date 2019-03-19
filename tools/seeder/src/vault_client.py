import utils, hvac

VAULT_HOST = utils.env("VAULT_HOST", 'localhost')
VAULT_SCHEMA = utils.env("VAULT_SCHEMA", 'http')
VAULT_PORT = int(utils.env("VAULT_PORT", 8200))
VAULT_TOKEN = utils.env("VAULT_TOKEN")

vault_url = "%s://%s:%i" % (VAULT_SCHEMA, VAULT_HOST, VAULT_PORT)
client = hvac.Client(url=vault_url, token=VAULT_TOKEN)

def put(app, key, value):
	print("vault_put: [%s][%s] => [%s]" % (app, id, value))
	#client.write('secret/foo', baz='bar', lease='1h')
	client.secrets.kv.v2.create_or_update_secret(
    	path="secret/%s" % app,
    	secret=dict(id=value),
    	#cas=0,
	)
