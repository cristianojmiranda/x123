import utils
import consul, logging

CONSUL_HOST = utils.env("CONSUL_HOST", "localhost")
CONSUL_PORT = utils.env("CONSUL_PORT", 8500)

c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT, scheme='http')

def put(id, value):
	logging.info("consul_put: [%s] => [%s]" % (id, value))
	c.kv.put(id, value)
