#!/usr/bin/env python3
"""
Kafka Data Stream Producer using Faker to generate synthetic data
"""

import json
import os
import random
import time
from datetime import datetime
from typing import Any, Dict

from dotenv import load_dotenv
from faker import Faker
from kafka import KafkaProducer
from loguru import logger

# Load environment variables
load_dotenv()

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_USERS = "users"
TOPIC_TRANSACTIONS = "transactions"
TOPIC_PRODUCTS = "products"
SLEEP_TIME = random.uniform(1, 60)  # random seconds between messages (1s to 60s)

# Initialize Faker and Kafka producer
fake = Faker()
logger.info(f"Connecting to Kafka 4.0 at {KAFKA_BOOTSTRAP_SERVERS}")

# Wait for Kafka to be ready
max_retries = 15
retry_delay = 10
for retry in range(max_retries):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
            # Kafka 4.0 specific configs
            acks="all",
            compression_type="snappy",
            batch_size=16384,
            linger_ms=100,
            max_in_flight_requests_per_connection=5,
            retry_backoff_ms=500,
            request_timeout_ms=30000,
        )
        logger.info("Successfully connected to Kafka 4.0")
        break
    except Exception as e:
        if retry < max_retries - 1:
            logger.warning(
                f"Failed to connect to Kafka, retrying in {retry_delay}s... ({e})"
            )
            time.sleep(retry_delay)
        else:
            logger.error(
                f"Failed to connect to Kafka after {max_retries} attempts: {e}"
            )
            raise


# Data generation functions
def generate_user() -> Dict[str, Any]:
    """Generate fake user data"""
    return {
        "id": fake.uuid4(),
        "username": fake.user_name(),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": fake.phone_number(),
        "created_at": datetime.now().isoformat(),
    }


def generate_product() -> Dict[str, Any]:
    """Generate fake product data"""
    return {
        "id": fake.uuid4(),
        "name": fake.catch_phrase(),
        "description": fake.text(max_nb_chars=200),
        "price": round(random.uniform(10, 1000), 2),
        "category": random.choice(
            ["Electronics", "Clothing", "Books", "Home", "Beauty"]
        ),
        "in_stock": random.choice([True, False]),
        "created_at": datetime.now().isoformat(),
    }


def generate_transaction() -> Dict[str, Any]:
    """Generate fake transaction data"""
    return {
        "id": fake.uuid4(),
        "user_id": fake.uuid4(),
        "product_id": fake.uuid4(),
        "quantity": random.randint(1, 10),
        "price": round(random.uniform(10, 1000), 2),
        "total": round(random.uniform(10, 5000), 2),
        "payment_method": random.choice(
            ["Credit Card", "PayPal", "Apple Pay", "Google Pay"]
        ),
        "status": random.choice(["Completed", "Pending", "Failed", "Refunded"]),
        "created_at": datetime.now().isoformat(),
    }


# Ensure topics exist with the new consumer protocol format
def create_topics():
    """Create topics if they don't exist"""
    from kafka.admin import KafkaAdminClient, NewTopic

    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id="producer-admin",
        )

        # Get existing topics
        existing_topics = admin_client.list_topics()
        topics_to_create = []

        # Check which topics need to be created
        for topic in [TOPIC_USERS, TOPIC_PRODUCTS, TOPIC_TRANSACTIONS]:
            if topic not in existing_topics:
                topics_to_create.append(
                    NewTopic(
                        name=topic,
                        num_partitions=3,
                        replication_factor=1,
                        # Topic configs for improved performance with Kafka 4.0
                        topic_configs={
                            "cleanup.policy": "delete",
                            "retention.ms": "604800000",  # 7 days
                            "segment.bytes": "1073741824",  # 1GB
                            "min.insync.replicas": "1",
                        },
                    )
                )

        if topics_to_create:
            admin_client.create_topics(topics_to_create)
            logger.info(f"Created topics: {[t.name for t in topics_to_create]}")
        else:
            logger.info("All required topics already exist")

        admin_client.close()
    except Exception as e:
        logger.error(f"Error creating topics: {e}")
        # Continue execution even if topic creation fails
        # The producer will auto-create topics if they don't exist


# Send data to Kafka
def send_data():
    """Generate and send data to Kafka topics"""
    try:
        # First try to create topics with proper configurations
        create_topics()
    except Exception as e:
        logger.warning(f"Failed to pre-create topics, will rely on auto-creation: {e}")

    count = 0
    while True:
        try:
            # Send user data
            user = generate_user()
            producer.send(TOPIC_USERS, key=user["id"], value=user)

            # Send product data
            product = generate_product()
            producer.send(TOPIC_PRODUCTS, key=product["id"], value=product)

            # Send transaction data
            transaction = generate_transaction()
            producer.send(TOPIC_TRANSACTIONS, key=transaction["id"], value=transaction)

            count += 3
            if count % 30 == 0:
                logger.info(f"Sent {count} messages so far")
            else:
                logger.debug(
                    f"Sent user: {user['id']}, product: {product['id']}, transaction: {transaction['id']}"
                )

            # Flush to ensure all messages are sent
            producer.flush()
            time.sleep(SLEEP_TIME)

        except Exception as e:
            logger.error(f"Error sending data: {e}")
            time.sleep(5)  # Wait before retrying


if __name__ == "__main__":
    logger.info("Starting Kafka 4.0 data stream producer")
    try:
        send_data()
    except KeyboardInterrupt:
        logger.info("Stopping producer")
    finally:
        if "producer" in locals():
            producer.close()
