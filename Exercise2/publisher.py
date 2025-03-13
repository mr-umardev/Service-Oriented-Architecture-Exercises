import pika
import json
import logging

# Configure logging
logging.basicConfig(filename='publisher.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Establish connection with RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare a queue (ensuring it exists)
    channel.queue_declare(queue='order_queue')

    # Sample order message
    order = {
        "order_id": 101,
        "product": "Laptop",
        "quantity": 1
    }

    # Publish message to the queue
    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=json.dumps(order),
        properties=pika.BasicProperties(
            delivery_mode=2  # Make the message persistent
        )
    )

    print(" [✔] Sent Order:", order)
    logging.info(f"Order Sent: {order}")

except Exception as e:
    logging.error(f"Error in publisher: {str(e)}")
    print(" [!] Error:", str(e))

finally:
    # Ensure the connection is closed properly
    if 'connection' in locals() and connection.is_open:
        connection.close()
