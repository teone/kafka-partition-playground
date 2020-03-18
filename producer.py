import json

from confluent_kafka import Producer
import sys

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Produces some kafka messages')
    parser.add_argument('--broker', dest='broker', default="localhost:9092",
                        help='The kafka broker')
    parser.add_argument('--topic', dest='topic', default="test_topic",
                        help='The kafka topic')
    parser.add_argument('--partition', dest='partition', default=4,
                        help='The number of partitions on which send the messages')

    args = parser.parse_args()
    print(args)

    broker = args.broker
    topic = args.topic

    # Producer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {
        'bootstrap.servers': broker,
        'partitioner': 'consistent'
    }

    # Create Producer instance
    p = Producer(**conf)


    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('Message "%s" delivered to %s on partition %d \n' %
                             (msg.value(), msg.topic(), msg.partition()))


    # Read lines from stdin, produce each line to Kafka
    partition = 0
    for line in range(0, 10):
        try:

            if partition == (int(args.partition) - 1):
                partition = 0
            else:
                partition = partition + 1

            p.produce(topic, json.dumps({"val": line, "partition": partition}), partition=partition, callback=delivery_callback)

        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                             len(p))

        # Serve delivery callback queue.
        # NOTE: Since produce() is an asynchronous API this poll() call
        #       will most likely not serve the delivery callback for the
        #       last produce()d message.
        p.poll(0)

    # Wait until all messages have been delivered
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush()