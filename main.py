from src.service import Service
from src.settings import Settings


def main():
    settings = Settings()
    service = Service(settings.service_host, settings.service_port)

    service.run()


if __name__ == "__main__":
    main()
