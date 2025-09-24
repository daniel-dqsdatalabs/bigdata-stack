# Sandbox

This project provides a comprehensive data engineering environment using Docker. It includes various tools and services commonly used in data engineering workflows, allowing you to experiment, learn, and develop data pipelines and analytics solutions.

## Table of Contents
- [Overview](#overview)
- [Components](#components)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)


## Overview

This sandbox environment sets up a local ecosystem of data engineering tools, including:

- PostgreSQL for relational database storage
- MinIO for object storage (S3-compatible)
- Apache Spark for distributed data processing
- Apache Flink for stream processing
- Apache Kafka for event streaming
- Jupyter Notebooks for interactive data analysis and visualization

All services are containerized using Docker, making it easy to set up and tear down the entire environment.

## Components

- **PostgreSQL**: Relational database with sample data (Northwind dataset)
- **MinIO**: S3-compatible object storage
- **Apache Spark**: Distributed computing system with a master and worker node
- **Apache Flink**: Stream processing framework with a job manager and task manager
- **Apache Kafka 4.0.0**: Official Kafka image running in KRaft mode with next generation consumer protocol (KIP-848) and a producer that generates synthetic data
- **Kafka UI**: Web interface for monitoring and managing Kafka clusters
- **Jupyter Notebooks**: Web-based interactive development environment

## Prerequisites

- Docker
- Docker Compose
- Git (optional, for cloning the repository)

## Getting Started

1. Clone this repository (or download the ZIP file):

   ```
   git clone https://github.com/daniel-dqsdatalabs/bigdata-stack.git
   cd bigdata-stack
   ```

2. Create a `.env` file in the project root and add the following environment variables:

   ```
   POSTGRES_USER=your_postgres_username
   POSTGRES_PASSWORD=your_postgres_password
   MINIO_ROOT_USER=your_minio_root_user
   MINIO_ROOT_PASSWORD=your_minio_root_password
   KAFKA_CLUSTER_ID=your-unique-kafka-cluster-id
   ```

3. Build and start the containers:

   ```
   docker-compose up --build
   ```

4. Wait for all services to start up. This may take a few minutes on the first run.

## Usage

Once all services are up and running, you can access them through the following URLs:

- Jupyter Notebooks: <http://localhost:8888>
- Spark Master UI: <http://localhost:8080>
- Spark Worker UI: <http://localhost:8082>
- Flink JobManager UI: <http://localhost:8081>
- MinIO Console: <http://localhost:9001>
- Kafka UI: <http://localhost:8090>

To connect to PostgreSQL:

- Host: localhost
- Port: 5432
- Database: northwind
- User: (as specified in .env file)
- Password: (as specified in .env file)

To connect to Kafka:

- Bootstrap server: localhost:9092
- Topics created by the producer:
  - users: Contains synthetic user data
  - products: Contains synthetic product data
  - transactions: Contains synthetic transaction data

To consume Kafka messages from the command line:

```
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic users --from-beginning
```

To create a topic with the new consumer protocol:

```
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic my-topic --bootstrap-server kafka:9092 --partitions 3 --replication-factor 1
```

## Configuration

- PostgreSQL: The Northwind sample database is automatically loaded on first startup.
- MinIO: Configure using the MinIO Console or `mc` client.
- Spark & Flink: Additional configuration can be done by modifying the respective Dockerfiles and docker-compose.yml entries.
- Kafka: Using the official Apache Kafka 4.0.0 image with the following key features:
  - No ZooKeeper dependency (KRaft mode only)
  - Next generation consumer group protocol (KIP-848)
  - Early access to Queues for Kafka (KIP-932) - disabled by default
  - Custom configuration via mounted server.properties file
  - Synthetic data producer in a separate container
- Jupyter: Custom packages can be added by modifying the Jupyter Dockerfile.

## Troubleshooting

- If services fail to start, check the Docker logs:

  ```
  docker-compose logs [service_name]
  ```

- Ensure all required ports are free on your host machine.
- For PostgreSQL issues, check the init-db.sh script and ensure it has the correct permissions.
- For Kafka issues, verify the KAFKA_CLUSTER_ID is set correctly in your .env file.
- If Kafka fails to start, it might be due to the new features in 4.0.0. Check the logs with:
  ```
  docker-compose logs kafka
  ```

