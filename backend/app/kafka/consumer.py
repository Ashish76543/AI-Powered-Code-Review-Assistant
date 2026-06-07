from confluent_kafka import Consumer
import json


consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "pr-review-group",
    "auto.offset.reset": "earliest"
})

##create consumer object listening to port 9092 ,multiple consumers with same group id can be created to divide tasksk amongst


TOPIC = "github-pr-events"

consumer.subscribe([TOPIC])
##susbcribed to this topic,any data in topic will immediately be received

def consume_events():
    ##infinitely keep asking the kafka server (polling) ,wait maximum 1 second
    while True:

        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(msg.error())
            continue

        payload = json.loads(
            msg.value().decode("utf-8")  ##convert json to dictionary
        )

        print("Received Event:")
        print(payload)