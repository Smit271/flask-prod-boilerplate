from confluent_kafka import Producer
import json

# Kafka configuration
KAFKA_CONF = {
    # Update if your Kafka server is different
    'bootstrap.servers': 'localhost:9092',
}

# Initialize Kafka producer
producer = Producer(KAFKA_CONF)


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def produce_message(topic, message):
    """Produce a message to the Kafka topic."""
    # Serialize the message to JSON
    message_json = json.dumps(message)

    # Produce the message to Kafka
    producer.produce(topic, key=None, value=message_json,
                     callback=delivery_report)

    # Wait up to 1 second for events to be processed
    producer.flush(timeout=10)


if __name__ == "__main__":
    topic = 'test_topic'
    message = {"key": "value"}

    # Produce a single message
    produce_message(topic, message)
