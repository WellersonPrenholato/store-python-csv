import pytest
from pydantic import ValidationError
from model import ProdutoCreate, Produto


class TestProdutoCreate:
    """Testes de validação do modelo ProdutoCreate."""

    def test_produto_valido(self):
        p = ProdutoCreate(
            nome="Arroz", marca="Sepe", codigo=324,
            preco=10.99, quantidade=3, corredor=3, prateleira=9
        )
        assert p.nome == "Arroz"
        assert p.codigo == 324

    def test_nome_vazio_invalido(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="", marca="Sepe", codigo=324,
                preco=10.99, quantidade=3, corredor=3, prateleira=9
            )

    def test_nome_longo_invalido(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="A" * 101, marca="Sepe", codigo=324,
                preco=10.99, quantidade=3, corredor=3, prateleira=9
            )

    def test_codigo_zero_invalido(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="Arroz", marca="Sepe", codigo=0,
                preco=10.99, quantidade=3, corredor=3, prateleira=9
            )

    def test_codigo_negativo_invalido(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="Arroz", marca="Sepe", codigo=-1,
                preco=10.99, quantidade=3, corredor=3, prateleira=9
            )

    def test_preco_zero_invalido(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="Arroz", marca="Sepe", codigo=324,
                preco=0, quantidade=3, corredor=3, prateleira=9
            )

    def test_preco_negativo_invalido(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="Arroz", marca="Sepe", codigo=324,
                preco=-5.0, quantidade=3, corredor=3, prateleira=9
            )

    def test_quantidade_zero_valido(self):
        p = ProdutoCreate(
            nome="Arroz", marca="Sepe", codigo=324,
            preco=10.99, quantidade=0, corredor=3, prateleira=9
        )
        assert p.quantidade == 0

    def test_quantidade_negativa_invalida(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="Arroz", marca="Sepe", codigo=324,
                preco=10.99, quantidade=-1, corredor=3, prateleira=9
            )

    def test_marca_vazia_invalida(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(
                nome="Arroz", marca="", codigo=324,
                preco=10.99, quantidade=3, corredor=3, prateleira=9
            )

    def test_campo_faltando_invalido(self):
        with pytest.raises(ValidationError):
            ProdutoCreate(nome="Arroz", codigo=324)


class TestProduto:
    """Testes do modelo completo Produto (com id)."""

    def test_id_opcional(self):
        p = Produto(
            nome="Arroz", marca="Sepe", codigo=324,
            preco=10.99, quantidade=3, corredor=3, prateleira=9
        )
        assert p.id is None

    def test_id_definido(self):
        p = Produto(
            id=1, nome="Arroz", marca="Sepe", codigo=324,
            preco=10.99, quantidade=3, corredor=3, prateleira=9
        )
        assert p.id == 1

    def test_model_dump(self):
        p = ProdutoCreate(
            nome="Arroz", marca="Sepe", codigo=324,
            preco=10.99, quantidade=3, corredor=3, prateleira=9
        )
        d = p.model_dump()
        assert isinstance(d, dict)
        assert d["nome"] == "Arroz"
        assert "id" not in d
