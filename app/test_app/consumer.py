from confluent_kafka import Consumer, KafkaException, KafkaError

# Kafka configuration
KAFKA_CONF = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'my-consumer-group',        # Consumer group ID
    # Start from the beginning if no offset is committed
    'auto.offset.reset': 'earliest'
}

# Initialize Kafka consumer
consumer = Consumer(KAFKA_CONF)
topic = 'test_topic'

# Subscribe to the topic
consumer.subscribe([topic])


def consume_messages():
    """Consume messages from Kafka topic."""
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Adjust timeout as needed

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition reached
                    continue
                else:
                    # Other errors
                    raise KafkaException(msg.error())

            # Successfully received message
            print(f"Received message: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        # Handle script termination
        print("Consumer stopped.")
    finally:
        # Clean up and close the consumer
        consumer.close()


if __name__ == "__main__":
    consume_messages()
