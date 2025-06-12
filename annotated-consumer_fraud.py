# consumer_fraud.py
import json
from kafka import KafkaConsumer
consumer = KafkaConsumer(
'events',
bootstrap_servers='localhost:9092',
group_id='fraud',
auto_offset_reset='earliest',
key_deserializer=lambda k: k.decode(),
value_deserializer=lambda v: json.loads(v.decode())
)
print("🔍 Fraud consumer listening for ORDER events…")
for msg in consumer:
event = msg.value
if event['type'] == 'order':
print(
f"→ [Order] ID {event['order_id']} "
f"by User {event['user_id']} "
f"worth ${event['amount']} "
f"at {event['timestamp']}"
)