from src.service import Service
from src.settings import Settings
from functools import lru_cache


@lru_cache()
def get_settings():
    return Settings()


def main():
    settings = Settings()
    service = Service(settings.service_host, settings.service_port)

    service.run()


if __name__ == "__main__":
    main()
