from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class AnalysisResult(Base):

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True)

    pull_request_id = Column(Integer)

    filename = Column(String)

    functions = Column(String)

    classes = Column(String)

    imports = Column(String)

    loops = Column(Integer)