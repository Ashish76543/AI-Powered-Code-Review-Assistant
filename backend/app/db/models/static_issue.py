from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class StaticIssue(Base):

    __tablename__ = "static_issues"

    id = Column(Integer, primary_key=True, index=True)

    pull_request_id = Column(Integer)

    filename = Column(String)

    tool = Column(String)

    severity = Column(String)

    message = Column(String)

    line_number = Column(Integer)