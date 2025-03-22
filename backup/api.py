from fastapi import FastAPI, HTTPException
# from main import delete_item, list_items_all, list_item_id, create_item, delete_item

from model import Item

from produto import Produto
from store import Store

app = FastAPI()

# @app.get("/")
# def get_items_all():
#     return list_items_all()

# @app.get("/items/{item_id}")
# def get_item_id(item_id: Item):
#     return list_item_id()

# @app.post("/send_item")
@app.post("/")
async def post_item(item: Item):
    produto = Produto(Item(item.nome, None, None))
    
    produto.marca = item.marca
    produto.codigo = item.codigo
    produto.preco = item.preco
    produto.quantidade = item.quantidade
    produto.corredor = item.corredor
    produto.prateleira = item.prateleira
    
    success = produto.create_item(produto)
    if success:
        return Item(
            nome=produto.nome,
            marca=produto.marca,
            codigo=produto.codigo,
            preco=produto.preco,
            quantidade=produto.quantidade,
            corredor=produto.corredor,
            prateleira=produto.prateleira,
            id=1  # Você pode definir um ID apropriado aqui
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create item")
    # return produto.create_item(item)

# Teste
# @app.get("/items/{item_id}")
# def get_item_id():
#     return list_item_id()

# @app.delete("/items/{item_id}")
# async def del_item(codigo: int):
#     return delete_item(codigo)
