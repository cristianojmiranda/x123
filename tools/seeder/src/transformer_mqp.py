import json, yaml, rabbitmq, utils
SPRING_PROFILE=utils.env("SPRING_PROFILE", "")

conn = rabbitmq.get_connection()
channel = conn.channel()
channel.basic_qos(prefetch_count=1)

queue_name='seeder-transform'
rabbitmq.create_queue(queue_name, 'seeder', 'transform', conn)

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	sbody = body.decode("utf-8")
	message = json.loads(sbody)

	if message['type'] == 'yaml' or message['type'] == 'yml':
		if 'spring' in sbody:
			ym = yaml.load(message['data'], Loader=yaml.CLoader)
			if ym['spring']['profile'] == SPRING_PROFILE:
				message['name'] = "%s-%s" % (message['name'], ym['spring']['profile'])
				rabbitmq.publish('seeder', 'seed', message, conn)
		else:
			rabbitmq.publish('seeder', 'seed', message, conn)

	else:
		print("Invalid type")

	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback, queue=queue_name, no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
