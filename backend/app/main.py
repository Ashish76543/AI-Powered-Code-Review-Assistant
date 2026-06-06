from fastapi import FastAPI

from app.db.base_class import Base
from app.db.session import engine

from app.webhook.router import router

import app.db.base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
##connect a router ,so the app can also process the requests which goes to the router endpoint

@app.get("/")
def home():

    return {"message": "Backend running"}