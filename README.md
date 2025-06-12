# ShopEase: Real-Time E-Commerce Analytics with Apache Kafka

This tutorial project demonstrates how Apache Kafka can be used to build a real-time data streaming pipeline for an e-commerce platform. You'll simulate user clicks and orders, process them through Kafka, and visualize the data with a Streamlit dashboard.

---

## Project Overview

**Goal:** Create a mini real-time data pipeline using Kafka producers, consumers, and a live dashboard.

**Use Case:** Simulate user activity (clicks and orders) on an e-commerce site and monitor it using a dashboard for business intelligence and fraud detection.

---

## Requirements

- OS: macOS 10.14+ / Windows 10+
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.7+
- Visual Studio Code or any editor
- Terminal / PowerShell

---

## Setup Instructions

### Install Docker and Python

Install Docker Desktop and Python 3.7+. Ensure Docker is running (whale icon visible).

### Project Setup

```bash
# Clone or create a project directory
mkdir kafka-tutorial
cd kafka-tutorial

# Create docker-compose.yml
# Paste configuration from the tutorial document
```

### Start Kafka and Zookeeper

```bash
docker-compose up -d
docker ps
```

---

##  Kafka Topic Creation

```bash
docker exec -it kafka \
  kafka-topics --create \
  --topic events \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

---

##  Python Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
.\venv\Scripts\Activate.ps1  # Windows

pip install kafka-python streamlit pandas requests watchdog
```

---

##  Files & Components

###  Producers
- `producer_click.py`: Simulates clickstream data.
- `producer_order.py`: Simulates order data.

###  Consumers
- `consumer_dashboard.py`: Reads and displays click events.
- `consumer_fraud.py`: Detects suspicious orders.

###  Dashboard
- `dashboard_app.py`: Interactive Streamlit dashboard with metrics and charts.

---

##  Running the Pipeline

Open 4 terminal tabs and run:

```bash
source venv/bin/activate
python producer_click.py
```

```bash
source venv/bin/activate
python producer_order.py
```

```bash
source venv/bin/activate
python consumer_dashboard.py
```

```bash
source venv/bin/activate
python consumer_fraud.py
```

Then, launch the dashboard:

```bash
source venv/bin/activate
streamlit run dashboard_app.py
```

Visit `http://localhost:8501` to view your real-time dashboard.

---

##  Dashboard Features

- Live Click & Order Counts
- Conversion Rate
- Page View Distribution
- Order Amount Histogram
- Latest 5 Events Table

---

##  Learning Outcomes

- Kafka producer-consumer architecture
- Real-time data processing
- Streamlit dashboard development
- Docker-based Kafka setup
