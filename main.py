from typing import List, Optional
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException, status

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

@app.get('/store')
async def get_store():
    return store

@app.get('/store/{produto_id}')
async def get_store(produto_id: int):
    try:
        produto = store[produto_id]
        return produto
    except KeyError:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND, details='Curso não encontrado!')


# @app.delete('/store/{produto_id}')
# async def delete_produto(produto_id: int):
        

if __name__ == '__main__':
    
    uvicorn.run("main:app", host='0.0.0.0', port=8000, debug=True, reload=True)