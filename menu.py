from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from usuario import create_usuario,read_usuario, update_usuario, delete_usuario
from vendedor import create_vendedor, read_vendedor, update_vendedor, delete_vendedor
from produto import create_produto, read_produto, update_produto, delete_produto
from compra import comprar, listar_compras
from favoritos import add_favorito, read_favorito, delete_favorito

uri = "mongodb+srv://mercado-livre:12345@cluster0.ue92a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercadolivre

key = 0
sub = 0

while (key != 'S'):
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("4-Compras")
    print("5-Favoritos")

    key = input("Digite a opção desejada? (S para sair) ")

    # CRUD Usuário
    if (key == '1'):
        print("Menu do Usuário")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        sub = input("Digite a opção desejada? (V para voltar) ")

        if (sub == '1'):
            create_usuario(db)  

        elif (sub == '2'):
            read_usuario(db)

        elif (sub == '3'):           
            update_usuario(db)  

        elif (sub == '4'):           
            delete_usuario(db)

    # CRUD Vendedor
    elif (key == '2'):
        print("Menu do Vendedor")
        print("1-Create Vendedor")
        print("2-Read Vendedor")
        print("3-Update Vendedor")
        print("4-Delete Vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ")

        if (sub == '1'):
            create_vendedor(db)  

        elif (sub == '2'):
            read_vendedor(db)  

        elif (sub == '3'):
            update_vendedor(db)  

        elif (sub == '4'):
            delete_vendedor(db)  

    # CRUD Produto
    elif (key == '3'):
        print("Menu do Produto")
        print("1-Create Produto")
        print("2-Read Produto")
        print("3-Update Produto")
        print("4-Delete Produto")
        sub = input("Digite a opção desejada? (V para voltar) ")

        if (sub == '1'):
            create_produto(db)  

        elif (sub == '2'):
            read_produto(db)  

        elif (sub == '3'):
            update_produto(db) 

        elif (sub == '4'):
            delete_produto(db) 

    # Menu de Compras
    elif (key == '4'):
        print("Menu Compra")
        print("1-Comprar")
        print("2-Listar Compras")
        sub = input("Digite a opção desejada? (V para voltar) ")


        if (sub == '1'):
            comprar(db)  

        elif (sub == '2'):
            listar_compras(db)

    # Menu de Favoritos
    elif (key == '5'):
        print("Menu Favoritos")
        print("1-Adicionar produto no favoritos")
        print("2-Listar favoritos")
        print("4-Deletar produto dos favoritos")
        sub = input("Digite a opção desejada? (V para voltar) ")

        if (sub == '1'):
            add_favorito(db) 

        elif (sub == '2'):
            read_favorito(db) 

        elif (sub == '3'):
            delete_favorito(db) 

print("Tchau...")