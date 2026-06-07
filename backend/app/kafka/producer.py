from confluent_kafka import Producer

##creates producer to acttually send the data from the github webhook to kafka server
import json

producer = Producer({
"bootstrap.servers": "localhost:9092"
})

##create producer object which connects to kafka server at port 9092

TOPIC = "github-pr-events"
##topic name like whatsap group to categoriese topics
def publish_event(payload):

    producer.produce(
        TOPIC,
        json.dumps(payload).encode("utf-8")
    )
    ##sent to kafka server,sent as json in utf-8



    producer.flush()
    ##flushed immediatesly to send immediately 
    ##instead of storing in server
    print("Event sent to Kafka")

