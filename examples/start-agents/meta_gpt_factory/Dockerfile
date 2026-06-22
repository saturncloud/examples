FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 libgbm1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Step 1: Install the Anchors and Pip upgrade
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 2: Install Playwright Chromium
RUN playwright install chromium

RUN mkdir -p /app/config /app/workspace
COPY . .

EXPOSE 8501
ENV METAGPT_CONFIG_PATH=/app/config/config2.yaml

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]