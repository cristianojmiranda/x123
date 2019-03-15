from rabbitmq import connection, publish

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	publish('seeder-exchange', 'seed', body)

channel = connection.channel()
channel.basic_consume(callback, queue='seeder-transform')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
