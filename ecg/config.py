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
    database_password: str = "password"
    database_name: str = "ecg"

    # JWT
    jwt_key: str = "secret"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.database_user}:"
            f"{self.database_password}@{self.database_host}"
            f"/{self.database_name}"
        )


settings = Settings()
