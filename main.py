import os
import subprocess
import yaml
import networkx as nx


def validate_files():
    required_files = ["node.py", "network_manager_pb2.py", "network_manager_pb2_grpc.py"]
    for file in required_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file '{file}' is missing.")


def generate_topology(num_nodes, topology_type):
    """Generate a topology using NetworkX."""
    if topology_type == "ring":
        return nx.cycle_graph(num_nodes)
    elif topology_type == "fully_connected":
        return nx.complete_graph(num_nodes)
    elif topology_type == "random":
        return nx.gnp_random_graph(num_nodes, 0.5)  # 50% chance of edge creation
    else:
        raise ValueError("Unsupported topology type")


def generate_docker_compose(node_count, topology_type):
    validate_files()  # Ensure required files are present.

    # Generate the graph for the specified topology
    graph = generate_topology(node_count, topology_type)

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

    for node_id in range(node_count):
        # Get neighbors from the graph
        neighbors = [
            f"192.168.1.{neighbor + 2}:50050{+ neighbor + 2}" for neighbor in graph.neighbors(node_id)
        ]

        service_name = f"node{node_id}"
        docker_compose["services"][service_name] = {
            "build": ".",
            "environment": {
                "NODE_ID": str(node_id),
                "NODE_PORT": f"50050{+ node_id + 2}",
                "NEIGHBORS": ",".join(neighbors),
            },
            "networks": {
                "my_network": {
                    "ipv4_address": f"192.168.1.{node_id + 2}"
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

        topology_type = input("Enter the topology type (ring, fully_connected, random): ").strip()
        if topology_type not in {"ring", "fully_connected", "random"}:
            raise ValueError("Unsupported topology type.")

        generate_docker_compose(node_count, topology_type)
        start_docker_compose()
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
