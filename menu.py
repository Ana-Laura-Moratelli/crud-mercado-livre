from neo4j import GraphDatabase
import bcrypt
from datetime import datetime

URI = "neo4j+s://321f9087.databases.neo4j.io"
AUTH = ("neo4j", "aX2fviFJWP4csSDS5IRyM9qgVAV22MRZHs03N2H95s8")
employee_threshold=10

def criar_usuario(tx, email, nome, sobrenome, username, hashed_senha, cpf):
    query = """
    CREATE (u:Usuario {
        email: $email,
        nome: $nome,
        sobrenome: $sobrenome,
        username: $username,
        senha: $hashed_senha,
        cpf: $cpf
    })
    RETURN u
    """
    result = tx.run(query, email=email, nome=nome, sobrenome=sobrenome,
                    username=username, hashed_senha=hashed_senha, cpf=cpf)
    return result.single()

def listar_usuarios(tx):
    query = "MATCH (u:Usuario) RETURN u"
    result = tx.run(query)
    return [record["u"] for record in result]

def criar_vendedor(tx, nome, sobrenome, cpf):
    query = """
    CREATE (v:Vendedor {
        nome: $nome,
        sobrenome: $sobrenome,
        cpf: $cpf
    })
    RETURN v
    """
    result = tx.run(query, nome=nome, sobrenome=sobrenome, cpf=cpf)
    return result.single()

def listar_vendedores(tx):
    query = "MATCH (v:Vendedor) RETURN v"
    result = tx.run(query)
    return [record["v"] for record in result]

def listar_vendedores_com_indices(tx):
    query = "MATCH (v:Vendedor) RETURN v"
    result = tx.run(query)
    return [record["v"] for record in result]

def criar_produto(tx, nome, descricao, preco, vendedor_id):
    query = """
    MATCH (v:Vendedor)
    WHERE ID(v) = $vendedor_id
    CREATE (p:Produto {
        nome: $nome,
        descricao: $descricao,
        preco: $preco
    })-[:VENDIDO_POR]->(v)
    RETURN p, v
    """
    result = tx.run(query, nome=nome, descricao=descricao, preco=preco, vendedor_id=vendedor_id)
    return result.single()

def listar_produtos(tx):
    query = """
    MATCH (p:Produto)-[:VENDIDO_POR]->(v:Vendedor)
    RETURN p, v
    """
    result = tx.run(query)
    return [{"produto": record["p"], "vendedor": record["v"]} for record in result]


def listar_produtos_para_compra(tx):
    query = """
    MATCH (p:Produto)-[:VENDIDO_POR]->(v:Vendedor)
    RETURN p, v
    """
    result = tx.run(query)
    return [{"produto": record["p"], "vendedor": record["v"]} for record in result]

def criar_compra(tx, produto_id, usuario_id, quantidade, estado):
    data_compra = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    query = """
    MATCH (p:Produto), (u:Usuario)
    WHERE ID(p) = $produto_id AND ID(u) = $usuario_id
    CREATE (u)-[:COMPROU]->(c:Compra {
        quantidade: $quantidade,
        estado: $estado,
        data_compra: datetime($data_compra)
    })-[:DE]->(p)
    RETURN c, u, p
    """
    result = tx.run(query, produto_id=produto_id, usuario_id=usuario_id,
                    quantidade=quantidade, estado=estado, data_compra=data_compra)
    return result.single()

def listar_compras(tx):
    query = """
    MATCH (u:Usuario)-[:COMPROU]->(c:Compra)-[:DE]->(p:Produto)
    RETURN c, u, p
    """
    result = tx.run(query)
    return [{"compra": record["c"], "usuario": record["u"], "produto": record["p"]} for record in result]

def registrar_compra(session):
    produtos = session.execute_write(listar_produtos_para_compra)
    if not produtos:
        print("Não há produtos cadastrados. Cadastre um produto antes de registrar uma compra.")
        return

    print("\nSelecione o produto que deseja comprar:")
    for idx, item in enumerate(produtos, start=1):
        produto = item["produto"]
        vendedor = item["vendedor"]
        print(f"{idx}. Produto: {produto['nome']}, Vendedor: {vendedor['nome']} {vendedor['sobrenome']}")

    while True:
        escolha_produto = input("Digite o número correspondente ao produto: ")
        if escolha_produto.isdigit() and 1 <= int(escolha_produto) <= len(produtos):
            produto_escolhido = produtos[int(escolha_produto) - 1]["produto"]
            produto_id = produto_escolhido.id
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

    usuarios = session.execute_write(listar_usuarios)
    if not usuarios:
        print("Não há usuários cadastrados. Cadastre um usuário antes de registrar uma compra.")
        return

    print("\nSelecione o usuário que está realizando a compra:")
    for idx, usuario in enumerate(usuarios, start=1):
        print(f"{idx}. {usuario['nome']} {usuario['sobrenome']} (Email: {usuario['email']})")

    while True:
        escolha_usuario = input("Digite o número correspondente ao usuário: ")
        if escolha_usuario.isdigit() and 1 <= int(escolha_usuario) <= len(usuarios):
            usuario_escolhido = usuarios[int(escolha_usuario) - 1]
            usuario_id = usuario_escolhido.id
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

    while True:
        quantidade = input("Digite a quantidade desejada: ")
        if quantidade.isdigit() and int(quantidade) > 0:
            quantidade = int(quantidade)
            break
        else:
            print("Quantidade inválida. Por favor, insira um número inteiro positivo.")

    estado = input("Digite o estado da compra (ex: 'Em processamento', 'Enviado', 'Concluído'): ")

    try:
        result = session.write_transaction(
            criar_compra, produto_id, usuario_id, quantidade, estado
        )
        compra = result["c"]
        data_compra = compra["data_compra"].iso_format()
        print(f"Compra registrada com sucesso em {data_compra}!")
    except Exception as e:
        print(f"Erro ao registrar compra: {e}")

def listar_todas_compras(session):
    try:
        compras = session.execute_write(listar_compras)
        if compras:
            print("\nLista de Compras:")
            for item in compras:
                compra = item["compra"]
                usuario = item["usuario"]
                produto = item["produto"]
                data_compra = compra["data_compra"].iso_format()
                print(f"Usuário: {usuario['nome']} {usuario['sobrenome']}, Produto: {produto['nome']}, Quantidade: {compra['quantidade']}, Estado: {compra['estado']}, Data: {data_compra}")
        else:
            print("Nenhuma compra encontrada.")
    except Exception as e:
        print(f"Erro ao listar compras: {e}")


def adicionar_favorito(tx, usuario_id, produto_id):
    query = """
    MATCH (u:Usuario), (p:Produto)
    WHERE ID(u) = $usuario_id AND ID(p) = $produto_id
    CREATE (u)-[:FAVORITOU]->(f:Favorito {data_favorito: datetime()})-[:REFERENCIA]->(p)
    RETURN f, u, p
    """
    result = tx.run(query, usuario_id=usuario_id, produto_id=produto_id)
    return result.single()


def listar_favoritos(tx, usuario_id):
    query = """
    MATCH (u:Usuario)-[:FAVORITOU]->(p:Produto)
    WHERE ID(u) = $usuario_id
    RETURN p
    """
    result = tx.run(query, usuario_id=usuario_id)
    return [record["p"] for record in result]

def adicionar_produto_aos_favoritos(session):
    produtos = session.execute_write(listar_produtos)
    if not produtos:
        print("Não há produtos cadastrados. Cadastre um produto antes de adicionar aos favoritos.")
        return

    print("\nSelecione o produto que deseja adicionar aos favoritos:")
    for idx, item in enumerate(produtos, start=1):
        produto = item["produto"]
        vendedor = item["vendedor"]
        print(f"{idx}. Produto: {produto['nome']}, Vendedor: {vendedor['nome']} {vendedor['sobrenome']}")

    while True:
        escolha_produto = input("Digite o número correspondente ao produto: ")
        if escolha_produto.isdigit() and 1 <= int(escolha_produto) <= len(produtos):
            produto_escolhido = produtos[int(escolha_produto) - 1]["produto"]
            produto_id = produto_escolhido.id
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

    usuarios = session.execute_write(listar_usuarios)
    if not usuarios:
        print("Não há usuários cadastrados. Cadastre um usuário antes de adicionar aos favoritos.")
        return

    print("\nSelecione o usuário que está adicionando o produto aos favoritos:")
    for idx, usuario in enumerate(usuarios, start=1):
        print(f"{idx}. {usuario['nome']} {usuario['sobrenome']} (Email: {usuario['email']})")

    while True:
        escolha_usuario = input("Digite o número correspondente ao usuário: ")
        if escolha_usuario.isdigit() and 1 <= int(escolha_usuario) <= len(usuarios):
            usuario_escolhido = usuarios[int(escolha_usuario) - 1]
            usuario_id = usuario_escolhido.id
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

    try:
        result = session.write_transaction(
            adicionar_favorito, usuario_id, produto_id
        )
        produto = result["p"]
        usuario = result["u"]
        print(f"Produto '{produto['nome']}' adicionado aos favoritos do usuário {usuario['nome']} {usuario['sobrenome']}.")
    except Exception as e:
        print(f"Erro ao adicionar favorito: {e}")

def listar_favoritos_do_usuario(session):
    usuarios = session.execute_write(listar_usuarios)
    if not usuarios:
        print("Não há usuários cadastrados.")
        return

    print("\nSelecione o usuário para ver seus favoritos:")
    for idx, usuario in enumerate(usuarios, start=1):
        print(f"{idx}. {usuario['nome']} {usuario['sobrenome']} (Email: {usuario['email']})")

    while True:
        escolha_usuario = input("Digite o número correspondente ao usuário: ")
        if escolha_usuario.isdigit() and 1 <= int(escolha_usuario) <= len(usuarios):
            usuario_escolhido = usuarios[int(escolha_usuario) - 1]
            usuario_id = usuario_escolhido.id
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

    try:
        favoritos = session.execute_write(listar_favoritos, usuario_id)
        if favoritos:
            print(f"\nProdutos favoritos de {usuario_escolhido['nome']} {usuario_escolhido['sobrenome']}:")
            for produto in favoritos:
                print(f"- {produto['nome']}: {produto['descricao']} (Preço: {produto['preco']})")
        else:
            print("Este usuário não possui produtos favoritos.")
    except Exception as e:
        print(f"Erro ao listar favoritos: {e}")

def main():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session() as session:
            while True:
                print("\nMenu Neo4j:")
                print("1. Criar Usuário")
                print("2. Listar Todos os Usuários")
                print("3. Criar Vendedor")
                print("4. Listar Todos os Vendedores")
                print("5. Criar Produto")
                print("6. Listar Todos os Produtos")
                print("7. Registrar Compra")
                print("8. Listar Todas as Compras")
                print("9. Adicionar Produto aos Favoritos")
                print("10. Listar Favoritos de um Usuário")
                print("11. Sair")
                opcao = input("Selecione uma opção: ")

                if opcao == "1":
                    email = input("Digite o email do usuário: ")
                    nome = input("Digite o nome do usuário: ")
                    sobrenome = input("Digite o sobrenome do usuário: ")
                    username = input("Digite o username do usuário: ")
                    senha = input("Digite a senha do usuário: ")
                    cpf = input("Digite o CPF do usuário: ")
                    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    try:
                        result = session.execute_write(
                            criar_usuario, email, nome, sobrenome, username, hashed_senha, cpf
                        )
                        print(f"Usuário {result['u']['nome']} criado com sucesso!")
                    except Exception as e:
                        print(f"Erro ao criar usuário: {e}")

                elif opcao == "2":
                    try:
                        usuarios = session.execute_write(listar_usuarios)
                        if usuarios:
                            print("\nLista de Usuários:")
                            for u in usuarios:
                                print(f"Nome: {u['nome']}, Email: {u['email']}, Username: {u['username']}")
                        else:
                            print("Nenhum usuário encontrado.")
                    except Exception as e:
                        print(f"Erro ao listar usuários: {e}")

                elif opcao == "3":
                    nome = input("Digite o nome do vendedor: ")
                    sobrenome = input("Digite o sobrenome do vendedor: ")
                    cpf = input("Digite o CPF do vendedor: ")

                    try:
                        result = session.execute_write(
                            criar_vendedor, nome, sobrenome, cpf
                        )
                        print(f"Vendedor {result['v']['nome']} criado com sucesso!")
                    except Exception as e:
                        print(f"Erro ao criar vendedor: {e}")

                elif opcao == "4":
                    try:
                        vendedores = session.execute_write(listar_vendedores)
                        if vendedores:
                            print("\nLista de Vendedores:")
                            for v in vendedores:
                                print(f"Nome: {v['nome']} {v['sobrenome']}, CPF: {v['cpf']}")
                        else:
                            print("Nenhum vendedor encontrado.")
                    except Exception as e:
                        print(f"Erro ao listar vendedores: {e}")

                elif opcao == "5":
                    nome = input("Digite o nome do produto: ")
                    descricao = input("Digite a descrição do produto: ")
                    try:
                        preco = float(input("Digite o preço do produto: "))
                    except ValueError:
                        print("Preço inválido. Por favor, insira um número.")
                        continue

                    vendedores = session.execute_write(listar_vendedores_com_indices)
                    if not vendedores:
                        print("Não há vendedores cadastrados. Cadastre um vendedor antes de criar um produto.")
                        continue

                    print("\nSelecione o vendedor associado ao produto:")
                    for idx, vendedor in enumerate(vendedores, start=1):
                        print(f"{idx}. {vendedor['nome']} {vendedor['sobrenome']} (CPF: {vendedor['cpf']})")

                    while True:
                        escolha = input("Digite o número correspondente ao vendedor: ")
                        if escolha.isdigit() and 1 <= int(escolha) <= len(vendedores):
                            vendedor_escolhido = vendedores[int(escolha) - 1]
                            vendedor_id = vendedor_escolhido.id  
                            break
                        else:
                            print("Opção inválida. Por favor, tente novamente.")

                    try:
                        result = session.write_transaction(
                            criar_produto, nome, descricao, preco, vendedor_id
                        )
                        produto = result["p"]
                        vendedor = result["v"]
                        print(f"Produto '{produto['nome']}' criado e vinculado ao vendedor {vendedor['nome']} {vendedor['sobrenome']}.")
                    except Exception as e:
                        print(f"Erro ao criar produto: {e}")

                elif opcao == "6":
                    try:
                        produtos = session.execute_write(listar_produtos)
                        if produtos:
                            print("\nLista de Produtos:")
                            for item in produtos:
                                produto = item["produto"]
                                vendedor = item["vendedor"]
                                print(f"Produto: {produto['nome']}, Descrição: {produto['descricao']}, Preço: {produto['preco']}, Vendedor: {vendedor['nome']} {vendedor['sobrenome']}")
                        else:
                            print("Nenhum produto encontrado.")
                    except Exception as e:
                        print(f"Erro ao listar produtos: {e}")

                elif opcao == "7":
                    registrar_compra(session)

                elif opcao == "8":
                    listar_todas_compras(session)

                elif opcao == "9":
                    adicionar_produto_aos_favoritos(session)

                elif opcao == "10":
                    listar_favoritos_do_usuario(session)

                elif opcao == "11":
                    print("Saindo do programa.")
                    break
                else:
                    print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()