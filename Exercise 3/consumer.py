from kafka import KafkaConsumer
import json

KAFKA_BROKER = "localhost:9092"
TOPIC = "order_topic"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest"
)

print("Consumer is listening for messages...")

for message in consumer:
    order = message.value
    print(f"Received Order: {order}")
