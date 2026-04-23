import os
from dotenv import load_dotenv
from store_service import StoreService

load_dotenv()

CSV_FILENAME = os.getenv("CSV_FILENAME", "store.csv")
store = StoreService(CSV_FILENAME)

SEPARADOR = "*" * 40


# ===================== UTILITÁRIOS =====================

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def ler_int(mensagem: str) -> int | None:
    try:
        return int(input(mensagem))
    except ValueError:
        print("\n[ERRO] Valor inválido! Informe um número inteiro.")
        return None


def ler_float(mensagem: str) -> float | None:
    try:
        return float(input(mensagem))
    except ValueError:
        print("\n[ERRO] Valor inválido! Informe um número.")
        return None


def exibir_produtos(produtos: list[dict], titulo: str = "RESULTADOS"):
    if not produtos:
        print("\nNenhum produto encontrado.")
        return

    print(f"\n{SEPARADOR}")
    print(f"  {titulo} ({len(produtos)} produto(s))")
    print(SEPARADOR)
    print(f"{'ID':<5} {'Nome':<15} {'Marca':<12} {'Código':<8} {'Preço':>8} {'Qtd':>5} {'Cor':>4} {'Prat':>5}")
    print("-" * 70)
    for p in produtos:
        print(f"{int(p['id']):<5} {p['nome']:<15} {p['marca']:<12} {int(p['codigo']):<8} {p['preco']:>8.2f} {int(p['quantidade']):>5} {int(p['corredor']):>4} {int(p['prateleira']):>5}")
    print("-" * 70)


# ===================== CADASTRAR PRODUTO =====================

def cadastrar_produto():
    print(f"\n{SEPARADOR}")
    print("       CADASTRAR PRODUTO")
    print(SEPARADOR)

    nome = input("  Nome: ").strip()
    if not nome:
        print("\n[ERRO] Nome não pode ser vazio.")
        return

    marca = input("  Marca: ").strip()
    if not marca:
        print("\n[ERRO] Marca não pode ser vazia.")
        return

    codigo = ler_int("  Código: ")
    if codigo is None or codigo <= 0:
        print("\n[ERRO] Código deve ser maior que zero.")
        return

    preco = ler_float("  Preço: ")
    if preco is None or preco <= 0:
        print("\n[ERRO] Preço deve ser maior que zero.")
        return

    quantidade = ler_int("  Quantidade: ")
    if quantidade is None or quantidade < 0:
        print("\n[ERRO] Quantidade não pode ser negativa.")
        return

    corredor = ler_int("  Corredor: ")
    if corredor is None or corredor <= 0:
        print("\n[ERRO] Corredor deve ser maior que zero.")
        return

    prateleira = ler_int("  Prateleira: ")
    if prateleira is None or prateleira <= 0:
        print("\n[ERRO] Prateleira deve ser maior que zero.")
        return

    produto = {
        "nome": nome, "marca": marca, "codigo": codigo,
        "preco": preco, "quantidade": quantidade,
        "corredor": corredor, "prateleira": prateleira,
    }

    resultado = store.criar_produto(produto)
    if resultado:
        print(f"\n[OK] Produto '{nome}' cadastrado com sucesso! (ID: {resultado['id']})")
    else:
        print(f"\n[ERRO] Já existe um produto com o código {codigo}.")


# ===================== DESCADASTRAR PRODUTO =====================

def descadastrar_produto():
    print(f"\n{SEPARADOR}")
    print("      DESCADASTRAR PRODUTO")
    print(SEPARADOR)

    codigo = ler_int("  Código do produto: ")
    if codigo is None:
        return

    produto = store.buscar_por_codigo(codigo)
    if produto is None:
        print(f"\n[ERRO] Produto com código {codigo} não encontrado.")
        return

    exibir_produtos([produto], "PRODUTO A SER REMOVIDO")
    confirmacao = input("\n  Confirma a remoção? (s/n): ").strip().lower()
    if confirmacao == "s":
        store.deletar_produto(codigo)
        print(f"\n[OK] Produto código {codigo} removido com sucesso!")
    else:
        print("\n  Operação cancelada.")


# ===================== INSERIR ITEM =====================

def inserir_item():
    print(f"\n{SEPARADOR}")
    print("        INSERIR ITEM")
    print(SEPARADOR)

    codigo = ler_int("  Código do produto: ")
    if codigo is None:
        return

    produto = store.buscar_por_codigo(codigo)
    if produto is None:
        print(f"\n[ERRO] Produto com código {codigo} não encontrado.")
        return

    print(f"  Produto: {produto['nome']} | Estoque atual: {int(produto['quantidade'])}")

    quantidade = ler_int("  Quantidade a inserir: ")
    if quantidade is None or quantidade <= 0:
        print("\n[ERRO] Quantidade deve ser maior que zero.")
        return

    resultado = store.inserir_item(codigo, quantidade)
    if resultado:
        print(f"\n[OK] +{quantidade} itens adicionados. Estoque atual: {int(resultado['quantidade'])}")


# ===================== REMOVER ITEM =====================

def remover_item():
    print(f"\n{SEPARADOR}")
    print("        REMOVER ITEM")
    print(SEPARADOR)

    codigo = ler_int("  Código do produto: ")
    if codigo is None:
        return

    produto = store.buscar_por_codigo(codigo)
    if produto is None:
        print(f"\n[ERRO] Produto com código {codigo} não encontrado.")
        return

    print(f"  Produto: {produto['nome']} | Estoque atual: {int(produto['quantidade'])}")

    quantidade = ler_int("  Quantidade a remover: ")
    if quantidade is None or quantidade <= 0:
        print("\n[ERRO] Quantidade deve ser maior que zero.")
        return

    resultado = store.remover_item(codigo, quantidade)
    if resultado is None:
        print(f"\n[ERRO] Produto com código {codigo} não encontrado.")
    elif resultado == "insuficiente":
        print(f"\n[ERRO] Estoque insuficiente! Disponível: {int(produto['quantidade'])}")
    else:
        print(f"\n[OK] -{quantidade} itens removidos. Estoque atual: {int(resultado['quantidade'])}")


# ===================== SUB-MENU LISTAGEM =====================

def listar_por_codigo():
    codigo = ler_int("  Código: ")
    if codigo is None:
        return
    produtos = store.listar_por_codigo(codigo)
    exibir_produtos(produtos, "POR CÓDIGO")


def listar_por_nome():
    nome = input("  Nome (ou parte): ").strip()
    if not nome:
        print("\n[ERRO] Informe um nome.")
        return
    produtos = store.listar_por_nome(nome)
    exibir_produtos(produtos, "POR NOME")


def listar_por_marca():
    marca = input("  Marca (ou parte): ").strip()
    if not marca:
        print("\n[ERRO] Informe uma marca.")
        return
    produtos = store.listar_por_marca(marca)
    exibir_produtos(produtos, "POR MARCA")


def listar_por_preco():
    preco_min = ler_float("  Preço mínimo: ")
    if preco_min is None:
        return
    preco_max = ler_float("  Preço máximo: ")
    if preco_max is None:
        return
    if preco_min > preco_max:
        print("\n[ERRO] Preço mínimo não pode ser maior que o máximo.")
        return
    produtos = store.listar_por_preco(preco_min, preco_max)
    exibir_produtos(produtos, f"POR PREÇO (R${preco_min:.2f} - R${preco_max:.2f})")


def listar_por_quantidade():
    qtd_min = ler_int("  Quantidade mínima: ")
    if qtd_min is None:
        return
    qtd_max = ler_int("  Quantidade máxima: ")
    if qtd_max is None:
        return
    if qtd_min > qtd_max:
        print("\n[ERRO] Quantidade mínima não pode ser maior que a máxima.")
        return
    produtos = store.listar_por_quantidade(qtd_min, qtd_max)
    exibir_produtos(produtos, f"POR QUANTIDADE ({qtd_min} - {qtd_max})")


def listar_por_localizacao():
    corredor = ler_int("  Corredor: ")
    if corredor is None:
        return
    prateleira = ler_int("  Prateleira: ")
    if prateleira is None:
        return
    produtos = store.listar_por_localizacao(corredor, prateleira)
    exibir_produtos(produtos, f"LOCALIZAÇÃO (Corredor {corredor}, Prateleira {prateleira})")


def listar_todos():
    produtos = store.listar_todos()
    exibir_produtos(produtos, "TODOS OS PRODUTOS")


def sub_menu_listagem():
    while True:
        print(f"\n{SEPARADOR}")
        print("       LISTAR PRODUTOS")
        print(SEPARADOR)
        print("  1 - Por código")
        print("  2 - Por nome")
        print("  3 - Por marca")
        print("  4 - Por preço")
        print("  5 - Por quantidade")
        print("  6 - Por localização")
        print("  7 - Todos os produtos")
        print("  8 - Retornar ao menu anterior")
        print(SEPARADOR)

        opcao = ler_int("\n  Informe uma opção: ")

        if opcao == 1:
            listar_por_codigo()
        elif opcao == 2:
            listar_por_nome()
        elif opcao == 3:
            listar_por_marca()
        elif opcao == 4:
            listar_por_preco()
        elif opcao == 5:
            listar_por_quantidade()
        elif opcao == 6:
            listar_por_localizacao()
        elif opcao == 7:
            listar_todos()
        elif opcao == 8:
            break
        else:
            print("\n[ERRO] Opção inválida!")

        if opcao and 1 <= opcao <= 7:
            pausar()


# ===================== MENU PRINCIPAL =====================

def menu_principal():
    while True:
        limpar_tela()
        print(f"\n{SEPARADOR}")
        print("      STORE - MENU PRINCIPAL")
        print(SEPARADOR)
        print("  1 - Cadastrar produto")
        print("  2 - Descadastrar produto")
        print("  3 - Inserir item")
        print("  4 - Remover item")
        print("  5 - Listar produtos")
        print("  6 - Sair")
        print(SEPARADOR)

        opcao = ler_int("\n  Informe uma opção: ")

        if opcao == 1:
            cadastrar_produto()
            pausar()
        elif opcao == 2:
            descadastrar_produto()
            pausar()
        elif opcao == 3:
            inserir_item()
            pausar()
        elif opcao == 4:
            remover_item()
            pausar()
        elif opcao == 5:
            sub_menu_listagem()
        elif opcao == 6:
            print("\n  Encerrando o programa. Até logo!\n")
            break
        else:
            print("\n[ERRO] Opção inválida!")
            pausar()


if __name__ == "__main__":
    menu_principal()
