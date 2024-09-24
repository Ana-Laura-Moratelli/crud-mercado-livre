import json
from bson.objectid import ObjectId

def listar_vendedor(db):
    mycol = db.vendedor
    vendedores = list(mycol.find())

    if not vendedores:
        print("Nenhum vendedor encontrado.")
        return None

    print("\nLista de vendedores:")
    for i, vendedor in enumerate(vendedores, 1):
        print(f"{i}. {vendedor['nome']} {vendedor['sobrenome']} (CPF: {vendedor['cpf']})")

    while True:
        try:
            escolha = int(input("Digite o número do vendedor que deseja selecionar: "))
            if 1 <= escolha <= len(vendedores):
                return vendedores[escolha - 1]
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def validar_cpf(cpf):
    """Valida se o CPF possui 11 dígitos numéricos."""
    return cpf.isdigit() and len(cpf) == 11

def cpf_existe(db, cpf):
    """Verifica se o CPF já existe na coleção de vendedores."""
    return db.vendedor.find_one({"cpf": cpf}) is not None

def create_vendedor(db):
    mycol = db.vendedor
    print("\nInserindo um novo vendedor")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")

    while True:
        cpf = input("CPF (11 dígitos): ")
        if validar_cpf(cpf):
            if not cpf_existe(db, cpf):
                break
            else:
                print("CPF já existe. Tente um CPF diferente.")
        else:
            print("CPF inválido. Deve conter exatamente 11 números.")

    vendedor = {"nome": nome, "sobrenome": sobrenome, "cpf": cpf}
    x = mycol.insert_one(vendedor)
    print(f"Vendedor inserido com sucesso. ID: {x.inserted_id}")
    
def read_vendedor(db):
    mycol_vendedor = db.vendedor
    mycol_produto = db.produto

    vendedores = list(mycol_vendedor.find())

    if not vendedores:
        print("Nenhum vendedor encontrado.")
        return None

    print("\nLista de vendedores:")
    for i, vendedor in enumerate(vendedores, 1):
        print(f"{i}. {vendedor['nome']} {vendedor['sobrenome']} (CPF: {vendedor['cpf']})")

    while True:
        try:
            escolha = int(input("Digite o número do vendedor que deseja selecionar: "))
            if 1 <= escolha <= len(vendedores):
                vendedor_selecionado = vendedores[escolha - 1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    vendedor_selecionado['_id'] = str(vendedor_selecionado['_id'])

    produtos_vendedor = list(mycol_produto.find({"vendedor_id": ObjectId(vendedor_selecionado['_id'])}))

    produtos_detalhes = []
    if produtos_vendedor:
        for produto in produtos_vendedor:
            produtos_detalhes.append({
                "produto_id": str(produto["_id"]),
                "nome": produto["nome"],
                "descricao": produto["descricao"],
                "quantidade": produto["quantidade"]
            })
    else:
        print("Nenhum produto encontrado para o vendedor.")

    vendedor_selecionado['produtos'] = produtos_detalhes

    print("Dados do vendedor selecionado:")
    print(json.dumps(vendedor_selecionado, indent=4))

    return vendedor_selecionado

def update_vendedor(db):
    vendedor = listar_vendedor(db)
    if not vendedor:
        return

    print("Dados do vendedor selecionado:", vendedor)

    mycol = db.vendedor
    myquery = {"_id": vendedor["_id"]}

    while True:
        print("\nEscolha uma opção para alterar:")
        print("1. Alterar Nome")
        print("2. Alterar Sobrenome")
        print("3. Alterar CPF")
        print("4. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == "1":
            novo_nome = input("Novo Nome: ")
            if novo_nome and novo_nome != vendedor["nome"]:
                vendedor["nome"] = novo_nome
                print("Nome atualizado.")
        elif opcao == "2":
            novo_sobrenome = input("Novo Sobrenome: ")
            if novo_sobrenome and novo_sobrenome != vendedor["sobrenome"]:
                vendedor["sobrenome"] = novo_sobrenome
                print("Sobrenome atualizado.")
        elif opcao == "3":
            while True:
                novo_cpf = input("Novo CPF (11 dígitos): ")
                if validar_cpf(novo_cpf):
                    if not cpf_existe(db, novo_cpf) or novo_cpf == vendedor["cpf"]:
                        vendedor["cpf"] = novo_cpf
                        print("CPF atualizado.")
                        break
                    else:
                        print("CPF já existe. Tente um CPF diferente.")
                else:
                    print("CPF inválido. Deve conter exatamente 11 números.")
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

    newvalues = {"$set": vendedor}
    mycol.update_one(myquery, newvalues)
    print("Dados atualizados com sucesso.")

def delete_vendedor(db):
    vendedor = listar_vendedor(db)
    if not vendedor:
        return

    mycol_vendedor = db.vendedor
    mycol_produto = db.produto  

    myquery = {"_id": vendedor["_id"]}
    result = mycol_vendedor.delete_one(myquery)
    
    if result.deleted_count > 0:
        print(f"Vendedor {vendedor['nome']} {vendedor['sobrenome']} deletado com sucesso.")
        
        produto_query = {"vendedor_id": vendedor["_id"]}
        produtos_result = mycol_produto.delete_many(produto_query)
        
        print(f"{produtos_result.deleted_count} produtos relacionados ao vendedor foram deletados.")
    else:
        print(f"Vendedor {vendedor['nome']} {vendedor['sobrenome']} não encontrado.")

