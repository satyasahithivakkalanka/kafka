# producer_order.py
import json, time, random
from kafka import KafkaProducer
producer = KafkaProducer(
bootstrap_servers='localhost:9092',
key_serializer=lambda k: k.encode(),
value_serializer=lambda v: json.dumps(v).encode()
)
order_id = 100
print("🚚 Order producer starting…")
while True:
user = random.randint(1,100)
event = {
'type': 'order',
'user_id': user,
'order_id': order_id,
'amount': round(random.uniform(10,200),2),
'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')
}
producer.send('events', key=str(user), value=event)
print("🚚 Order:", event)
order_id += 1
time.sleep(3)