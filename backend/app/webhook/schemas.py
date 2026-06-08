from pydantic import BaseModel


class PullRequestUser(BaseModel):

    login: str


class PullRequestData(BaseModel):

    number: int

    user: PullRequestUser


class RepositoryData(BaseModel):

    full_name: str


class GithubWebhookSchema(BaseModel):

    action: str

    repository: RepositoryData

    pull_request: PullRequestData