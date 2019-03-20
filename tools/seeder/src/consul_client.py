import utils
import consul, logging

S_CONSUL_HOST = utils.env("S_CONSUL_HOST", "localhost")
S_CONSUL_PORT = int(utils.env("S_CONSUL_PORT", 8500))

c = consul.Consul(host=S_CONSUL_HOST, port=S_CONSUL_PORT, scheme='http')

def put(id, value):
	logging.info("consul_put: [%s] => [%s]" % (id, value))
	c.kv.put(id, value)
