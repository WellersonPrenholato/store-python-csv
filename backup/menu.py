from functions import register_product, insert_item, delete_item, delete_product
from produto import create_item
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


def sub_menu_list():
    num_input = 99
    
    while(num_input != 9):
        print("\n********** LISTAGEM **********")
        print("1 - Por código.")
        print("2 - Por marca.")
        print("3 - Por preço.")
        print("4 - Por quantidade.")
        print("5 - Por localização.")
        print("9 - Retornar ao menu anterior.")
        print("******************************\n")
        
        num_input = int(input("\n*** Informe a forma da listagem: "))
        
        functions_sub_menu_list(num_input)
        
        while (int(num_input) < 1 or int(num_input) > 5):
            print("\n- Este número não está nas alternativas.")
            # num_input = int(input("*** Informe uma nova alternativa de listagem: "))
            sub_menu_list()
            
    if (num_input == 9):
        num_input = 99
        menu(num_input)
        
def functions_sub_menu_list(num_input):
    if (num_input == 1):
        print("*"*15 +
              "* POR CÓDIGO *" +
              "*"*15)
        sub_menu_list()
        
    elif(num_input == 2):
        print("*"*15 +
              "* POR MARCA *" +
              "*"*15)
        sub_menu_list()
        
    elif(num_input == 3):
        print("*"*15 +
              "* INSERIR ITEM *" +
              "*"*15)
        sub_menu_list()
        
    elif(num_input == 4):
        print("\nSaida 4")
        sub_menu_list()
    elif(num_input == 5):
        print("\nSaida 5")
        sub_menu_list()
    else:
        if(num_input == 9):
            menu()

def make_text_title(text):
    print("\n")
    print("*"*(len(text) + 2) +
            "\n*"+ text + "*\n" +
            "*"*(len(text) + 2))


def functions_menu(num_input):
    num_input = int(num_input)
    
    if (num_input == 1):
        make_text_title(" CADASTRAR ITEM ")
        register_product()
        print ("\n")
        menu(1)
        
    elif(num_input == 2):
        make_text_title(" INSERIR ITEM ")
        # insert_item()
        print ("\n")
        menu(2)
        
    elif(num_input == 3):
        make_text_title(" DESCARTAR PRODUTO ")
        # delete_product()
        print ("\n")
        menu(3)
        
    elif(num_input == 4):
        make_text_title(" REMOVER ITEM ")
        # delete_item()
        print ("\n")
        menu(4)
        
    elif(num_input == 5):
        make_text_title(" LISTAR PRODUTOS ")
        print ("\n")
        sub_menu_list()
    
    elif(num_input == 0):
        print("\n*** ENCERRANDO A EXECUÇÃO DO CÓDIGO!\n")
        menu(0)

menu(1)