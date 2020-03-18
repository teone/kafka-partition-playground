# Kafka partitions examples

## Requirements

**Python libraries:**

```bash
pip install confluent_kafka
```

**Tools:**

[kafkacat](https://github.com/edenhill/kafkacat)

```bash
# debian
apt-get install kafkacat

# mac os
brew install kafkacat
```

[docker](https://www.docker.com)

[docker-compose](https://docs.docker.com/compose/)

## Run

Store you

Start kafka with an `PARTITION=4` number of partitions:

```bash
DOCKER_HOST_IP=<your-ip> PARTITION=4 docker-compose up -d
```

> If you're running on Mac you can use `DOCKER_HOST_IP=$(ipconfig getifaddr en0)  PARTITION=4 docker-compose up -d`

Listen on kafka:

```bash
kafkacat -b 127.0.0.1:9092 -G group1 test_topic
```

> NOTE that you can start multiple listeners to see how the messages are handled

Produce the events:

```bash
python producer.py --partition 4
```

## What next

Try to play around with multiple consumers, consumer groups 
and changing the `--partition` parameter to observe how `messages`
are distributed between consumers
