from sqlalchemy import create_engine
##this is used to connect to the database
from sqlalchemy.orm import sessionmaker
##used to create the session,each converstaion is a session,we start and the  end it

from app.core.config import settings
##import the settings class from config to access the environment variables
engine = create_engine(settings.DATABASE_URL)
##create the engine to connetc to database

SessionLocal = sessionmaker(
    autocommit=False,   ##cannot autocommit,we have to commit manually
    autoflush=False,   ##cannot autoflush,we have to flush manually
    bind=engine   ##bind the engine to the session
)

##session creation