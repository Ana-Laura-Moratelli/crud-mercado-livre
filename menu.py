from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from usuario import create_usuario
from usuario import delete_usuario
from usuario import read_usuario
from usuario import update_usuario

from vendedor import create_vendedor    
from vendedor import delete_vendedor
from vendedor import read_vendedor
from vendedor import update_vendedor

uri = "mongodb+srv://mercado-livre:12345@cluster0.ue92a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercadolivre

key = 0
sub = 0

while (key != 'S'):
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    key = input("Digite a opção desejada? (S para sair) ")
#Usuário
    if (key == '1'):
        print("Menu do Usuário")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create usuario")
            create_usuario()
            
        elif (sub == '2'):
            nome = input("Read usuário, deseja algum nome especifico? ")
            read_usuario(nome)
        
        elif (sub == '3'):
            print("Listando usuários para atualização:")
            update_usuario()

        elif (sub == '4'):
            print("delete usuario")
            nome = input("Nome a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            delete_usuario(nome, sobrenome)
#Vendedor            
    elif (key == '2'):
        print("Menu do Vendedor")
        print("1-Create Vendedor")
        print("2-Read Vendedor")
        print("3-Update Vendedor")
        print("4-Delete Vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create vendedor")
            create_vendedor()
            
        elif (sub == '2'):
            nome = input("Read vendedor, deseja algum nome especifico? ")
            read_vendedor(nome)
        
        elif (sub == '3'):
            nome = input("Update vendedor, deseja algum nome especifico? ")
            update_vendedor(nome)

        elif (sub == '4'):
            print("delete usuario")
            nome = input("Nome a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            delete_vendedor(nome, sobrenome) 
#Produto
    elif (key == '3'):
        print("Menu do Produto")
        print("1-Create Produto")
        print("2-Read Produto")
        print("3-Update Produto")
        print("4-Delete Produto")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create Produto")
            create_usuario()
            
        elif (sub == '2'):
            nome = input("Read usuário, deseja algum nome especifico? ")
            read_usuario(nome)
        
        elif (sub == '3'):
            print("Listando Produto para atualização:")
            update_usuario()

        elif (sub == '4'):
            print("delete Produto")
            nome = input("Nome a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            delete_usuario(nome, sobrenome)   
#Compra  
    elif (key == '4'):
        print("Menu Compra")
        print("1-Comprar")
        print("2-Listar Compras")
#Favoritos 
    elif (key == '5'):
        print("Menu Favoritos")
        print("1-Adicionar produto no favoritos")
        print("2-Listar favoritos")
        print("4-Deletar produto do favoritos")
    
print("Tchau...")
