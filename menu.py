from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import bcrypt
import uuid
from datetime import datetime

cloud_config = {
    'secure_connect_bundle': 'C:/caminho-pro-arquivo/secure-connect-mercado-livre.zip'
}

auth_provider = PlainTextAuthProvider(username='token', password='AstraCS:seutoken')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

session.set_keyspace('default_keyspace') 

def create_usuario():
    email = input("Digite o email do usuário: ")
    nome = input("Digite o nome do usuário: ")
    sobrenome = input("Digite o sobrenome do usuário: ")
    username = input("Digite o username do usuário: ")
    senha = input("Digite a senha do usuário: ")
    cpf = input("Digite o CPF do usuário: ")

    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user_id = uuid.uuid4()

    query = """
    INSERT INTO usuarios (id, email, nome, sobrenome, username, senha, cpf)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    session.execute(query, (user_id, email, nome, sobrenome, username, hashed_senha, cpf))
    print("Usuário criado com sucesso. ID:", user_id)

def list_all_users():
    query = "SELECT * FROM usuarios"
    rows = session.execute(query)
    if rows:
        for row in rows:
            print("ID:", row.id)
            print("Email:", row.email)
            print("Nome:", row.nome)
            print("Sobrenome:", row.sobrenome)
            print("Username:", row.username)
            print("CPF:", row.cpf)
            print("Senha (hash):", row.senha)
            print("-" * 30)  
    else:
        print("Nenhum usuário encontrado.")

def list_all_users_for_selection():
    query = "SELECT * FROM usuarios"
    rows = session.execute(query)
    
    users = list(rows)
    print("Usuários cadastrados:")
    
    for index, row in enumerate(users, start=1):
        print(f"{index}. Nome: {row.nome} | Username: {row.username} | Email: {row.email} | ID: {row.id}")
    print("-" * 30)
    
    return users  

def update_usuario():
    users = list_all_users_for_selection()
    
    while True:
        try:
            user_index = int(input("Digite o número do usuário a ser atualizado: ")) - 1
            if 0 <= user_index < len(users):
                user_id = users[user_index].id 
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    print("\nEscolha o campo a ser atualizado:")
    print("1. Email")
    print("2. Username")
    print("3. Senha")
    print("4. Nome")
    print("5. Sobrenome")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        new_email = input("Digite o novo email: ")
        query = "UPDATE usuarios SET email = %s WHERE id = %s"
        session.execute(query, (new_email, user_id))
        print("Email atualizado com sucesso.")
    
    elif choice == '2':
        new_username = input("Digite o novo username: ")
        query = "UPDATE usuarios SET username = %s WHERE id = %s"
        session.execute(query, (new_username, user_id))
        print("Username atualizado com sucesso.")
    
    elif choice == '3':
        new_senha = input("Digite a nova senha: ")
        hashed_senha = bcrypt.hashpw(new_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = "UPDATE usuarios SET senha = %s WHERE id = %s"
        session.execute(query, (hashed_senha, user_id))
        print("Senha atualizada com sucesso.")
    
    elif choice == '4':
        new_nome = input("Digite o novo nome: ")
        query = "UPDATE usuarios SET nome = %s WHERE id = %s"
        session.execute(query, (new_nome, user_id))
        print("Nome atualizado com sucesso.")
    
    elif choice == '5':
        new_sobrenome = input("Digite o novo sobrenome: ")
        query = "UPDATE usuarios SET sobrenome = %s WHERE id = %s"
        session.execute(query, (new_sobrenome, user_id))
        print("Sobrenome atualizado com sucesso.")
    
    else:
        print("Opção inválida. Nenhuma alteração foi feita.")


def create_vendedor():
    nome = input("Digite o nome do vendedor: ")
    sobrenome = input("Digite o sobrenome do vendedor: ")
    cpf = input("Digite o CPF do vendedor: ")

    vendedor_id = uuid.uuid4()

    query = """
    INSERT INTO vendedores (id, nome, sobrenome, cpf)
    VALUES (%s, %s, %s, %s)
    """
    
    session.execute(query, (vendedor_id, nome, sobrenome, cpf))
    print("Vendedor criado com sucesso. ID:", vendedor_id)

def read_vendedores():
    query = "SELECT * FROM vendedores"
    rows = session.execute(query)

    print("Vendedores e seus Produtos:")
    for vendedor in rows:
        print(f"Vendedor: {vendedor.nome} {vendedor.sobrenome} | CPF: {vendedor.cpf} | ID: {vendedor.id}")
        print("Produtos vinculados:")

        if vendedor.produtos:
            for produto_id in vendedor.produtos:
                produto_query = "SELECT * FROM produtos WHERE id = %s"
                produto = session.execute(produto_query, (produto_id,)).one()
                if produto:
                    print(f" - Nome do Produto: {produto.nome} | Descrição: {produto.descricao} | Preço: {produto.preco} | Quantidade: {produto.quantidade}")
        else:
            print("Nenhum produto vinculado.")
        print("-" * 30)

def list_all_vendedores_for_selection():
    query = "SELECT * FROM vendedores"
    rows = session.execute(query)
    
    vendedores = list(rows)
    print("Vendedores cadastrados:")
    
    for index, vendedor in enumerate(vendedores, start=1):
        print(f"{index}. Nome: {vendedor.nome} | Sobrenome: {vendedor.sobrenome} | CPF: {vendedor.cpf} | ID: {vendedor.id}")
    print("-" * 30)
    
    return vendedores

def create_produto():
    
    vendedores = list_all_vendedores_for_selection()
    
    while True:
        try:
            vendedor_index = int(input("Escolha o número do vendedor para vincular o produto: ")) - 1
            if 0 <= vendedor_index < len(vendedores):
                vendedor_id = vendedores[vendedor_index].id  
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")

    while True:
        try:
            preco = float(input("Digite o preço do produto: "))
            break  
        except ValueError:
            print("Entrada inválida. Por favor, insira um número para o preço.")

    while True:
        try:
            quantidade = int(input("Digite a quantidade do produto: "))
            break  
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro para a quantidade.")

    produto_id = uuid.uuid4()

    query = """
    INSERT INTO produtos (id, nome, descricao, preco, quantidade, vendedor_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    session.execute(query, (produto_id, nome, descricao, preco, quantidade, vendedor_id))
    print("Produto criado com sucesso e vinculado ao vendedor:", vendedor_id)

    update_vendedor_query = "UPDATE vendedores SET produtos = produtos + [%s] WHERE id = %s"
    session.execute(update_vendedor_query, (produto_id, vendedor_id))
    print(f"Produto {produto_id} adicionado à lista de produtos do vendedor {vendedor_id}.")


def read_produtos_por_vendedor():

    vendedores = list_all_vendedores_for_selection()
    
    while True:
        try:
            vendedor_index = int(input("Escolha o número do vendedor para listar os produtos: ")) - 1
            if 0 <= vendedor_index < len(vendedores):
                vendedor_id = vendedores[vendedor_index].id 
                vendedor_nome = f"{vendedores[vendedor_index].nome} {vendedores[vendedor_index].sobrenome}"
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    query = "SELECT * FROM produtos WHERE vendedor_id = %s ALLOW FILTERING"
    rows = session.execute(query, (vendedor_id,))

    print(f"\nProdutos vinculados ao vendedor {vendedor_nome} (ID: {vendedor_id}):")
    if rows:
        for produto in rows:
            print(f"ID: {produto.id} | Nome: {produto.nome} | Descrição: {produto.descricao} | Preço: {produto.preco} | Quantidade: {produto.quantidade}")
        print("-" * 30)
    else:
        print("Nenhum produto encontrado para este vendedor.")

def list_all_produtos_for_selection():
    query = "SELECT * FROM produtos"
    rows = session.execute(query)
    
    produtos = list(rows)
    print("Produtos disponíveis:")
    
    for index, produto in enumerate(produtos, start=1):
        print(f"{index}. Nome: {produto.nome} | Descrição: {produto.descricao} | Preço: {produto.preco} | ID: {produto.id}")
    print("-" * 30)
    
    return produtos  

def create_compra():

    usuarios = list_all_users_for_selection()
    while True:
        try:
            usuario_index = int(input("Escolha o número do usuário (comprador): ")) - 1
            if 0 <= usuario_index < len(usuarios):
                usuario_id = usuarios[usuario_index].id
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    produtos = list_all_produtos_for_selection()
    while True:
        try:
            produto_index = int(input("Escolha o número do produto: ")) - 1
            if 0 <= produto_index < len(produtos):
                produto_id = produtos[produto_index].id
                nome_produto = produtos[produto_index].nome
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    while True:
        try:
            quantidade = int(input("Digite a quantidade: "))
            break  
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro para a quantidade.")

    estado = input("Digite o estado da compra: ")
    data_compra = datetime.now() 

    compra_id = uuid.uuid4()

    query = """
    INSERT INTO compras (id, produto_id, nome_produto, quantidade, estado, data_compra, usuario_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    session.execute(query, (compra_id, produto_id, nome_produto, quantidade, estado, data_compra, usuario_id))
    print("Compra registrada com sucesso.")

    update_usuario_query = "UPDATE usuarios SET compras = compras + [%s] WHERE id = %s"
    session.execute(update_usuario_query, (compra_id, usuario_id))
    print(f"Compra {compra_id} adicionada à lista de compras do usuário {usuario_id}.")

def read_compras_por_usuario():
    usuarios = list_all_users_for_selection()
    while True:
        try:
            usuario_index = int(input("Escolha o número do usuário para listar as compras: ")) - 1
            if 0 <= usuario_index < len(usuarios):
                usuario_id = usuarios[usuario_index].id  
                usuario_nome = f"{usuarios[usuario_index].nome} {usuarios[usuario_index].sobrenome}"
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    query = "SELECT * FROM compras WHERE usuario_id = %s ALLOW FILTERING"
    rows = session.execute(query, (usuario_id,))

    print(f"\nCompras realizadas pelo usuário {usuario_nome} (ID: {usuario_id}):")
    if rows:
        for compra in rows:
            print(f"ID da Compra: {compra.id} | Produto: {compra.nome_produto} | Quantidade: {compra.quantidade} | Estado: {compra.estado} | Data da Compra: {compra.data_compra}")
        print("-" * 30)
    else:
        print("Nenhuma compra encontrada para este usuário.")

def delete_compra():

    usuarios = list_all_users_for_selection()
    while True:
        try:
            usuario_index = int(input("Escolha o número do usuário para listar as compras: ")) - 1
            if 0 <= usuario_index < len(usuarios):
                usuario_id = usuarios[usuario_index].id 
                usuario_nome = f"{usuarios[usuario_index].nome} {usuarios[usuario_index].sobrenome}"
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    query = "SELECT * FROM compras WHERE usuario_id = %s ALLOW FILTERING"
    rows = session.execute(query, (usuario_id,))
    
    compras = list(rows)
    if not compras:
        print("Nenhuma compra encontrada para este usuário.")
        return

    print(f"\nCompras realizadas pelo usuário {usuario_nome} (ID: {usuario_id}):")
    for index, compra in enumerate(compras, start=1):
        print(f"{index}. ID da Compra: {compra.id} | Produto: {compra.nome_produto} | Quantidade: {compra.quantidade} | Estado: {compra.estado} | Data da Compra: {compra.data_compra}")
    print("-" * 30)

    while True:
        try:
            compra_index = int(input("Escolha o número da compra para deletar: ")) - 1
            if 0 <= compra_index < len(compras):
                compra_id = compras[compra_index].id  
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    delete_query = "DELETE FROM compras WHERE id = %s"
    session.execute(delete_query, (compra_id,))
    print("Compra deletada com sucesso.")

    user_query = "SELECT compras FROM usuarios WHERE id = %s"
    user_data = session.execute(user_query, (usuario_id,)).one()
    
    if user_data and user_data.compras:

        updated_compras = [cid for cid in user_data.compras if cid != compra_id]

        update_usuario_query = "UPDATE usuarios SET compras = %s WHERE id = %s"
        session.execute(update_usuario_query, (updated_compras, usuario_id))
        print(f"Compra {compra_id} removida da lista de compras do usuário {usuario_nome}.")

def add_favorito():

    usuarios = list_all_users_for_selection()
    while True:
        try:
            usuario_index = int(input("Escolha o número do usuário para adicionar o favorito: ")) - 1
            if 0 <= usuario_index < len(usuarios):
                usuario_id = usuarios[usuario_index].id 
                usuario_nome = f"{usuarios[usuario_index].nome} {usuarios[usuario_index].sobrenome}"
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    produtos = list_all_produtos_for_selection()
    while True:
        try:
            produto_index = int(input("Escolha o número do produto para adicionar aos favoritos: ")) - 1
            if 0 <= produto_index < len(produtos):
                produto_id = produtos[produto_index].id 
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    user_query = "SELECT favoritos FROM usuarios WHERE id = %s"
    user_data = session.execute(user_query, (usuario_id,)).one()

    if user_data and user_data.favoritos and produto_id in user_data.favoritos:
        print(f"O produto {produto_id} já está nos favoritos do usuário {usuario_nome}.")
    else:
        update_usuario_query = "UPDATE usuarios SET favoritos = favoritos + [%s] WHERE id = %s"
        session.execute(update_usuario_query, (produto_id, usuario_id))
        print(f"Produto {produto_id} adicionado aos favoritos do usuário {usuario_nome}.")

def list_favoritos_por_usuario():

    usuarios = list_all_users_for_selection()
    while True:
        try:
            usuario_index = int(input("Escolha o número do usuário para listar os favoritos: ")) - 1
            if 0 <= usuario_index < len(usuarios):
                usuario_id = usuarios[usuario_index].id 
                usuario_nome = f"{usuarios[usuario_index].nome} {usuarios[usuario_index].sobrenome}"
                break
            else:
                print("Índice fora do alcance. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    user_query = "SELECT favoritos FROM usuarios WHERE id = %s"
    user_data = session.execute(user_query, (usuario_id,)).one()
    
    print(f"\nFavoritos do usuário {usuario_nome} (ID: {usuario_id}):")
    if user_data and user_data.favoritos:
        for produto_id in user_data.favoritos:
            produto_query = "SELECT * FROM produtos WHERE id = %s"
            produto = session.execute(produto_query, (produto_id,)).one()
            if produto:
                print(f" - Nome do Produto: {produto.nome} | Descrição: {produto.descricao} | Preço: {produto.preco} | Quantidade: {produto.quantidade}")
        print("-" * 30)
    else:
        print("Nenhum produto favorito encontrado para este usuário.")


# Função principal para o menu
def main():
    while True:
        print("\nMenu Principal:")
        print("1. Menu de Usuários")
        print("2. Menu de Vendedores")
        print("3. Menu de Produtos")
        print("4. Menu de Compras")
        print("5. Menu de Favoritos")
        print("6. Sair")

        choice = input("Escolha uma opção: ")
        if choice == '1':
            usuario_menu()
        elif choice == '2':
            vendedor_menu()
        elif choice == '3':
            produto_menu()
        elif choice == '4':
            compra_menu()
        elif choice == '5':
            favoritos_menu()
        elif choice == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Submenu Usuário
def usuario_menu():
    while True:
        print("\nMenu CRUD de Usuários:")
        print("1. Criar Usuário")
        print("2. Listar Todos os Usuários")
        print("3. Atualizar Usuário")
        print("4. Voltar ao Menu Principal")

        choice = input("Escolha uma opção: ")
        if choice == '1':
            create_usuario()
        elif choice == '2':
            list_all_users()
        elif choice == '3':
            update_usuario()
        elif choice == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Submenu Vendedor
def vendedor_menu():
    while True:
        print("\nMenu Vendedores:")
        print("1. Criar Vendedor")
        print("2. Listar Todos os Vendedores")
        print("3. Voltar ao Menu Principal")

        choice = input("Escolha uma opção: ")
        if choice == '1':
            create_vendedor()
        elif choice == '2':
            read_vendedores()
        elif choice == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Submenu Produto
def produto_menu():
    while True:
        print("\nMenu Produtos:")
        print("1. Criar Produto")
        print("2. Listar Todos os Produtos")
        print("3. Voltar ao Menu Principal")

        choice = input("Escolha uma opção: ")
        if choice == '1':
            create_produto()
        elif choice == '2':
            read_produtos_por_vendedor()
        elif choice == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Submenu Compra
def compra_menu():
    while True:
        print("\nMenu Compras:")
        print("1. Comprar")
        print("2. Listar Todos as compras")
        print("3. Deletar compra")
        print("4. Voltar ao Menu Principal")

        choice = input("Escolha uma opção: ")
        if choice == '1':
            create_compra()
        elif choice == '2':
            read_compras_por_usuario()
        elif choice == '3':
            delete_compra()
        elif choice == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Submenu Favoritos
def favoritos_menu():
    while True:
        print("\nMenu Favoritos:")
        print("1. Adicionar produto nos favoritos")
        print("2. Listar Todos as favoritos")
        print("3. Voltar ao Menu Principal")

        choice = input("Escolha uma opção: ")
        if choice == '1':
            add_favorito()
        elif choice == '2':
            list_favoritos_por_usuario()
        elif choice == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
