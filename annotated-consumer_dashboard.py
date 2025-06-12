# consumer_dashboard.py
import json
from kafka import KafkaConsumer
consumer = KafkaConsumer(
'events',
bootstrap_servers='localhost:9092',
group_id='dashboard',
auto_offset_reset='earliest',
key_deserializer=lambda k: k.decode(),
value_deserializer=lambda v: json.loads(v.decode())
)
print("📊 Dashboard consumer listening for CLICK events…")
for msg in consumer:
event = msg.value
if event['type']=='click':
print(f"→ [Click] User {event['user_id']} at {event['page']}
({event['timestamp']})")