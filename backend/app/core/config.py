from pydantic_settings import BaseSettings

class Settings(BaseSettings):##used the BaseSettings allows us to work with environment variables

    DATABASE_URL: str

    GITHUB_TOKEN: str

    GITHUB_WEBHOOK_SECRET: str

    OPENAI_API_KEY: str

    class Config:
        env_file = ".env" ##looks for environment variables in the .env only not system environment variables

settings = Settings() ##later we can access the url as settings.DATABASE_URL and so on 