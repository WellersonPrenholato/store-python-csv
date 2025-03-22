import csv
import os
from dotenv import load_dotenv
from model import Item

load_dotenv()
path_database = os.environ["DATABASE"]

class Produto(Item):
    
    def __init__(self, item: Item):
        super().__init__(item.nome, item.ano, item.duracao)

    def create_item(self, item: Item):
        with open(path_database,"r") as file:
            firstLine = file.readline()

            if (firstLine.find("nome;marca;codigo;preco;quantidade;corredor;prateleira") >= 0):
                file.close()

            else:
                with open(path_database,"a", newline='', encoding='utf-8') as file:
                    title = csv.writer(file, delimiter=';')
                    title.writerow([
                        'nome',
                        'marca',
                        'codigo',
                        'preco',
                        'quantidade',
                        'corredor',
                        'prateleira'
                    ])
                    
            file = open(path_database, 'a', newline='', encoding='utf-8')
            new_item = csv.writer(file, delimiter=';')
            new_item.writerow([
                self.nome,
                self.marca,
                self.codigo,
                self.preco,
                self.quantidade,
                self.corredor,
                self.prateleira
            ])
            file.close()
            
        print("ITEM CRIADO COM SUCESSO! create_item")

        return True
    
    
    # def insert_item (self, item: Item):
        
    #     return True
    
    
    # def delete_item(self, codigo: int):
    #     with open(path_database, 'r') as f:
    #         linhas = csv.reader(f, delimiter=';')
    #         lst = list(linhas)
            
    #         print (lst)
            
    #         # lst.remove([F,1,Matrix,5.0])
            
    #         with open(path_database, 'w') as f: 
    #             writer = csv.writer(f)
    #             writer.writer(lst)
        
    #     return True
