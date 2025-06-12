# dashboard_app.py
import json, time
from collections import deque, Counter
import pandas as pd
import streamlit as st
from kafka import KafkaConsumer
# —— Streamlit page config ——
st.set_page_config(layout="wide")
st.title("📊 ShopEase Mini Dashboard")
# —— Sidebar controls ——
window_size = st.sidebar.slider(
"Event Window Size", min_value=10, max_value=200, value=50
)
topic_name = st.sidebar.text_input("Kafka Topic", "events")
# —— Data buffers ——
timestamps = deque(maxlen=window_size)
click_counts = deque(maxlen=window_size)
order_counts = deque(maxlen=window_size)
pages = deque(maxlen=window_size)
order_amounts = deque(maxlen=window_size)
latest_events = deque(maxlen=5) # keep last 5 events
users_set = set()
# —— Metrics placeholders ——
metric1 = st.metric("Total Clicks", 0)
metric2 = st.metric("Total Orders", 0)
metric3 = st.metric("Unique Users", 0)
conversion_placeholder = st.empty()
# —— Charts placeholders ——
line_chart = st.line_chart(pd.DataFrame({'Clicks': [], 'Orders': []}))
bar_chart = st.bar_chart(pd.DataFrame({'Page Views': []}, index=[]))
hist_plot = st.empty()
table_plot = st.empty()
# —— Kafka consumer setup ——
consumer = KafkaConsumer(
topic_name,
bootstrap_servers='localhost:9092',
auto_offset_reset='latest',
value_deserializer=lambda b: json.loads(b.decode('utf-8'))
)
# —— Counters ——
total_clicks = 0
total_orders = 0
# —— Consume & Update Loop ——
for msg in consumer:
evt = msg.value
ts = pd.to_datetime(evt['timestamp'])
# Update buffers & counters
timestamps.append(ts)
if evt['type'] == 'click':
total_clicks += 1
click_counts.append(1)
order_counts.append(0)
pages.append(evt['page'])
order_amounts.append(0)
else:
total_orders += 1
click_counts.append(0)
order_counts.append(1)
pages.append(None)
order_amounts.append(evt['amount'])
users_set.add(evt['user_id'])
latest_events.append({
'timestamp': evt['timestamp'],
'type': evt['type'],
'user_id': evt['user_id'],
'page_or_amount': evt.get('page', evt.get('amount'))
})
# —— Update metrics ——
metric1.metric("Total Clicks", total_clicks)
metric2.metric("Total Orders", total_orders)
metric3.metric("Unique Users", len(users_set))
# Add conversion rate
conversion_rate = (total_orders / total_clicks * 100) if total_clicks else 0
conversion_placeholder.metric("Conversion Rate", f"{conversion_rate:.2f}%")
# —— Update event count chart ——
df_line = pd.DataFrame({
'Clicks': [sum(click_counts)],
'Orders': [sum(order_counts)]
}, index=[ts])
line_chart.add_rows(df_line)
# —— Update page-view bar chart ——
page_counts = Counter(p for p in pages if p)
df_bar = pd.DataFrame.from_dict(
page_counts, orient='index', columns=['Page Views']
)
bar_chart.data = df_bar
# —— Update order amount histogram ——
amounts = [a for a in order_amounts if a > 0]
if amounts:
df_hist = pd.DataFrame({'Amount': amounts})
hist_data = df_hist['Amount'].value_counts(bins=10).sort_index()
hist_plot.bar_chart(hist_data)
# —— Update latest events table ——
df_table = pd.DataFrame(list(latest_events))
df_table = df_table[['timestamp', 'type', 'user_id', 'page_or_amount']]
df_table.columns = ['Timestamp', 'Type', 'User ID', 'Page / Amount']
table_plot.table(df_table)
time.sleep(0.1)