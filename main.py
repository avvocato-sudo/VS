import os
import subprocess
import yaml

def validate_files():
    required_files = ["node.py", "network_manager_pb2.py", "network_manager_pb2_grpc.py"]
    for file in required_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file '{file}' is missing.")


def generate_docker_compose(node_count):
    validate_files()  # Ensure required files are present.

    docker_compose = {
        "version": "3.8",
        "services": {},
        "networks": {
            "my_network": {
                "driver": "bridge",
                "ipam": {
                    "config": [
                        {"subnet": "192.168.1.0/24"}
                    ]
                }
            }
        }
    }

    for node_id in range(1, node_count + 1):
        service_name = f"node{node_id}"
        docker_compose["services"][service_name] = {
            "build": ".",
            "environment": {"NODE_ID": str(node_id)},
            "networks": {
                "my_network": {
                    "ipv4_address": f"192.168.1.{node_id + 1}"
                }
            }
        }

    with open("docker-compose.yml", "w") as f:
        yaml.dump(docker_compose, f, default_flow_style=False)
    print("docker-compose.yml generated successfully.")

def start_docker_compose():
    print("Starting Docker Compose...")
    subprocess.run(["docker-compose", "up", "-d"])

def main():
    try:
        node_count = int(input("Enter the number of nodes: "))
        if node_count < 1:
            raise ValueError("Number of nodes must be at least 1.")
        generate_docker_compose(node_count)
        start_docker_compose()
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
