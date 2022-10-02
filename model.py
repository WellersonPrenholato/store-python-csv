from pydantic import BaseModel

class Item(BaseModel):
    nome: str
    marca: str | None = None
    codigo: int
    preco: float | None = None
    quantidade: int | None = None
    corredor: int | None = None
    prateleira: int | None = None