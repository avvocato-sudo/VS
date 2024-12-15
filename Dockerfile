FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY node.py .
COPY network_manager.proto .
COPY network_manager_pb2.py network_manager_pb2_grpc.py .

CMD ["python", "node.py"]
