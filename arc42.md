# arc42 Template: Distributed Systems Project

## 1. Introduction and Objectives

### 1.1 Introduction
This document describes the architecture of a distributed system designed to analyze the performance of multicast algorithms, specifically using Gossip-based random walk dissemination. The system is implemented and deployed using containerized environments and focuses on running across two physical machines, communicating via a network.

### 1.2 Objectives
- **Primary Goal**: Measure and visualize the performance of the Gossip multicast algorithm in terms of message propagation and system behavior.
- **Secondary Objectives**:
  - Ensure scalability to a variable number of nodes.
  - Maintain transparency, as outlined by Maarten van Steen, focusing on the user experience and internal system design.

---

## 2. Stakeholders

| Role                 | Name                      | Contact        | Expectation                           |
|----------------------|---------------------------|----------------|---------------------------------------|
| Professors (Clients) | Frank Matthiesen, Prof. Dr. Jan Sudeikat | N/A            | Documentation, working system, and analysis. |
| Developers           | Kjell Lööck, Duc Pham   | N/A            | Implementation and testing.          |

---

## 3. Quality Goals

### 3.1 Scalability
The system should dynamically adapt to a varying number of nodes, ensuring efficiency and consistency in message propagation as the number of participants increases.

### 3.2 Transparency
The system must abstract away the underlying distribution and topology complexities from users while ensuring that all internal functionalities align with the principles described by Maarten van Steen.

---

## 4. Constraints

- The system uses Docker Compose for deployment but can migrate to Docker Swarm if scalability or orchestration requires a more advanced setup.
- Communication between nodes must use gRPC for its structured RPC capabilities.
- The system is implemented in Python, leveraging the NetworkX library for graph topology modeling.
- Logging is a required feature to facilitate debugging and performance analysis.

---

## 5. Context and Scope

### 5.1 Functional Context
The system simulates a distributed network where nodes communicate using a Gossip-based algorithm. It measures metrics such as propagation speed and message load while running on two physical machines interconnected via a network.

### 5.2 Technical Context
Each node runs in an isolated Docker container, and communication is facilitated using gRPC. Docker Compose is used to manage multi-container deployment, allowing for scalability and cross-machine communication.

---

## 6. Solution Strategy

1. **Design**:
   - Implement a three-layer architecture:
     - Presentation Layer: Visualization of metrics (future scope).
     - Application Layer: Gossip-based message dissemination logic.
     - Data Layer: NetworkX-based graph topology and message data.
   - Leverage Python for implementation due to its extensive library support and developer familiarity.

2. **Implementation**:
   - Use NetworkX to generate random graph topologies for node placement.
   - Implement Gossip random walk algorithm for message propagation.
   - Use gRPC for inter-node communication.

3. **Testing**:
   - Develop unit tests for node behavior and gRPC communication.
   - Create integration tests for verifying message propagation in random graph topologies.
   - Log system activities for debugging and metrics collection.

---

## 7. Building Blocks

### 7.1 Key Components
- **Node Container**:
  - Implements the Gossip algorithm.
  - Handles incoming and outgoing messages.
  - Logs performance metrics.

- **Coordinator** (Optional):
  - Initializes the network.
  - Collects and aggregates metrics.

- **Visualization Tool** (Future scope):
  - Visualizes message propagation over time.

---

## 8. Runtime View

### 8.1 Typical Scenario
1. Nodes are deployed as Docker containers on two physical machines.
2. The system initializes a random graph topology using NetworkX.
3. Messages are propagated through the network using the Gossip random walk algorithm.
4. Logs are generated at each node for performance analysis.

---

## 9. Deployment View

### 9.1 Deployment Approach
- Use Docker Compose for managing containers on each machine.
- Leverage overlay networking to enable communication between containers on different machines.

---

## 10. Cross-Cutting Concepts

### 10.1 Logging
- Use Python’s `logging` library to capture node activities and performance metrics.

### 10.2 Monitoring (Optional)
- Include basic monitoring to observe node activity during runtime.

---

## 11. Experiments

### 11.1 Planned Experiments
- Measure message propagation speed in random graph topologies.
- Collect metrics such as message count, latency, and node activity.
- Perform scalability tests by varying the number of nodes.

---

## 12. Risks and Technical Debt

- **Cross-Machine Communication**: Ensuring reliable communication between containers.
- **Logging Overhead**: Excessive logging may impact performance.
- **Scalability Limits**: Docker Compose may not scale well for very large networks.

---

## 13. Glossary

| Term       | Definition                                   |
|------------|---------------------------------------------|
| Gossip     | A communication protocol for information dissemination based on random peer-to-peer message exchanges. |
| Node       | A process participating in the distributed system. |
| Docker     | A containerization platform for deploying applications. |
| gRPC       | A high-performance RPC framework.          |

