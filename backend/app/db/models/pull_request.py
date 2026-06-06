from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

class PullRequest(Base):

    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)

    repo_name = Column(String)

    pr_number = Column(Integer)

    author = Column(String)