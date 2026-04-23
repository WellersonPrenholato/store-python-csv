import pandas as pd
import logging

logger = logging.getLogger(__name__)

CSV_COLUMNS = ['id', 'nome', 'marca', 'codigo', 'preco', 'quantidade', 'corredor', 'prateleira']


class StoreService:
    """Serviço responsável pelas operações CRUD no arquivo CSV."""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def ler_produtos(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.csv_path)
            logger.info("CSV carregado: %d produtos", len(df))
            return df
        except FileNotFoundError:
            logger.warning("Arquivo CSV não encontrado, criando DataFrame vazio")
            return pd.DataFrame(columns=CSV_COLUMNS)

    def salvar_produtos(self, df: pd.DataFrame):
        df.to_csv(self.csv_path, index=False)
        logger.info("CSV salvo com %d produtos", len(df))

    def listar_todos(self) -> list[dict]:
        df = self.ler_produtos()
        return df.to_dict(orient="records")

    def buscar_por_codigo(self, codigo: int) -> dict | None:
        df = self.ler_produtos()
        produto = df[df['codigo'] == codigo]
        if produto.empty:
            return None
        return produto.to_dict(orient="records")[0]

    def criar_produto(self, produto_dict: dict) -> dict:
        df = self.ler_produtos()

        if not df[df["codigo"] == produto_dict["codigo"]].empty:
            logger.warning("Código duplicado: %s", produto_dict["codigo"])
            return None

        next_id = int(df["id"].max()) + 1 if not df.empty and not pd.isna(df["id"].max()) else 1
        produto_dict["id"] = next_id
        logger.info("Criando produto ID=%d, codigo=%s", next_id, produto_dict["codigo"])

        df = pd.concat([df, pd.DataFrame([produto_dict])], ignore_index=True)
        self.salvar_produtos(df)
        return produto_dict

    def atualizar_produto(self, codigo: int, produto_dict: dict) -> dict | None:
        df = self.ler_produtos()

        if df.empty:
            return None

        index = df.index[df["codigo"] == codigo].tolist()
        if not index:
            return None

        produto_dict["id"] = int(df.at[index[0], "id"])
        logger.info("Atualizando produto ID=%d, codigo=%s", produto_dict["id"], codigo)

        for col in CSV_COLUMNS:
            if col in produto_dict:
                df.at[index[0], col] = produto_dict[col]

        self.salvar_produtos(df)
        return produto_dict

    def deletar_produto(self, codigo: int) -> bool:
        df = self.ler_produtos()

        if df.empty:
            return False

        index = df.index[df["codigo"] == codigo].tolist()
        if not index:
            return False

        logger.info("Deletando produto codigo=%s", codigo)
        df = df.drop(index[0])
        self.salvar_produtos(df)
        return True

    # ===================== OPERAÇÕES DE QUANTIDADE =====================

    def inserir_item(self, codigo: int, quantidade: int) -> dict | None:
        """Adiciona quantidade ao estoque de um produto existente."""
        df = self.ler_produtos()

        index = df.index[df["codigo"] == codigo].tolist()
        if not index:
            return None

        df.at[index[0], "quantidade"] = int(df.at[index[0], "quantidade"]) + quantidade
        logger.info("Inserido +%d itens no produto codigo=%s", quantidade, codigo)
        self.salvar_produtos(df)
        return df.loc[index[0]].to_dict()

    def remover_item(self, codigo: int, quantidade: int) -> dict | None | str:
        """Remove quantidade do estoque. Retorna None se não encontrou, 'insuficiente' se não tem estoque."""
        df = self.ler_produtos()

        index = df.index[df["codigo"] == codigo].tolist()
        if not index:
            return None

        atual = int(df.at[index[0], "quantidade"])
        if quantidade > atual:
            return "insuficiente"

        df.at[index[0], "quantidade"] = atual - quantidade
        logger.info("Removido -%d itens do produto codigo=%s", quantidade, codigo)
        self.salvar_produtos(df)
        return df.loc[index[0]].to_dict()

    # ===================== FILTROS DE LISTAGEM =====================

    def listar_por_codigo(self, codigo: int) -> list[dict]:
        df = self.ler_produtos()
        return df[df["codigo"] == codigo].to_dict(orient="records")

    def listar_por_nome(self, nome: str) -> list[dict]:
        df = self.ler_produtos()
        return df[df["nome"].str.contains(nome, case=False, na=False)].to_dict(orient="records")

    def listar_por_marca(self, marca: str) -> list[dict]:
        df = self.ler_produtos()
        return df[df["marca"].str.contains(marca, case=False, na=False)].to_dict(orient="records")

    def listar_por_preco(self, preco_min: float, preco_max: float) -> list[dict]:
        df = self.ler_produtos()
        return df[(df["preco"] >= preco_min) & (df["preco"] <= preco_max)].to_dict(orient="records")

    def listar_por_quantidade(self, qtd_min: int, qtd_max: int) -> list[dict]:
        df = self.ler_produtos()
        return df[(df["quantidade"] >= qtd_min) & (df["quantidade"] <= qtd_max)].to_dict(orient="records")

    def listar_por_localizacao(self, corredor: int, prateleira: int) -> list[dict]:
        df = self.ler_produtos()
        return df[(df["corredor"] == corredor) & (df["prateleira"] == prateleira)].to_dict(orient="records")
