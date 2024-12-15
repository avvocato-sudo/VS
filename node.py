import grpc
from concurrent import futures
import os
import logging
import threading
import time
import network_manager_pb2 as pb2
import network_manager_pb2_grpc as pb2_grpc

logging.basicConfig(level=logging.INFO)


class NodeService(pb2_grpc.NodeServiceServicer):
    def __init__(self, node_id, neighbors):
        self.node_id = node_id
        self.unique_messages = set()
        self.neighbors = neighbors  # List of neighbor node addresses

    def GossipMessage(self, request, context):
        if request.message not in self.unique_messages:
            logging.info(f"Node {self.node_id} received new message: {request.message}")
            self.unique_messages.add(request.message)

            # Forward the message to neighbors
            for neighbor in self.neighbors:
                try:
                    channel = grpc.insecure_channel(neighbor)
                    stub = pb2_grpc.NodeServiceStub(channel)
                    stub.GossipMessage(pb2.MessageRequest(message=request.message))
                except Exception as e:
                    logging.error(f"Failed to send message to {neighbor}: {e}")
        return pb2.Empty()

    def GetUniqueMessageCount(self, request, context):
        count = len(self.unique_messages)
        logging.info(f"Node {self.node_id} has {count} unique messages.")
        return pb2.MessageCount(count=count)


def send_periodic_messages(stub, node_id):
    """Send periodic gRPC messages every 5 seconds."""
    while True:
        message = f"Hello from Node {node_id}"
        try:
            logging.info(f"Node {node_id} sending message: {message}")
            stub.GossipMessage(pb2.MessageRequest(message=message))
        except Exception as e:
            logging.error(f"Error sending message: {e}")
        time.sleep(5)


def serve():
    node_id = os.getenv("NODE_ID", "1")
    port = os.getenv("NODE_PORT", "50050")
    neighbors_env = os.getenv("NEIGHBORS", "")
    neighbors = neighbors_env.split(",") if neighbors_env else []

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_NodeServiceServicer_to_server(NodeService(node_id, neighbors), server)
    server.add_insecure_port(f"[::]:{port}")
    logging.info(f"Node {node_id} started on port {port} with neighbors: {neighbors}")
    server.start()

    # Create stubs for each neighbor
    stubs = [pb2_grpc.NodeServiceStub(grpc.insecure_channel(neighbor)) for neighbor in neighbors]

    # Start periodic message-sending threads for each neighbor
    for stub in stubs:
        threading.Thread(target=send_periodic_messages, args=(stub, node_id), daemon=True).start()

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
