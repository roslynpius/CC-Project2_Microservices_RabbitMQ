import pymongo
import pika
import time
import json
import logging
logging.basicConfig(level=logging.INFO)

time.sleep(9)
# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://database")
db = client["studentdatabase"]
collection = db["students"]
print('172.17.0.1')
time.sleep(9)


# Establish connection with RabbitMQ
credentials = pika.PlainCredentials('guest','guest')
parameters = pika.ConnectionParameters('172.17.0.1',5672,'/',credentials,heartbeat=1200)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# Declare queue and bind to exchange
channel.queue_declare(queue='read_database')
channel.queue_bind(queue='read_database', exchange='student_management', routing_key='read_database')

# Define callback function for reading from database
def read_database_callback(ch, method, properties, body):
    # Retrieve all documents in the collection
    documents = collection.find()
    # Print each document
    for document in documents:
        logging.info("%s",document)
    ch.basic_ack(delivery_tag=method.delivery_tag)
# Consume messages from queue
channel.basic_consume(queue='read_database', on_message_callback=read_database_callback)

# Start consuming messages
channel.start_consuming()
