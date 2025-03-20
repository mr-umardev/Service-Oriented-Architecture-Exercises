from kafka import KafkaProducer
import json
import time

KAFKA_BROKER = "localhost:9092"
TOPIC = "order_topic"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_orders():
    orders = [
        {"order_id": 1, "product": "Laptop", "price": 1200},
        {"order_id": 2, "product": "Phone", "price": 800},
        {"order_id": 3, "product": "Tablet", "price": 400}
    ]

    for order in orders:
        producer.send(TOPIC, order)
        print(f"Sent: {order}")
        time.sleep(1)

    producer.flush()

if __name__ == "__main__":
    send_orders()
