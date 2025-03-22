from functions import register_product, insert_item, delete_item, delete_product
from produto import Produto
from model import Item

# num_input = 99

def menu(flag: int):
    flag = 1
    while(flag):
        print ("*"*27)
        print ("********** MENU ***********")
        print ("* 1 - Cadastrar produto.  *")
        print ("* 2 - Inserir item.       *")
        print ("* 3 - Descartar produto.  *")
        print ("* 4 - Remover item.       *")
        print ("* 5 - Listar produto(s).  *")
        print ("* 0 - Sair.               *")
        print ("*"*27)
        print ("\n")
        
        num_input = input("*** Informe uma alternativa: ")
        
        if (int(num_input) == 0):
            print("\n*** ENCERRANDO A EXECUÇÃO DO CÓDIGO!\n")
            break
        
        while (str(num_input) == '' or str(num_input) == ' '):
            print("\n- Nenhuma alternativa foi identificada.\n")
            menu(flag)
            # num_input = input("*** Informe uma nova alternativa: ")
            
        while (int(num_input) < 0 or int(num_input) > 5):
            print("\n- Este número não está nas alternativas.\n")
            menu(flag)
            # num_input = int(input("*** Informe uma nova alternativa: "))
        
        if (int(num_input) >= 1 and int(num_input) <=5):
            functions_menu(num_input)
        
    return False


def functions_menu(num_input):
    num_input = int(num_input)
    
    if (num_input == 1):
        # make_text_title(" CADASTRAR ITEM ")
        # register_product()
        
        item = register_product()
        produto = Produto()
        
        produto.create_item(item)
        
        print ("CADASTRO\n")
        menu(1)

menu(1)