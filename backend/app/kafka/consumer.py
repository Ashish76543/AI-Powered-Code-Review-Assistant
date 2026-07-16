from confluent_kafka import Consumer
from app.db.models.pull_request_file import PullRequestFile
import json
from app.services.diff_parser import extract_added_code

from app.services.ast_parser import analyze_python_code

from app.db.models.analysis_result import AnalysisResult
from app.db.session import SessionLocal
from app.db.models.pull_request import PullRequest

from app.utils.logger import logger
from app.services.retrieval_service import (
    retrieve_similar_code
)
from app.github.service import fetch_pr_data
from app.services.static_analysis import run_bandit
from app.db.models.static_issue import StaticIssue
from app.Orchastrator.graph import graph
from app.services.embedding_service import (
    generate_embedding
)

from app.services.faiss_service import (
    add_code_embedding
)
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

                existing_pr.status = action

                pr_record = existing_pr

                logger.info("Updated existing PR")

            else:

                pr = PullRequest(
                    repo_name=repo,
                    pr_number=pr_number,
                    author=author,
                    status=action
                )

                db.add(pr)

                db.flush()

                pr_record = pr

                logger.info("Created new PR")

            # Remove old file records for this PR
            db.query(PullRequestFile).filter(
                PullRequestFile.pull_request_id == pr_record.id
            ).delete()
            db.query(AnalysisResult).filter(
                AnalysisResult.pull_request_id == pr_record.id
            ).delete()
            db.query(StaticIssue).filter(
                StaticIssue.pull_request_id == pr_record.id
            ).delete()

            # Save current files from GitHub PR
            for file in pr_data["files"]:

                db_file = PullRequestFile(
                    pull_request_id=pr_record.id,
                    filename=file["filename"],
                    status=file["status"],
                    patch=file["patch"]
                )

                db.add(db_file)
                code = extract_added_code(
                    file.get("patch")
                )
                ## we call the patch to get the result

                if code.strip(): ## remove white space and check if empty

                    analysis = analyze_python_code(
                        code
                    )   ##if empty send for analysis

                    if analysis:
                            ##if analysis result got  add to the AnalysisResult model
                        result = AnalysisResult(
                            pull_request_id=pr_record.id,
                            filename=file["filename"],
                            functions=",".join(
                                analysis["functions"]
                            ), ##join based on commas into a string 
                            classes=",".join(
                                analysis["classes"]
                            ),
                            imports=",".join(
                                analysis["imports"]
                            ),
                            loops=analysis["loops"]
                        )

                        db.add(result)

                        logger.info(analysis)
                        issues = run_bandit(code)
                        logger.info(issues)
                        for issue in issues:

                            db_issue = StaticIssue(
                                pull_request_id=pr_record.id,
                                filename=file["filename"],
                                tool="bandit",
                                severity=issue.get(
                                    "issue_severity"
                                ),
                                message=issue.get(
                                    "issue_text"
                                ),
                                line_number=issue.get(
                                    "line_number"
                                )
                            )

                            db.add(db_issue)
                        embedding = generate_embedding(
                            code
                        )
                        similar_files=retrieve_similar_code(embedding)
                        add_code_embedding(
                            embedding,
                            file["filename"],code,pr_record.id
                        )
                        
                        logger.info(f"Similar files:{similar_files}")
                        state = {

                            "repo": repo,

                            "pr_number": pr_number,

                            "author": author,

                            "title": pr_data["title"],

                            "body": pr_data["body"],

                            "files": [

                                {

                                    "filename": file["filename"],

                                    "code": code,

                                    "analysis": analysis,

                                    "issues": issues,

                                    "similar_files": similar_files

                                }

                            ]

                        }

                        graph.invoke(state)

            db.commit()

            db.close()

        except Exception as e:

            logger.error(str(e))