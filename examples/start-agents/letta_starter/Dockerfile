# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for Letta and Postgres connections
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose ports (Streamlit: 8000, Letta Server: 8283)
EXPOSE 8000
EXPOSE 8283

# Set environment variable to trigger auto-start in run.py
ENV CLOUD_ENV=true

# Start the Master Orchestrator
CMD ["python", "run.py"]
