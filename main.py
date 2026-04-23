import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os

from model import ProdutoCreate
from store_service import StoreService

# Carrega variáveis de ambiente
load_dotenv()

# Configuração via .env
CSV_FILENAME = os.getenv("CSV_FILENAME", "store.csv")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Configuração de logging
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

app = FastAPI(title="Store Python CSV", version="1.0.0")

# CORS - permite chamadas de qualquer origem (ajuste em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serviço de acesso ao CSV
store = StoreService(CSV_FILENAME)


@app.get('/store')
async def get_store():
    logger.info("GET /store - Listando todos os produtos")
    return store.listar_todos()


@app.get('/store/{produto_cod}')
async def get_store_codigo(produto_cod: int):
    logger.info("GET /store/%s - Buscando produto", produto_cod)
    produto = store.buscar_por_codigo(produto_cod)

    if produto is None:
        logger.warning("Produto codigo=%s não encontrado", produto_cod)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto de código {produto_cod} não foi encontrado!"
        )
    return produto


@app.post("/store", status_code=status.HTTP_201_CREATED)
async def post_store(produto: ProdutoCreate):
    logger.info("POST /store - Criando produto codigo=%s", produto.codigo)

    resultado = store.criar_produto(produto.model_dump())

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"O produto {produto.codigo} já existe na base de dados!"
        )
    return resultado


@app.put("/store/{produto_cod}", status_code=status.HTTP_200_OK)
async def put_store(produto_cod: int, produto: ProdutoCreate):
    logger.info("PUT /store/%s - Atualizando produto", produto_cod)

    resultado = store.atualizar_produto(produto_cod, produto.model_dump())

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe produto com o código {produto_cod}!"
        )
    return {"message": "Produto atualizado com sucesso", "produto": resultado}


@app.delete("/store/{produto_cod}", status_code=status.HTTP_200_OK)
async def delete_produto(produto_cod: int):
    logger.info("DELETE /store/%s - Deletando produto", produto_cod)

    if not store.deletar_produto(produto_cod):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um produto com o código: {produto_cod}."
        )
    return {"message": "Produto deletado com sucesso!", "codigo": produto_cod}


if __name__ == '__main__':
    logger.info("Iniciando servidor em %s:%d (debug=%s)", HOST, PORT, DEBUG)
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG)