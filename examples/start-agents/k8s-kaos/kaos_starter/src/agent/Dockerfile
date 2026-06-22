FROM python:3.9-slim
WORKDIR /app
RUN pip install fastapi uvicorn pydantic requests
COPY app.py .
CMD ["python", "app.py"]
