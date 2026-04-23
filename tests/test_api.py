import os
import pytest
from fastapi.testclient import TestClient

# Força CSV de teste antes de importar o app
os.environ["CSV_FILENAME"] = "test_api.csv"

import pandas as pd
from main import app, store


@pytest.fixture(autouse=True)
def csv_limpo():
    """Reseta o CSV de teste antes de cada teste."""
    csv_path = "test_api.csv"
    df = pd.DataFrame([
        {"id": 1, "nome": "Arroz", "marca": "Sepe", "codigo": 324, "preco": 10.99, "quantidade": 3, "corredor": 3, "prateleira": 9},
        {"id": 2, "nome": "Feijao", "marca": "Preto", "codigo": 222, "preco": 7.99, "quantidade": 5, "corredor": 12, "prateleira": 6},
    ])
    df.to_csv(csv_path, index=False)
    store.csv_path = csv_path
    yield
    if os.path.exists(csv_path):
        os.remove(csv_path)


@pytest.fixture
def client():
    return TestClient(app)


PRODUTO_VALIDO = {
    "nome": "Macarrao",
    "marca": "Barilla",
    "codigo": 789,
    "preco": 8.50,
    "quantidade": 7,
    "corredor": 4,
    "prateleira": 6,
}


# ===================== GET /store =====================

class TestGetStore:
    def test_lista_todos_retorna_200(self, client):
        resp = client.get("/store")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        assert len(resp.json()) == 2

    def test_campos_do_produto(self, client):
        resp = client.get("/store")
        produto = resp.json()[0]
        assert "id" in produto
        assert "nome" in produto
        assert "codigo" in produto


# ===================== GET /store/{codigo} =====================

class TestGetStoreCodigo:
    def test_busca_existente_retorna_200(self, client):
        resp = client.get("/store/324")
        assert resp.status_code == 200
        assert resp.json()["nome"] == "Arroz"

    def test_busca_inexistente_retorna_404(self, client):
        resp = client.get("/store/9999")
        assert resp.status_code == 404

    def test_codigo_invalido_retorna_422(self, client):
        resp = client.get("/store/abc")
        assert resp.status_code == 422


# ===================== POST /store =====================

class TestPostStore:
    def test_cria_produto_retorna_201(self, client):
        resp = client.post("/store", json=PRODUTO_VALIDO)
        assert resp.status_code == 201
        assert resp.json()["codigo"] == 789
        assert "id" in resp.json()

    def test_duplicado_retorna_409(self, client):
        produto_dup = {**PRODUTO_VALIDO, "codigo": 324}
        resp = client.post("/store", json=produto_dup)
        assert resp.status_code == 409

    def test_campo_obrigatorio_faltando_retorna_422(self, client):
        incompleto = {"nome": "Sal", "codigo": 100}
        resp = client.post("/store", json=incompleto)
        assert resp.status_code == 422

    def test_preco_negativo_retorna_422(self, client):
        invalido = {**PRODUTO_VALIDO, "preco": -5.0}
        resp = client.post("/store", json=invalido)
        assert resp.status_code == 422

    def test_nome_vazio_retorna_422(self, client):
        invalido = {**PRODUTO_VALIDO, "nome": ""}
        resp = client.post("/store", json=invalido)
        assert resp.status_code == 422

    def test_codigo_zero_retorna_422(self, client):
        invalido = {**PRODUTO_VALIDO, "codigo": 0}
        resp = client.post("/store", json=invalido)
        assert resp.status_code == 422


# ===================== PUT /store/{codigo} =====================

class TestPutStore:
    def test_atualiza_retorna_200(self, client):
        dados = {**PRODUTO_VALIDO, "codigo": 324, "nome": "Arroz Integral", "preco": 14.99}
        resp = client.put("/store/324", json=dados)
        assert resp.status_code == 200
        assert resp.json()["produto"]["nome"] == "Arroz Integral"

    def test_inexistente_retorna_404(self, client):
        resp = client.put("/store/9999", json=PRODUTO_VALIDO)
        assert resp.status_code == 404

    def test_persiste_atualizacao(self, client):
        dados = {**PRODUTO_VALIDO, "codigo": 324, "nome": "Arroz Premium"}
        client.put("/store/324", json=dados)
        resp = client.get("/store/324")
        assert resp.json()["nome"] == "Arroz Premium"


# ===================== DELETE /store/{codigo} =====================

class TestDeleteStore:
    def test_deleta_retorna_200(self, client):
        resp = client.delete("/store/324")
        assert resp.status_code == 200
        assert "deletado" in resp.json()["message"].lower()

    def test_inexistente_retorna_404(self, client):
        resp = client.delete("/store/9999")
        assert resp.status_code == 404

    def test_deleta_remove_do_csv(self, client):
        client.delete("/store/324")
        resp = client.get("/store/324")
        assert resp.status_code == 404

    def test_deleta_nao_afeta_outros(self, client):
        client.delete("/store/324")
        resp = client.get("/store")
        assert len(resp.json()) == 1
        assert resp.json()[0]["codigo"] == 222
