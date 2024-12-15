import grpc
from concurrent import futures
import os
import logging
import network_manager_pb2 as pb2
import network_manager_pb2_grpc as pb2_grpc


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
    node_id = os.getenv("NODE_ID", "1")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_NodeServiceServicer_to_server(NodeService(node_id), server)
    server.add_insecure_port("[::]:50051")
    logging.info(f"Node {node_id} started on port 50051.")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
