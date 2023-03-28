import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PREFIX: str = os.environ.get('API_PREFIX', '/api/v1')
    PROJECT_NAME: str = os.environ.get('PROJECT_NAME', 'fastapiproject')
    OPENAPI_URL: str = os.environ.get('OPENAPI_URL', '/openapi.json')  # If empty this service won't expose docs
    API_PORT: int = int(os.environ.get('API_PORT', '5000'))


settings = Settings()
