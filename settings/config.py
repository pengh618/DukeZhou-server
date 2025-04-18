import os
import typing
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CORS_ORIGINS: typing.List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List = ["*"]
    CORS_ALLOW_HEADERS: typing.List = ["*"]

    api_key: typing.Text = os.getenv("OPENAI_API_KEY")
    openrouter_key: typing.Text = os.getenv("OPENROUTER_API_KEY")

settings = Settings()