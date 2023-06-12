import pytest
from fastapi import status
from starlette.testclient import TestClient

from api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_crawl_valid_process(client):
    numero = "0700442-69.2022.8.02.0050"
    response = client.post("/crawl", json={"numero": numero})

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "detail": f"A captura dos dados do processo {numero} foi iniciada. Ao finalizar os dados estarão disponíveis no endpoint /processo/{numero}."
    }


def test_crawl_invalid_number(client):
    numero = "0700442-69.2022.8.00.0050"
    response = client.post("/crawl", json={"numero": numero})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Nenhum crawler disponível" in response.json().get("detail")


def test_get_processo_not_found(client):
    numero = "0700442-69.2022.8.02.0010"
    response = client.get("/processo/{numero}")

    assert response.status_code == status.HTTP_200_OK
    assert "ainda não existe em nossa base de dados." in response.json().get("detail")
