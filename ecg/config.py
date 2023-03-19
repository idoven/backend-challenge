from pydantic import BaseSettings

from ecg import __version__


class Settings(BaseSettings):
    app_name: str = "Idoven ECG API"
    debug: bool = False
    version: str = __version__
    log_level: str = "INFO"

    # Database
    database_user: str = "postgres"
    database_host: str = "localhost"
    # TODO: make this a secret
    database_password: str = "password"
    database_name: str = "ecg"


settings = Settings()
