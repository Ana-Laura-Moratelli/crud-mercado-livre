import json

nome = input("Nome: ")
sobrenome = input("Sobrenome: ")
end = [] #isso é uma lista
card = []

key = 1
key = 2

while (key != 'N'):
    rua = input("Rua: ")
    num = input("Num: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP: ")
    numero = input("Número: ")
    validade = input("Validade: ")
    cvc = input("CVC: ")
    nomeCard = input("Nome: ")

    endereco = {        #isso nao eh json, isso é chave-valor, eh um obj
        "rua":rua,
        "num": num,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "cep": cep
    }
       
    dados = {
        "numero": numero,
        "validade": validade,
        "cvc": cvc,
        "nomeCard": nomeCard,
    }
    end.append(endereco) #estou inserindo na lista
    card.append(dados)

    key = input("Deseja cadastrar um novo endereço (S/N)? ")
    key = input("Deseja cadastrar um novo cartão (S/N)? ")

usuario = {  #estou montando o obj final
    "nome" : nome,
    "sobrenome" : sobrenome,
    "enderecos" : end, 
    "dados" : card,
}
print(json.dumps(usuario)) #estou transformando um obj em json (texto)

def delete_usuario(nome, sobrenome):
    #Delete
    global db
    mycol = db.usuario
    myquery = {"nome": nome, "sobrenome":sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)

def create_usuario():
    #Insert
    global db
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    key = 1
    end = []
    while (key != 'N'):
        print("Endereço:")
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {        #isso nao eh json, isso é chave-valor, eh um obj
            "rua":rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco) #estou inserindo na lista
        key = input("Deseja cadastrar um novo endereço (S/N)? ")

    key = 2
    card = []
    while (key != 'N'):
        print("Cadastrar cartão:")
        numero = input("Número: ")
        validade = input("Validade: ")
        cvc = input("CVC: ")
        nomeCard = input("Nome: ")
        dados = {        #isso nao eh json, isso é chave-valor, eh um obj
            "numero":numero,
            "validade": validade,
            "cvc": cvc,
            "nomeCard": nomeCard,
        }
        card.append(dados) #estou inserindo na lista
        key= input("Deseja cadastrar um novo cartão (S/N)? ")


    mydoc = { "nome": nome, "sobrenome": sobrenome, "cpf": cpf, "end": end, "card": card}
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_usuario(nome):
    #Read
    global db
    mycol = db.usuario
    print("Usuários existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(x["nome"],x["cpf"])
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def listar_usuarios():
    # Read
    global db
    mycol = db.usuario
    usuarios = list(mycol.find())  # Buscar todos os usuários

    if not usuarios:
        print("Nenhum usuário encontrado.")
        return None

    print("\nLista de usuários:")
    for i, usuario in enumerate(usuarios, 1):  # Enumerar usuários a partir de 1
        print(f"{i}. {usuario['nome']}")

    while True:
        try:
            escolha = int(input("Digite o número do usuário que deseja alterar: "))
            if 1 <= escolha <= len(usuarios):
                return usuarios[escolha - 1]  # Retorna o usuário selecionado com base no número
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def update_usuario():
    # Listar e selecionar o usuário
    usuario = listar_usuarios()  # Chama a função que lista e seleciona o usuário
    if not usuario:
        return  # Se nenhum usuário foi selecionado, encerra

    print("Dados do usuário selecionado:", usuario)

    mycol = db.usuario
    myquery = {"_id": usuario["_id"]}  # Usa o ID para identificar o documento correto

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
                usuario["nome"] = nome
                print("Nome atualizado.")
        elif opcao == "2":
            sobrenome = input("Novo Sobrenome: ")
            if len(sobrenome):
                usuario["sobrenome"] = sobrenome
                print("Sobrenome atualizado.")
        elif opcao == "3":
            cpf = input("Novo CPF: ")
            if len(cpf):
                usuario["cpf"] = cpf
                print("CPF atualizado.")
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")


    # Atualizar os dados no banco de dados
    newvalues = {"$set": usuario}
    mycol.update_one(myquery, newvalues)
    print("Dados atualizados com sucesso.")
