import pika
import json
import logging
from prometheus_client import start_http_server, Counter

# Configure logging
logging.basicConfig(filename='consumer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define Prometheus metric
order_count = Counter('processed_orders', 'Number of orders processed')

# Start Prometheus server on port 8000
start_http_server(8000)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare the queue (must match the publisher's queue)
channel.queue_declare(queue='order_queue')

# Define callback function for message processing
def callback(ch, method, properties, body):
    order = json.loads(body)
    
    # Logging received order
    logging.info(f"Received Order: {order}")
    
    # Print to console
    print(f" [x] Received Order: {order}")
    
    # Simulating storing to a database
    print(f" [✔] Order {order['order_id']} stored successfully!")

    # Increment Prometheus counter
    order_count.inc()

    # Acknowledge message processing
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up consumer to listen on 'order_queue'
channel.basic_consume(queue='order_queue', on_message_callback=callback)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
