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
    response = client.post("/processo", json={"numero": numero})

    assert response.status_code == status.HTTP_200_OK

    output_data = response.json()
    processos_1_grau = output_data.get("1 Grau", [])
    processos_2_grau = output_data.get("2 Grau", [])

    assert len(processos_1_grau) == 1
    assert len(processos_2_grau) == 1

    assert processos_1_grau[0].get("numero") == numero
    assert processos_1_grau[0].get("data_distribuicao") == "2022-05-12 00:00:00"
    assert processos_1_grau[0].get("classe") == "Procedimento Comum Cível"
    assert processos_1_grau[0].get("instancia") == "1 Grau"

    assert processos_2_grau[0].get("numero") == numero
    assert processos_2_grau[0].get("classe") == "Apelação Cível"
    assert processos_2_grau[0].get("instancia") == "2 Grau"


def test_crawl_invalid_number(client):
    numero = "0700442-69.2022.8.00.0050"
    response = client.post("/processo", json={"numero": numero})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Nenhum crawler disponível" in response.json().get("detail")


def test_crawl_processo_segredo(client):
    numero = "0050350-83.2020.8.06.0119"
    response = client.post("/processo", json={"numero": numero})

    assert response.status_code == status.HTTP_200_OK
    assert "encontra em segredo de justiça" in response.json().get("detail")


def test_crawl_processo_not_found(client):
    numero = "0700442-69.2022.8.02.0010"
    response = client.post("/processo", json={"numero": numero})

    assert response.status_code == status.HTTP_200_OK
    assert "Nenhuma informação foi encontrada" in response.json().get("detail")
