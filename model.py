from pydantic import BaseModel
from typing import Optional

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: str | None = None
    codigo: int
    preco: float | None = None
    quantidade: int | None = None
    corredor: str | None = None
    prateleira: str | None = None