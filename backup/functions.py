from model import Item

def register_product():
    nome = input("* Insira o nome do produto: ")
    marca = input("* Insira a marca do produto: ")
    codigo = int(input("* Insira o código do produto: "))
    preco = input("* Insira o preço do produto: ")
    quantidade = int(input("* Insira a quantidade de produto(s): "))
    corredor = int(input("* Insira o corredor do produto: "))
    prateleira = int(input("* Insira a prateleira do produto: "))
    
    return Item(
            nome=nome,
            marca=marca,
            codigo=codigo,
            preco=preco,
            quantidade=quantidade,
            corredor=corredor,
            prateleira=prateleira,
            id=1  # Você pode definir um ID apropriado aqui
        )
    
def insert_item():
    codigo = int(input("* Insira o código do produto: "))
    quantidade = int(input("* Insira a quantidade de produto(s) que deseja inserir: "))
    
def delete_product():
    codigo = int(input("* Insira o código do produto que deseja deletar do banco de dados: "))
    
def delete_item():
    codigo = int(input("* Insira o código do produto que deseja deletar item(s): "))
    quantidade = int(input("* Insira a quantidade de item(s) do produto que deseja reduzir: "))