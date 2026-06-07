from app.kafka.producer import publish_event


def process_webhook(payload):

    print(payload)

    if "pull_request" not in payload:
        return {
            "message": "Not a pull request event"
        }

    print("Pull request event detected")

    publish_event(payload)

    print("publish_event completed")
    ##send the data to kafka producer.py function

    return {
        "message": "Event queued successfully"
    }