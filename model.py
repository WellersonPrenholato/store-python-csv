from pydantic import BaseModel, Field
from typing import Optional


class ProdutoCreate(BaseModel):
    """Modelo para criação/atualização de produto (sem id)."""
    nome: str = Field(..., min_length=1, max_length=100)
    marca: str = Field(..., min_length=1, max_length=100)
    codigo: int = Field(..., gt=0)
    preco: float = Field(..., gt=0)
    quantidade: int = Field(..., ge=0)
    corredor: int = Field(..., gt=0)
    prateleira: int = Field(..., gt=0)


class Produto(ProdutoCreate):
    """Modelo completo do produto (com id)."""
    id: Optional[int] = None