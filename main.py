import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import pandas as pd
import logging
import os

# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Nome do arquivo CSV
csv_filename = "store.csv"

def ler_produtos_csv() -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_filename)
        # logger.debug("CSV carregado com sucesso: %s", df)
        return df
    except FileNotFoundError:
        logger.debug("Arquivo CSV não encontrado, criando DataFrame vazio")
        return pd.DataFrame(columns=['id', 'nome', 'marca', 'codigo', 'preco', 'quantidade', 'corredor', 'prateleira'])
    except Exception as e:
        logger.error("Erro ao ler o CSV: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao ler o CSV: {str(e)}")

# Função para salvar o CSV
def salvar_produtos_csv(df: pd.DataFrame):
    try:
        # logger.debug("Tentando salvar DataFrame: %s", df)
        df.to_csv(csv_filename, index=False)
        logger.debug("CSV salvo com sucesso!")
    except Exception as e:
        logger.error("Erro ao salvar o CSV: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o CSV: {str(e)}")

# Modelo do Produto
class Produto(BaseModel):
    nome: str
    marca: str
    codigo: int
    preco: float
    quantidade: int
    corredor: int
    prateleira: int

@app.get('/store')
async def get_store():
    df = ler_produtos_csv()
    return df.to_dict(orient="records")

@app.get('/store/{produto_cod}')
async def get_store_codigo(produto_cod: int):
    df = ler_produtos_csv()
    produto = df[df['codigo'] == produto_cod]
    
    if not produto.empty:
        return produto.to_dict(orient="records")[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Produto de código {produto_cod} não foi encontrado!")

@app.post("/store", status_code=status.HTTP_201_CREATED)
async def post_store(produto: Produto):
    try:
        # logger.debug("Recebido produto: %s", produto.dict())
        df = ler_produtos_csv()

        # Verifica duplicata
        if not df[df["codigo"] == produto.codigo].empty:
            # logger.warning("Código duplicado encontrado: %s", produto.codigo)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O produto {produto.codigo} já existe na base de dados!"
            )

        # Gera próximo ID
        next_id = int(df["id"].max()) + 1 if not pd.isna(df["id"].max()) else 1
        produto_dict = produto.dict()
        produto_dict["id"] = next_id
        # logger.debug("Produto com ID gerado: %s", produto_dict)

        df = pd.concat([df, pd.DataFrame([produto_dict])], ignore_index=True)
        salvar_produtos_csv(df)

        return produto_dict

    except HTTPException as e:
        # Relevanta exceções HTTP específicas (como o 409)
        raise e
    except Exception as e:
        logger.error("Erro interno no endpoint: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.put("/store/{produto_cod}", status_code=status.HTTP_200_OK)
async def put_store(produto_cod: str, produto: Produto):
    try:
        # logger.debug("PUT recebido - Código: %s, Dados: %s", produto_cod, produto.dict())
        df = ler_produtos_csv()

        # Verifica se o DataFrame está vazio
        if df.empty:
            logger.warning("CSV vazio, nenhum produto para atualizar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum produto encontrado no banco (CSV vazio)."
            )

        # Busca o produto pelo código
        index = df.index[df["codigo"].astype(str) == produto_cod].tolist()
        if not index:
            logger.warning("Produto não encontrado: %s", produto_cod)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Não existe produto com o código {produto_cod}!"
            )

        # Prepara os dados atualizados, preservando o ID
        produto_dict = produto.dict()
        produto_dict["id"] = int(df.at[index[0], "id"])  # Mantém o ID original

        # Atualiza o DataFrame
        df.loc[index[0],['id', 'nome', 'marca', 'codigo', 'preco', 'quantidade', 'corredor', 'prateleira']] = [
            produto_dict["id"],
            produto_dict["nome"],
            produto_dict["marca"],
            produto_dict["codigo"],
            produto_dict["preco"],
            produto_dict["quantidade"],
            produto_dict["corredor"],
            produto_dict["prateleira"]
        ]

        # Salva as alterações
        salvar_produtos_csv(df)
        # logger.debug("Atualização concluída para código: %s", produto_cod)

        # Retorna uma resposta simples e serializável
        return {
            "message": "Produto atualizado com sucesso",
            "produto": produto_dict
        }

    except HTTPException as e:
        raise e  # Propaga exceções específicas (ex.: 404)
    except Exception as e:
        logger.error("Erro interno no PUT: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.delete("/store/{produto_cod}", status_code=status.HTTP_200_OK)
async def delete_produto(produto_cod: str):
    try:
        df = ler_produtos_csv()

        # Verifica se o DataFrame está vazio
        if df.empty:
            # logger.warning("CSV está vazio, nenhum produto para deletar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum produto encontrado no banco (CSV vazio)."
            )

        # Converte produto_cod para o tipo correto, se necessário
        # (assumindo que "codigo" no CSV é string; ajuste se for int)
        # logger.debug("Buscando produto com código: %s", produto_cod)
        index = df.index[df["codigo"].astype(str) == produto_cod].tolist()

        if not index:
            logger.warning("Produto não encontrado para o código: %s", produto_cod)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Não existe um produto com o código: {produto_cod}."
            )

        # Remove o produto
        # logger.debug("Índice encontrado: %s", index)
        df = df.drop(index[0])

        salvar_produtos_csv(df)
        # logger.debug("Deleção concluída para o código: %s", produto_cod)

        return {
            "message": "Produto deletado com sucesso!",
            "codigo": produto_cod
        }

    except HTTPException as e:
        raise e  # Propaga exceções HTTP específicas (como 404)
    except Exception as e:
        logger.error("Erro interno ao deletar produto: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, debug=True, reload=True)