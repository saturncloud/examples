#!/bin/bash

# 1. Start Kafka in KRaft mode (Daemon)
# Updated path to match the 'kafka' folder created in setup
echo "Starting Kafka Broker..."
./kafka/bin/kafka-server-start.sh -daemon ./kafka/config/kraft/server.properties

# 2. Wait for Kafka to initialize
sleep 5

# 3. Start the Data Producer using the Virtual Env Python
echo "Starting Data Producer..."
./env/bin/python producer.py &

# 4. Start the Streamlit Dashboard using the Virtual Env Python
echo "Launching Dashboard..."
./env/bin/python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0