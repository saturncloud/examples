FROM python:3.9-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY server.py .
CMD ["python", "server.py"]
