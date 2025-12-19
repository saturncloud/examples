import json
import time
import random
from confluent_kafka import Producer

# Connect to the local broker started in Step 4
KAFKA_CONFIG = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(KAFKA_CONFIG)
topic = "sensor_data"

print(f"🚀 Producer started. Sending data to topic: {topic}")

try:
    while True:
        data = {
            "timestamp": time.time(),
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "device_id": "sensor_01"
        }
        producer.produce(topic, json.dumps(data).encode('utf-8'))
        producer.flush() # Ensure message is sent
        time.sleep(1)    # 1 Hz frequency
except KeyboardInterrupt:
    print("Stopping Producer...")