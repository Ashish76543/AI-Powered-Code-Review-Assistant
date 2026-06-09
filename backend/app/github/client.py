from github import Github

from app.core.config import settings


# Create GitHub client using personal access token

github_client = Github(settings.GITHUB_TOKEN)


def get_repository(repo_name: str):
    """
    Fetch a GitHub repository object.

    Example repo_name:
    "openai/openai-python"
    """
    
    return github_client.get_repo(repo_name)


def get_pull_request(repo_name: str, pr_number: int):
    """
    Fetch a specific pull request from a repository.
    """

    repo = get_repository(repo_name)

    return repo.get_pull(pr_number)