from langchain_openai import ChatOpenAI
from app.core.config import settings

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model="gpt-4.1-mini",
    temperature=0,
)

def get_llm():
    return llm