
# num_input = 99

def menu():
    flag  = 1
    while(flag):
        print("\n********** MENU **********")
        print ("1 - Cadastrar produto.")
        print ("2 - Descartar produto.")
        print ("3 - Inserir item.") 
        print ("4 - Remover item.")
        print ("5 - Listar produto(s).")
        print ("0 - Sair.")
        print("*************************\n")
        
        num_input = input("*** Informe uma alternativa: ")
        
        while (num_input == '' or num_input == ' '):
            print("\n- Nenhum alternativa foi identificada.")
            num_input = input("*** Informe uma nova alternativa: ")
        
        if (int(num_input) == 0):
            print("\n*** ENCERRANDO A EXECUÇÃO DO CÓDIGO!\n")
            break

        if (int(num_input) >= 1 or int(num_input) <=5):
            functions_menu(num_input)
        
    return True


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
            num_input = int(input("*** Informe uma nova alternativa de listagem: "))
            
    if (num_input == 9):
        num_input = 99
        menu(num_input)
        
        
        
def make_text_title(text):
    print("\n")
    print("*"*(len(text) + 2) +
            "\n*"+ text + "*\n" +
            "*"*(len(text) + 2))


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
        

def functions_menu(num_input):
    num_input = int(num_input)
    
    if (num_input == 1):
        make_text_title(" CADASTRAR ITEM ")
        menu()
        
    elif(num_input == 2):
        make_text_title(" DESCARTAR ITEM ")
        menu()
        
    elif(num_input == 3):
        make_text_title(" INSERIR ITEM ")
        menu()
        
    elif(num_input == 4):
        make_text_title(" REMOVER ITEM ")
        menu()
        
    elif(num_input == 5):
        make_text_title(" LISTAR PRODUTOS ")
        sub_menu_list()
        
    else:
        while (int(num_input) < 0 or int(num_input) > 5):
            print("\n- Este número não está nas alternativas.")
            num_input = int(input("*** Informe uma nova alternativa: "))
    


menu()