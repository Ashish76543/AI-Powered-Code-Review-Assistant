from app.kafka.producer import publish_event

from app.utils.logger import logger


def process_webhook(payload):

    if "pull_request" not in payload:

        logger.info("Ignored non-PR event")

        return {
            "message": "Not a pull request event"
        }

    publish_event(payload)

    logger.info("Event sent to Kafka")

    return {
        "message": "Event queued successfully"
    }