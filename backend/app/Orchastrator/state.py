from typing import TypedDict


class FileState(TypedDict):
    filename: str
    status: str
    patch: str
    code: str
    analysis: dict
    issues: list
    similar_files: list




class ReviewState(TypedDict):
    repo: str
    pr_number: int
    author: str
    title: str
    body: str

    files: list[FileState]

    code_review: str
    security_review: str
    performance_review: str

    final_review: str

    risk: str