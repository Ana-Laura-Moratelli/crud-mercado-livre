import json

nome= input("Nome: ")
sobrenome = input("Sobrenome: ")
cpf = input("CPF: ")

vendedor = {  #estou montando o obj final
    "nome" : nome,
    "sobrenome" : sobrenome,
    "cpf" : cpf,
}
print(json.dumps(vendedor)) #estou transformando um obj em json (texto)

def listar_vendedor():
    # Read
    global db
    mycol = db.vendedor
    vendedores = list(mycol.find())  # Buscar todos os usuários

    if not vendedor:
        print("Nenhum vendedor encontrado.")
        return None

    print("\nLista de vendedores:")
    for i, vendedor in enumerate(vendedores, 1):  # Enumerar usuários a partir de 1
        print(f"{i}. {vendedor['nome']}")

    while True:
        try:
            escolha = int(input("Digite o número do vendedor que deseja alterar: "))
            if 1 <= escolha <= len(vendedores):
                return vendedor[escolha - 1]  # Retorna o usuário selecionado com base no número
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def update_vendedor():
    # Listar e selecionar o usuário
    vendedor = listar_vendedor()
    if not vendedor:
        return  # Nenhum usuário foi selecionado

    print("Dados do vendedor selecionado:", vendedor)

    mycol = db.vendedor
    myquery = {"_id": vendedor["_id"]}  # Usa o ID para identificar o documento correto

    while True:
        print("\nEscolha uma opção para alterar:")
        print("1. Alterar Nome")
        print("2. Alterar Sobrenome")
        print("3. Alterar CPF")
        print("4. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == "1":
            nome = input("Novo Nome: ")
            if len(nome):
                vendedor["nome"] = nome
                print("Nome atualizado.")
        elif opcao == "2":
            sobrenome = input("Novo Sobrenome: ")
            if len(sobrenome):
                vendedor["sobrenome"] = sobrenome
                print("Sobrenome atualizado.")
        elif opcao == "3":
            cpf = input("Novo CPF: ")
            if len(cpf):
                vendedor["cpf"] = cpf
                print("CPF atualizado.")
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

    # Atualizar os dados no banco de dados
    newvalues = {"$set": vendedor}
    mycol.update_one(myquery, newvalues)
    print("Dados atualizados com sucesso.")

def delete_vendedor(nome, sobrenome):
    #Delete
    global db
    mycol = db.vendedor
    myquery = {"nome": nome, "sobrenome":sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o vendedor ",mydoc)

def create_vendedor():
    #Insert
    global db
    mycol = db.vendedor
    print("\nInserindo um novo vendedor")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")

    mydoc = { "nome": nome, "sobrenome": sobrenome, "cpf": cpf}
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_vendedor(nome):
    #Read
    global db
    mycol = db.vendedor
    print("Vendedores existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(x["nome"],x["cpf"])
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_vendedor(nome):
    #Read
    global db
    mycol = db.vendedor
    myquery = {"nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do vendedor: ",mydoc)
    nome = input("Mudar Nome:")
    if len(nome):
        mydoc["nome"] = nome

    sobrenome = input("Mudar Sobrenome:")
    if len(sobrenome):
        mydoc["sobrenome"] = sobrenome

    cpf = input("Mudar CPF:")
    if len(cpf):
        mydoc["cpf"] = cpf

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)
