from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class PullRequestFile(Base):

    __tablename__ = "pull_request_files"

    id = Column(Integer, primary_key=True, index=True)

    pull_request_id = Column(
        Integer,
        ForeignKey("pull_requests.id")
    )

    filename = Column(String)

    status = Column(String)

    patch = Column(String)

    ##it is the actual code change made to the file 