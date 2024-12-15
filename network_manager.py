import grpc
from concurrent import futures
import os
import logging
import network_manager_pb2 as pb2
import network_manager_pb2_grpc
from pkg_resources import get_distribution
import time

logging.basicConfig(level=logging.INFO)

class NodeService(pb2_grpc.NodeServiceServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.unique_messages = set()

    def GossipMessage(self, request, context):
        # Process incoming message
        logging.info(f"Node {self.node_id} received message: {request.message}")
        self.unique_messages.add(request.message)
        return pb2.Empty()

    def GetUniqueMessageCount(self, request, context):
        # Return the count of unique messages processed by this node
        count = len(self.unique_messages)
        logging.info(f"Node {self.node_id} has {count} unique messages.")
        return pb2.MessageCount(count=count)

def serve():
    # Retrieve environment variables
    node_id = os.getenv("NODE_ID", "1")

    # Log library versions
    protobuf_version = get_distribution("protobuf").version
    grpcio_version = get_distribution("grpcio").version
    logging.info(f"Starting Node {node_id}")
    logging.info(f"Protobuf version: {protobuf_version}")
    logging.info(f"gRPC version: {grpcio_version}")

    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_NodeServiceServicer_to_server(NodeService(node_id), server)
    server.add_insecure_port("[::]:50051")
    logging.info(f"Node {node_id} started on port 50051.")
    server.start()

    # Prevent the process from exiting
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Node shutting down...")
        server.stop(0)

if __name__ == "__main__":
    serve()
