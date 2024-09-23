import json
from bson import ObjectId
from vendedor import listar_vendedor

def listar_produtos(db):
    mycol_produto = db.produto
    produtos = list(mycol_produto.find())

    if not produtos:
        print("Nenhum produto encontrado.")
        return None

    print("\nLista de produtos:")
    for i, produto in enumerate(produtos, 1):
        print(f"{i}. {produto['nome']} - Nome do vendedor: {produto['vendedor_nome']}")

    return produtos


def create_produto(db):
    mycol_produto = db.produto
    mycol_vendedor = db.vendedor

    print("\nInserindo um novo produto")


    # Listar e selecionar um vendedor
    vendedor = listar_vendedor(db)
    if not vendedor:
        print("Nenhum vendedor disponível. Produto não pode ser criado sem um vendedor.")
        return
    
    # Coletar os dados do produto
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    preco = input("Preço: ")
    quantidade = input("Quantidade: ")

    # Criar o documento do produto com a associação ao vendedor
    produto = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "quantidade": quantidade,
        "vendedor_id": vendedor["_id"],  # Associando o ID do vendedor
        "vendedor_nome": f"{vendedor['nome']} {vendedor['sobrenome']}"  # Nome do vendedor
    }

    # Inserir o produto no banco de dados
    x = mycol_produto.insert_one(produto)
    print(f"Produto inserido com sucesso. ID: {x.inserted_id}")

def read_produto(db, nome=None):
    mycol_produto = db.produto

    print("\nProdutos existentes: ")
    if not nome:
        produtos = mycol_produto.find().sort("nome")
        for produto in produtos:
            print(f"{produto['nome']} - Nome do vendedor: {produto['vendedor_nome']}")
    else:
        myquery = {"nome": nome}
        produtos = mycol_produto.find(myquery)
        if produtos.count() == 0:
            print("Nenhum produto encontrado.")
        else:
            for produto in produtos:
                print(f"{produto['nome']} -  Nome do vendedor: {produto['vendedor_nome']}")

def update_produto(db):
    mycol_produto = db.produto

    # Listar produtos com índice
    produtos = listar_produtos(db)
    if not produtos:
        return

    while True:
        try:
            escolha = int(input("Digite o número do produto que deseja atualizar: "))
            if 1 <= escolha <= len(produtos):
                produto_selecionado = produtos[escolha - 1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    print("\nDados do produto selecionado:", produto_selecionado)

    while True:
        print("\nEscolha o que deseja alterar:")
        print("1. Alterar Nome")
        print("2. Alterar Descrição")
        print("3. Alterar Quantidade")
        print("4. Alterar Vendedor")
        print("5. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == "1":
            novo_nome = input("Novo Nome: ")
            if novo_nome:
                produto_selecionado["nome"] = novo_nome
                print("Nome atualizado.")

        elif opcao == "2":
            nova_descricao = input("Nova Descrição: ")
            if nova_descricao:
                produto_selecionado["descricao"] = nova_descricao
                print("Descrição atualizada.")

        elif opcao == "3":
            nova_quantidade = input("Nova Quantidade: ")
            if nova_quantidade:
                produto_selecionado["quantidade"] = nova_quantidade
                print("Quantidade atualizada.")

        elif opcao == "4":
            print("\nListando vendedores disponíveis para alteração:")
            vendedor = listar_vendedor(db)
            if vendedor:
                produto_selecionado["vendedor_id"] = vendedor["_id"]
                produto_selecionado["vendedor_nome"] = f"{vendedor['nome']} {vendedor['sobrenome']}"
                print("Vendedor atualizado.")

        elif opcao == "5":
            break

        else:
            print("Opção inválida. Tente novamente.")

    # Atualizar os dados no banco de dados
    myquery = {"_id": produto_selecionado["_id"]}
    newvalues = {"$set": produto_selecionado}
    mycol_produto.update_one(myquery, newvalues)
    print("Produto atualizado com sucesso.")

def delete_produto(db):
    # Listar produtos com índice
    produtos = listar_produtos(db)
    if not produtos:
        print("Nenhum produto disponível para exclusão.")
        return

    while True:
        try:
            escolha = int(input("Digite o número do produto que deseja selecionar: "))
            if 1 <= escolha <= len(produtos):
                produto_selecionado = produtos[escolha - 1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    mycol_produto = db.produto
    myquery = {"_id": produto_selecionado["_id"]}
    result = mycol_produto.delete_one(myquery)
    
    if result.deleted_count > 0:
        print(f"Produto {produto_selecionado['nome']} deletado com sucesso.")
    else:
        print(f"Produto {produto_selecionado['nome']} não encontrado.")
