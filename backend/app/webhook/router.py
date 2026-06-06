from fastapi import APIRouter, Request

from app.webhook.service import process_webhook

router = APIRouter()
##create a router for the webhook,webhook request got here
@router.post("/github/webhook")
async def github_webhook(req: Request):
    ##to get the payload from the request
    payload = await req.json()
    ##to process the payload
    ##returns the return from process_webhook in service.py for github
    return process_webhook(payload)