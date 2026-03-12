#!/bin/bash

# 1. Update and install system-level dependencies
echo "📦 Installing system dependencies (Python 3.10 and Java 11)..."
apt update
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt install -y python3.10 python3.10-venv python3.10-dev openjdk-11-jdk build-essential libffi-dev libssl-dev

# 2. Setup Java environment variables for Spark
echo "☕ Configuring JAVA_HOME..."
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.bashrc

# 3. Create and configure the Virtual Environment
echo "🐍 Creating Python 3.10 virtual environment..."
python3.10 -m venv virt-env
source virt-env/bin/activate

# 4. Install Python libraries
echo "🚀 Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete! Run 'source virt-env/bin/activate' to start."