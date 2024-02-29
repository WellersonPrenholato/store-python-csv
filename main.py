from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, status, Response
from model import Produto
import uvicorn

app = FastAPI()

store = {
    "Produtos":
    [{
        "id": 1,
        "nome": "Tomate",
        "marca": "Hortifruti",
        "codigo": 555,
        "preco": 5.99,
        "quantidade": 10,
        "corredor": 12,
        "prateleira": 5
    },
    {
        "id": 2,
        "nome": "Arroz",
        "marca": "Sepe",
        "codigo": 324,
        "preco": 10.99,
        "quantidade": 3,
        "corredor": 3,
        "prateleira": 9
    },
    {
        "id": 3,
        "nome": "Feijao",
        "marca": "Carioca",
        "codigo": "1233",
        "preco": 13.99,
        "quantidade": 4,
        "corredor": 7,
        "prateleira": 10
    }]
}


@app.get('/store')
async def get_store():
    return store

@app.get('/store/{produto_cod}')
async def get_store_codigo(produto_cod: int):
    try:
        for item in store["Produtos"]:
            if str(item["codigo"]) == str(produto_cod):
                return item
        
        return {"message": f"Produto de código {produto_cod} não foi encontrado!"}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produto não encontrado!")


@app.post('/store', status_code=status.HTTP_201_CREATED)
async def post_store(produto: Produto):
    for item in store["Produtos"]:
        if str(produto.codigo) == str(item['codigo']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"O produto {produto.codigo} já existe na base de dados!")
    
    next_id = len(store['Produtos']) + 1
    produto_dict = produto.dict()
    produto_dict['id'] = next_id
    store['Produtos'].append(produto_dict)
    
    return f"Produto de código: {produto.codigo} foi registrado com sucesso!"

@app.put('/store/{produto_cod}')
async def put_store(produto_cod: int, produto: Produto):
    for item in store["Produtos"]:
        if produto_cod == item["codigo"]:
            produto.id = item["id"]
            item.update(produto.dict())
            return item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Não existe produto com o codigo {produto_cod}!")

@app.delete('/store/{produto_cod}')
async def delete_produto(produto_cod: int):
    for index, item in enumerate(store["Produtos"]):
        if item["codigo"] == produto_cod:
            del store["Produtos"][index]
            # Ainda falta inserir uma mensagem de "Produto deletado com sucesso!" no response da request.
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Não existe um produto com o código: {produto_cod}.")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, debug=True, reload=True)