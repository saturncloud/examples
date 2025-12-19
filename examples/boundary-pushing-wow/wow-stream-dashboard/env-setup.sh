#!/bin/bash

# --- 1. System Dependencies ---
echo "Installing Java (OpenJDK 11)..."
apt-get update && apt-get install -y openjdk-11-jdk

# --- 2. Kafka Setup ---
KAFKA_VER="3.9.1"
KAFKA_DIR="/workspace/kafka"

# FIX: Force clear previous metadata to prevent Cluster ID mismatch
echo "Cleaning up old Kafka metadata..."
rm -rf /tmp/kraft-combined-logs
pkill -9 -f kafka

if [ ! -d "$KAFKA_DIR" ]; then
    echo "Downloading Kafka..."
    wget https://downloads.apache.org/kafka/$KAFKA_VER/kafka_2.13-$KAFKA_VER.tgz
    tar -xzf kafka_2.13-$KAFKA_VER.tgz
    mv kafka_2.13-$KAFKA_VER $KAFKA_DIR
    rm kafka_2.13-$KAFKA_VER.tgz
fi

# ALWAYS Re-format to ensure the current run matches the current Cluster ID
echo "Formatting Kafka KRaft Storage..."
cd $KAFKA_DIR
KAFKA_CLUSTER_ID=$(bin/kafka-storage.sh random-uuid)
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
cd ..

# --- 3. Python Environment ---
echo "Syncing Virtual Environment..."
if [ ! -d "env" ]; then
    python3 -m venv env
fi
./env/bin/pip install --upgrade pip
./env/bin/pip install -r requirements.txt

echo "✅ Environment Reset and Ready!"