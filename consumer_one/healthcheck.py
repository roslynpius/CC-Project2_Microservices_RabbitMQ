import pika
import time
import logging

logging.basicConfig(level=logging.INFO)
print('172.17.0.1')
time.sleep(9)

# Establish connection with RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.1',5672,'/',credentials,heartbeat=1200)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


print("Consumer running")
# Declare exchange and queue
channel.exchange_declare(exchange='student_management', exchange_type='direct')
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='student_management', queue='health_check', routing_key='health_check')

def callback(ch, method, properties, body):
    logging.info("Received message: %s", body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up consumer to listen for messages on queue
channel.basic_consume(queue='health_check', on_message_callback=callback)

print(' [*] Waiting for health check messages. To exit press CTRL+C')
channel.start_consuming()
