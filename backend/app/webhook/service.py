from app.db.session import SessionLocal
from app.db.models.pull_request import PullRequest

def process_webhook(payload):

    print(payload)

    if "pull_request" not in payload:

        return {
            "message": "Not a pull request event"
        }

    repo = payload["repository"]["full_name"]

    pr_number = payload["pull_request"]["number"]

    author = payload["pull_request"]["user"]["login"]

    db = SessionLocal()

    pr = PullRequest(
        repo_name=repo,
        pr_number=pr_number,
        author=author
    )

    db.add(pr)

    db.commit()

    db.close()

    return {
        "message": "PR saved"
    }