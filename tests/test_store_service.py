import os
import pytest
import pandas as pd
from store_service import StoreService, CSV_COLUMNS

CSV_TEST = "test_store_service.csv"


@pytest.fixture(autouse=True)
def csv_limpo():
    """Cria um CSV limpo antes de cada teste e remove depois."""
    df = pd.DataFrame([
        {"id": 1, "nome": "Arroz", "marca": "Sepe", "codigo": 324, "preco": 10.99, "quantidade": 3, "corredor": 3, "prateleira": 9},
        {"id": 2, "nome": "Feijao", "marca": "Preto", "codigo": 222, "preco": 7.99, "quantidade": 5, "corredor": 12, "prateleira": 6},
    ])
    df.to_csv(CSV_TEST, index=False)
    yield
    if os.path.exists(CSV_TEST):
        os.remove(CSV_TEST)


@pytest.fixture
def service():
    return StoreService(CSV_TEST)


@pytest.fixture
def service_vazio():
    """Serviço apontando para CSV inexistente."""
    path = "test_vazio.csv"
    yield StoreService(path)
    if os.path.exists(path):
        os.remove(path)


# ===================== LISTAR =====================

class TestListarTodos:
    def test_retorna_lista(self, service):
        resultado = service.listar_todos()
        assert isinstance(resultado, list)
        assert len(resultado) == 2

    def test_csv_vazio_retorna_lista_vazia(self, service_vazio):
        resultado = service_vazio.listar_todos()
        assert resultado == []

    def test_campos_presentes(self, service):
        produto = service.listar_todos()[0]
        for col in CSV_COLUMNS:
            assert col in produto


# ===================== BUSCAR POR CÓDIGO =====================

class TestBuscarPorCodigo:
    def test_encontra_produto_existente(self, service):
        produto = service.buscar_por_codigo(324)
        assert produto is not None
        assert produto["nome"] == "Arroz"

    def test_retorna_none_para_codigo_inexistente(self, service):
        assert service.buscar_por_codigo(9999) is None

    def test_retorna_none_csv_vazio(self, service_vazio):
        assert service_vazio.buscar_por_codigo(324) is None


# ===================== CRIAR =====================

class TestCriarProduto:
    def test_cria_produto_novo(self, service):
        novo = {
            "nome": "Macarrao", "marca": "Barilla", "codigo": 789,
            "preco": 8.50, "quantidade": 7, "corredor": 4, "prateleira": 6
        }
        resultado = service.criar_produto(novo)
        assert resultado is not None
        assert resultado["id"] == 3
        assert resultado["codigo"] == 789

    def test_rejeita_codigo_duplicado(self, service):
        duplicado = {
            "nome": "Arroz Integral", "marca": "Sepe", "codigo": 324,
            "preco": 12.00, "quantidade": 1, "corredor": 3, "prateleira": 9
        }
        assert service.criar_produto(duplicado) is None

    def test_cria_no_csv_vazio(self, service_vazio):
        novo = {
            "nome": "Azeite", "marca": "Gallo", "codigo": 1010,
            "preco": 20.90, "quantidade": 2, "corredor": 1, "prateleira": 2
        }
        resultado = service_vazio.criar_produto(novo)
        assert resultado is not None
        assert resultado["id"] == 1

    def test_persiste_no_csv(self, service):
        novo = {
            "nome": "Sal", "marca": "Cisne", "codigo": 555,
            "preco": 3.50, "quantidade": 10, "corredor": 2, "prateleira": 1
        }
        service.criar_produto(novo)
        # Lê novamente do disco
        todos = service.listar_todos()
        assert len(todos) == 3
        codigos = [p["codigo"] for p in todos]
        assert 555 in codigos


# ===================== ATUALIZAR =====================

class TestAtualizarProduto:
    def test_atualiza_produto_existente(self, service):
        dados = {
            "nome": "Arroz Integral", "marca": "Sepe", "codigo": 324,
            "preco": 14.99, "quantidade": 10, "corredor": 3, "prateleira": 9
        }
        resultado = service.atualizar_produto(324, dados)
        assert resultado is not None
        assert resultado["preco"] == 14.99
        assert resultado["nome"] == "Arroz Integral"
        assert resultado["id"] == 1  # preserva o ID original

    def test_retorna_none_codigo_inexistente(self, service):
        dados = {
            "nome": "X", "marca": "X", "codigo": 9999,
            "preco": 1.0, "quantidade": 1, "corredor": 1, "prateleira": 1
        }
        assert service.atualizar_produto(9999, dados) is None

    def test_retorna_none_csv_vazio(self, service_vazio):
        dados = {
            "nome": "X", "marca": "X", "codigo": 1,
            "preco": 1.0, "quantidade": 1, "corredor": 1, "prateleira": 1
        }
        assert service_vazio.atualizar_produto(1, dados) is None

    def test_persiste_atualizacao(self, service):
        dados = {
            "nome": "Feijao Carioca", "marca": "Carioca", "codigo": 222,
            "preco": 9.99, "quantidade": 8, "corredor": 12, "prateleira": 6
        }
        service.atualizar_produto(222, dados)
        produto = service.buscar_por_codigo(222)
        assert produto["nome"] == "Feijao Carioca"


# ===================== DELETAR =====================

class TestDeletarProduto:
    def test_deleta_produto_existente(self, service):
        assert service.deletar_produto(324) is True
        assert len(service.listar_todos()) == 1

    def test_retorna_false_codigo_inexistente(self, service):
        assert service.deletar_produto(9999) is False

    def test_retorna_false_csv_vazio(self, service_vazio):
        assert service_vazio.deletar_produto(324) is False

    def test_nao_afeta_outros_produtos(self, service):
        service.deletar_produto(324)
        restante = service.listar_todos()
        assert len(restante) == 1
        assert restante[0]["codigo"] == 222
