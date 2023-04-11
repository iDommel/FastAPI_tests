import tempfile
import shutil
import os
import pytest
from fastapi.testclient import TestClient
from service import Service
from settings import Settings


@pytest.fixture(scope="module")
def audio_file():
    audio_bytes = b"\x00\x01\x02\x03"  # Replace with actual audio file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(audio_bytes)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture(scope="module")
def app_client():
    settings = Settings()
    service = Service(settings.service_host, settings.service_port)
    client = TestClient(service.app)
    yield client


def test_reverse_audio(audio_file, app_client):
    with open(audio_file, "rb") as f:
        response = app_client.post("/mp3", files={"audio_file": f})

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert (
        response.content == b"\x03\x02\x01\x00"
    )  # Replace with expected reversed audio bytes


def test_extract_audio_metadata(audio_file, app_client):
    with open(audio_file, "rb") as f:
        response = app_client.post("/pdf", files={"audio_file": f})

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    # Replace with assertion that checks the contents of the PDF file
