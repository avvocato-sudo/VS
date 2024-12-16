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
        logging.info(f"Node {self.node_id} received new message: {request.message}")
        if request.message not in self.unique_messages:
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


def send_periodic_messages(address, node_id, message):
    stub = connect_with_retries(address)
    if not stub:
        logging.error(f"Could not establish connection to {address}")
        return
    while True:
        try:
            logging.info(f"Node {node_id} sending message: {message} to {address}")
            stub.GossipMessage(pb2.MessageRequest(message=message))
        except Exception as e:
            logging.error(f"Error sending message to {address}: {e}")
        time.sleep(5)

def connect_with_retries(address, retries=5, delay=2):
    for attempt in range(retries):
        try:
            channel = grpc.insecure_channel(address)
            grpc.channel_ready_future(channel).result(timeout=5)
            return pb2_grpc.NodeServiceStub(channel)
        except grpc.FutureTimeoutError:
            logging.warning(f"Retrying connection to {address} (attempt {attempt + 1})...")
            time.sleep(delay)
    logging.error(f"Failed to connect to {address} after {retries} attempts.")
    return None


def serve():
    node_id = os.getenv("NODE_ID", "1")
    port = os.getenv("NODE_PORT", "50050")
    neighbors_env = os.getenv("NEIGHBORS", "")
    neighbors = neighbors_env.split(",") if neighbors_env else []

    logging.info(f"Node {node_id} listening on port {port} with neighbors: {neighbors}")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_NodeServiceServicer_to_server(NodeService(node_id, neighbors), server)
    server.add_insecure_port(f"[::]:{port}")
    logging.info(f"Node {node_id} started on port {port}.")
    server.start()

    # Wait for all nodes to initialize
    time.sleep(5)

    # Start periodic messaging threads
    for neighbor in neighbors:
        threading.Thread(
            target=send_periodic_messages,
            args=(neighbor, node_id, f"Hello from Node {node_id}"),
            daemon=True,
        ).start()

    server.wait_for_termination()

if __name__ == "__main__":
    serve()
