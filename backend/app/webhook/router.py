from fastapi import APIRouter

from app.webhook.schemas import GithubWebhookSchema
from app.webhook.service import process_webhook


router = APIRouter()


@router.post("/github/webhook")
async def github_webhook(payload: GithubWebhookSchema):

    return process_webhook(payload.model_dump())