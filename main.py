from typing import List, Optional
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException, status, Response

from model import Produto

import uvicorn

app = FastAPI()

store = {
    
    1: {
        "nome": "Tomate",
        "marca": "Hortifruti",
        "codigo": "555",
        "preco": 5.99,
        "quantidade": 10,
        "corredor": 12,
        "prateleira": 5
    },
    
    2: {
        "nome": "Arroz",
        "marca": "Sepe",
        "codigo": "324",
        "preco": 10.99,
        "quantidade": 3,
        "corredor": 3,
        "prateleira": 9
    }
}

# TO DO: converter a estrutura para o JSON ABAIXO:
# store = {
#     "loja": [
#     {
#         "id": 1,
#         "nome": "teste1"
#     },
#     {
#         "id": 2,
#         "nome": "teste2"
#     }
#     ]
# }

@app.get('/store')
async def get_store():
    return store

@app.get('/store/{produto_id}')
async def get_store(produto_id: int):
    try:
        produto = store[produto_id]
        return produto
    except KeyError:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Curso não encontrado!")

# TO DO: Pesquisar se o produto já existe, para nao criar outro.
@app.post('/store', status_code=status.HTTP_201_CREATED)
async def post_store(produto: Produto):
    next_id: int = len(store) + 1
    
    # if produto.id not in store:
    produto.id = next_id
    store[next_id] = produto
    
    return store
    # else:
    #     raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail="Já existe um curso com o ID: {curso.id}.")

@app.put('/store/{produto_id}')
async def put_store(produto_id: int, produto: Produto):
    
    if produto_id in store:
        produto.id = produto_id
        store[produto_id] = produto
        return produto
    
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Não existe produto com o id {produto_id}!")

@app.delete('/store/{produto_id}')
async def delete_produto(produto_id: int):
    if produto_id in store:
        del store[produto_id]
        # return JSONResponse(status_code = status.HTTP_204_NO_CONTENT)
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Não existe um curso com o ID: {curso.id}.")
        

if __name__ == '__main__':
    
    uvicorn.run("main:app", host='0.0.0.0', port=8000, debug=True, reload=True)