from pydantic import BaseSettings


class Settings(BaseSettings):
    service_host: str = "127.0.0.1"
    service_port: int = 8000

    class Config:
        env_file = ".env"
