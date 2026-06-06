from app.db.session import SessionLocal
##to create the session for model
from app.db.models.pull_request import PullRequest
## to create Pull Request object for adding to model

def process_webhook(payload):

    repo = payload["repository"]["full_name"]

    pr_number = payload["pull_request"]["number"]

    author = payload["pull_request"]["user"]["login"]
    ##to get data from json payload

    db = SessionLocal()
    ##to create the session for model
    pr = PullRequest(
        repo_name=repo,
        pr_number=pr_number,
        author=author
    )
    ##to create the Pull Request object for adding to model

    db.add(pr)
     ##to add the Pull Request object to the session
    db.commit()
    #to commit the changes to the database
    db.close()
    ##to close the session
    return {
        "message": "PR saved"
    }
    ##to return the message that the PR is saved