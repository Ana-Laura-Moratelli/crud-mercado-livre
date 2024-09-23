import json
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

    print("\nInserindo um novo produto")

    vendedor = listar_vendedor(db)
    if not vendedor:
        return
    
    nome = input("Nome: ")
    descricao = input("Descrição: ")

    while True:
        try:
            preco = float(input("Preço: "))
            if preco >= 0:
                preco_formatado = f"{preco:.2f}"  
                break
            else:
                print("Preço inválido. Deve ser maior ou igual a zero.")
        except ValueError:
            print("Entrada inválida. Digite um valor numérico para o preço.")
    
    while True:
        try:
            quantidade = int(input("Quantidade: "))
            if quantidade >= 0:
                break
            else:
                print("Quantidade inválida. Deve ser maior ou igual a zero.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    produto = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco_formatado,  
        "quantidade": quantidade,
        "vendedor_id": vendedor["_id"],  
        "vendedor_nome": f"{vendedor['nome']} {vendedor['sobrenome']}"
    }

    x = mycol_produto.insert_one(produto)
    print(f"Produto inserido com sucesso. ID: {x.inserted_id}")

def read_produto(db):
    mycol_produto = db.produto
    mycol_vendedor = db.vendedor

    produtos = list(mycol_produto.find())
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    print("\nLista de produtos:")
    for i, produto in enumerate(produtos, 1):
        vendedor = mycol_vendedor.find_one({"_id": produto["vendedor_id"]})
        vendedor_nome = f"{vendedor['nome']} {vendedor['sobrenome']}" if vendedor else "Desconhecido"
        
        print(f"{i}. {produto['nome']} - Nome do vendedor: {vendedor_nome}")

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

    vendedor = mycol_vendedor.find_one({"_id": produto_selecionado["vendedor_id"]})
    vendedor_nome = f"{vendedor['nome']} {vendedor['sobrenome']}" if vendedor else "Desconhecido"

    produto_selecionado['_id'] = str(produto_selecionado['_id'])
    produto_selecionado['vendedor_id'] = str(produto_selecionado['vendedor_id'])
    produto_selecionado['vendedor_nome'] = vendedor_nome

    print("\nDados do produto selecionado:")
    print(json.dumps(produto_selecionado, indent=4))

def update_produto(db):
    mycol_produto = db.produto

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
        print("4. Alterar Preço")
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
            while True:
                try:
                    nova_quantidade = int(input("Nova Quantidade: "))
                    if nova_quantidade >= 0:
                        produto_selecionado["quantidade"] = nova_quantidade
                        print("Quantidade atualizada.")
                        break
                    else:
                        print("Quantidade inválida. Deve ser maior ou igual a zero.")
                except ValueError:
                    print("Entrada inválida. Digite um número inteiro.")

        elif opcao == "4":
            while True:
                try:
                    novo_preco = float(input("Novo preço: "))
                    if novo_preco >= 0:
                        produto_selecionado["preco"] = f"{novo_preco:.2f}"
                        print("Preço atualizado.")
                        break
                    else:
                        print("Preço inválido. Deve ser maior ou igual a zero.")
                except ValueError:
                    print("Entrada inválida. Digite um valor numérico para o preço.")

        elif opcao == "5":
            break

        else:
            print("Opção inválida. Tente novamente.")

    myquery = {"_id": produto_selecionado["_id"]}
    newvalues = {"$set": produto_selecionado}
    mycol_produto.update_one(myquery, newvalues)
    print("Produto atualizado com sucesso.")


def delete_produto(db):
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
