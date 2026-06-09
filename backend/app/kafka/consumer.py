from confluent_kafka import Consumer

import json

from app.db.session import SessionLocal
from app.db.models.pull_request import PullRequest

from app.utils.logger import logger

from app.github.service import fetch_pr_data ##to call the github api


consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "pr-review-group",
    "auto.offset.reset": "earliest"
})


TOPIC = "github-pr-events"

consumer.subscribe([TOPIC])


def consume_events():

    while True:

        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():

            logger.error(msg.error())

            continue

        payload = json.loads(
            msg.value().decode("utf-8")
        )

        try:

            action = payload["action"]

            repo = payload["repository"]["full_name"]

            pr_number = payload["pull_request"]["number"]

            author = payload["pull_request"]["user"]["login"]

            pr_data = fetch_pr_data(
                repo,
                pr_number
            )

            logger.info(pr_data)

            db = SessionLocal()

            existing_pr = db.query(PullRequest).filter(
                PullRequest.repo_name == repo,
                PullRequest.pr_number == pr_number
            ).first()

            if existing_pr:

                existing_pr.status = action  ##if the pr already exisys,we update inly the status

                logger.info("Updated existing PR")

            else:

                pr = PullRequest(
                    repo_name=repo,
                    pr_number=pr_number,
                    author=author,
                    status=action
                )

                db.add(pr)

                logger.info("Created new PR")

            db.commit()

            db.close()

        except Exception as e:

            logger.error(str(e))