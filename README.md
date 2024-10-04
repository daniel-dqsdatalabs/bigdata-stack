# Data Engineering Sandbox

This project provides a comprehensive data engineering sandbox environment using Docker. It includes various tools and services commonly used in data engineering workflows, allowing you to experiment, learn, and develop data pipelines and analytics solutions.

## Table of Contents

1. [Overview](#overview)
2. [Components](#components)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

This sandbox environment sets up a local ecosystem of data engineering tools, including:

- PostgreSQL for relational database storage
- MinIO for object storage (S3-compatible)
- Apache Spark for distributed data processing
- Apache Flink for stream processing
- Jupyter Notebooks for interactive data analysis and visualization

All services are containerized using Docker, making it easy to set up and tear down the entire environment.

## Components

- **PostgreSQL**: Relational database with sample data (Northwind dataset)
- **MinIO**: S3-compatible object storage
- **Apache Spark**: Distributed computing system with a master and worker node
- **Apache Flink**: Stream processing framework with a job manager and task manager
- **Jupyter Notebooks**: Web-based interactive development environment

## Prerequisites

- Docker
- Docker Compose
- Git (optional, for cloning the repository)

## Getting Started

1. Clone this repository (or download the ZIP file):
   ```
   git clone https://github.com/daniel-dqsdatalabs/data-engineering-sandbox.git
   cd data-engineering-sandbox
   ```

2. Create a `.env` file in the project root and add the following environment variables:
   ```
   POSTGRES_USER=your_postgres_username
   POSTGRES_PASSWORD=your_postgres_password
   MINIO_ROOT_USER=your_minio_root_user
   MINIO_ROOT_PASSWORD=your_minio_root_password
   ```

3. Build and start the containers:
   ```
   docker-compose up --build
   ```

4. Wait for all services to start up. This may take a few minutes on the first run.

## Usage

Once all services are up and running, you can access them through the following URLs:

- Jupyter Notebooks: http://localhost:8888
- Spark Master UI: http://localhost:8080
- Spark Worker UI: http://localhost:8082
- Flink JobManager UI: http://localhost:8081
- MinIO Console: http://localhost:9001

To connect to PostgreSQL:
- Host: localhost
- Port: 5432
- Database: northwind
- User: (as specified in .env file)
- Password: (as specified in .env file)

## Configuration

- PostgreSQL: The Northwind sample database is automatically loaded on first startup.
- MinIO: Configure using the MinIO Console or `mc` client.
- Spark & Flink: Additional configuration can be done by modifying the respective Dockerfiles and docker-compose.yml entries.
- Jupyter: Custom packages can be added by modifying the Jupyter Dockerfile.

## Troubleshooting

- If services fail to start, check the Docker logs:
  ```
  docker-compose logs [service_name]
  ```
- Ensure all required ports are free on your host machine.
- For PostgreSQL issues, check the init-db.sh script and ensure it has the correct permissions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open-source and available under the [MIT License](LICENSE).