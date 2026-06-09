from app.github.client import get_pull_request


def fetch_pr_data(repo_name: str, pr_number: int):

    # Fetch pull request object
    pr = get_pull_request(
        repo_name,
        pr_number
    )

    files = []

    # Loop through changed files in the PR
    for file in pr.get_files():
        ##for each updated file
        files.append({
            "filename": file.filename,  ##the actual file path
            "status": file.status,      ##the current file status
            "patch": file.patch         ##the actual modified changes
        })

    # Return structured PR data
    return {
        "title": pr.title,
        "body": pr.body,
        "author": pr.user.login,
        "files": files  ## we return everything
    }