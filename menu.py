from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from usuario import create_usuario, read_usuario, update_usuario, delete_usuario
from vendedor import create_vendedor, read_vendedor, update_vendedor, delete_vendedor
from produto import create_produto, read_produto, update_produto, delete_produto
from compra import create_compra, listar_compras
from favoritos import add_favorito, read_favorito, delete_favorito
from usuarioRedis import sincronizar_endereco_mongo_para_redis, adicionar_endereco_redis, editar_endereco_redis, remover_endereco_redis, listar_endereco_redis, sincronizar_endereco_redis_para_mongo, sincronizar_cartao_mongo_para_redis, adicionar_cartao_redis, editar_cartao_redis, remover_cartao_redis, listar_cartao_redis, sincronizar_cartao_redis_para_mongo

import bcrypt
import redis

# Conexão Redis
r = redis.Redis(
    host='redis-17330.c11.us-east-1-2.ec2.redns.redis-cloud.com',
    port=17330,
    password='Q8SNK0YuL1GWvYzDPbm6WrglHlS9d3VY'
)

# Conexão MongoDB
uri = "mongodb+srv://mercado-livre:12345@cluster0.ue92a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercadolivre

key = ''
sub = ''

def confirmar_saida():
    confirmacao = input("Tem certeza que deseja sair? (S para confirmar, N para cancelar) ").lower()
    return confirmacao == 's' or  confirmacao == 'S'

def login_usuario(db, r):
    mycol = db.usuario
    username = input("Digite o username: ")
    senha = input("Digite a senha: ")

    usuario = mycol.find_one({"username": username})
    
    if usuario:
        senha_armazenada = usuario['senha']
        
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):
            print("Login bem-sucedido!")
            token = f"token_{username}"
            r.set(f"session:{token}", username, ex=300) 
            return token  
        else:
            print("Senha incorreta.")
            return None
    else:
        print("Username não encontrado.")
        return None

def verificar_sessao(r, token):
    usuario = r.get(f"session:{token}")
    if usuario:
        return usuario.decode('utf-8')  
    else:
        return None

token = None

while key != 'S':
    if not token:
        print("1-Login Usuário")
        key = input("Digite a opção desejada? (S para sair) ")

        if key == '1':
            token = login_usuario(db, r)
        continue

    usuario_logado = verificar_sessao(r, token)
    
    if usuario_logado:
        print(f"Usuário logado: {usuario_logado}")
        print("1-CRUD Usuário")
        print("2-CRUD Vendedor")
        print("3-CRUD Produto")
        print("4-Compras")
        print("5-Favoritos")
        print("6-Redis Endereço")
        print("7-Redis Cartão")

        key = input("Digite a opção desejada? (S para sair) ").upper()

        if key == 'S' and usuario_logado:
            if confirmar_saida():
                break
            else:
                key = ''
                continue

        usuario_logado = verificar_sessao(r, token)
        if not usuario_logado:
            print("Sessão expirada. Faça login novamente.")
            token = None
            continue

        usuario_logado = verificar_sessao(r, token)
        if not usuario_logado:
            print("Sessão expirada. Faça login novamente.")
            token = None
            continue 

        # CRUD Usuário
        if key == '1':
            print("Menu do Usuário")
            print("1-Create Usuário")
            print("2-Read Usuário")
            print("3-Update Usuário")
            print("4-Delete Usuário")
            sub = input("Digite a opção desejada? (V para voltar) ")

            if sub == '1':
                create_usuario(db)

            elif sub == '2':
                read_usuario(db)

            elif sub == '3':
                update_usuario(db)

            elif sub == '4':
                delete_usuario(db)

        # CRUD Vendedor
        elif key == '2':
            print("Menu do Vendedor")
            print("1-Create Vendedor")
            print("2-Read Vendedor")
            print("3-Update Vendedor")
            print("4-Delete Vendedor")
            sub = input("Digite a opção desejada? (V para voltar) ")

            if sub == '1':
                create_vendedor(db)

            elif sub == '2':
                read_vendedor(db)

            elif sub == '3':
                update_vendedor(db)

            elif sub == '4':
                delete_vendedor(db)

        # CRUD Produto
        elif key == '3':
            print("Menu do Produto")
            print("1-Create Produto")
            print("2-Read Produto")
            print("3-Update Produto")
            print("4-Delete Produto")
            sub = input("Digite a opção desejada? (V para voltar) ")

            if sub == '1':
                create_produto(db)

            elif sub == '2':
                read_produto(db)

            elif sub == '3':
                update_produto(db)

            elif sub == '4':
                delete_produto(db)

        # Menu de Compras
        elif key == '4':
            print("Menu Compra")
            print("1-Comprar")
            print("2-Listar Compras")
            sub = input("Digite a opção desejada? (V para voltar) ")

            if sub == '1':
                create_compra(db)

            elif sub == '2':
                listar_compras(db)

        # Menu de Favoritos
        elif key == '5':
            print("Menu Favoritos")
            print("1-Adicionar produto no favoritos")
            print("2-Listar favoritos")
            print("3-Deletar produto dos favoritos")
            sub = input("Digite a opção desejada? (V para voltar) ")

            if sub == '1':
                add_favorito(db)

            elif sub == '2':
                read_favorito(db)

            elif sub == '3':
                delete_favorito(db)

        # Menu Redis Endereço
        elif key == '6': 
            print("Redis Endereço")
            print("1-Sincronizar endereço no Redis")
            print("2-Adicionar endereço no Redis")
            print("3-Editar endereço no Redis")
            print("4-Remover endereço no Redis")
            print("5-Listar endereço no Redis")
            print("6-Sincronizar com o Mongo")
            sub = input("Digite a opção desejada? (V para voltar) ")
         
            if sub == '1':
                sincronizar_endereco_mongo_para_redis(db, r, usuario_logado)

            elif sub == '2':
                adicionar_endereco_redis(r, usuario_logado)

            elif sub == '3':
                editar_endereco_redis(r, usuario_logado)

            elif sub == '4':
                remover_endereco_redis(r, usuario_logado)

            elif sub == '5':
                listar_endereco_redis(r, usuario_logado)

            elif sub == '6':
                sincronizar_endereco_redis_para_mongo(db, r, usuario_logado)

        # Menu Redis Cartão
        elif key == '7': 
            print("Redis Cartão")
            print("1-Sincronizar cartão no Redis")
            print("2-Adicionar cartão no Redis")
            print("3-Editar cartão no Redis")
            print("4-Remover cartão no Redis")
            print("5-Listar cartão no Redis")
            print("6-Sincronizar com o Mongo")
            sub = input("Digite a opção desejada? (V para voltar) ")
         
            if sub == '1':
                sincronizar_cartao_mongo_para_redis(db, r, usuario_logado)

            elif sub == '2':
                adicionar_cartao_redis(r, usuario_logado)

            elif sub == '3':
                editar_cartao_redis(r, usuario_logado)

            elif sub == '4':
                remover_cartao_redis(r, usuario_logado)

            elif sub == '5':
                listar_cartao_redis(r, usuario_logado)

            elif sub == '6':
                sincronizar_cartao_redis_para_mongo(db, r, usuario_logado)

    else:
        print("Sessão expirada. Faça login novamente.")
        token = None

print("Tchau...")
