from fastapi.testclient import TestClient
from service import Service
from settings import Settings

settings = Settings()

service = Service(settings.service_host, settings.service_port)

client = TestClient(service.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
