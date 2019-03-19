import utils
import consul

CONSUL_HOST = utils.env("CONSUL_HOST", "localhost")
CONSUL_PORT = utils.env("CONSUL_PORT", 8500)

c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT, scheme='http')

def put(id, value):
	print("consul_put: [%s] => [%s]" % (id, value))
	c.kv.put(id, value)
