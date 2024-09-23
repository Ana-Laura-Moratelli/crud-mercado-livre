import json

def listar_usuarios(db):
    mycol = db.usuario
    usuarios = list(mycol.find())

    if not usuarios:
        print("Nenhum usuário encontrado.")
        return None

    print("\nLista de usuários:")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nome']} {usuario['sobrenome']} (CPF: {usuario.get('cpf', '')})")

    while True:
        try:
            escolha = int(input("Digite o número do usuário que deseja selecionar: "))
            if 1 <= escolha <= len(usuarios):
                return usuarios[escolha - 1] 
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def create_usuario(db):
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")

    enderecos = []
    while True:
        print("Cadastro de Endereço:")
        rua = input("Rua: ")
        num = input("Número: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")

        endereco = {
            "rua": rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        enderecos.append(endereco)

        key = input("Deseja cadastrar outro endereço? (S/N): ").upper()
        if key == 'N':
            break

    cartoes = []
    while True:
        print("Cadastro de Cartão:")
        numero = input("Número do Cartão: ")
        validade = input("Validade (MM/AA): ")
        cvc = input("CVC: ")
        nome_card = input("Nome do Titular: ")

        cartao = {
            "numero": numero,
            "validade": validade,
            "cvc": cvc,
            "nomeCard": nome_card
        }
        cartoes.append(cartao)

        key = input("Deseja cadastrar outro cartão? (S/N): ").upper()
        if key == 'N':
            break

    usuario = {"nome": nome, "sobrenome": sobrenome, "cpf": cpf, "enderecos": enderecos, "cartoes": cartoes}
    x = mycol.insert_one(usuario)
    print("Usuário inserido com sucesso. ID:", x.inserted_id)

def read_usuario(db):
    mycol = db.usuario
    usuarios = list(mycol.find())
    
    if not usuarios:
        print("Nenhum usuário encontrado.")
        return None

    print("\nLista de usuários:")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nome']}")

    while True:
        try:
            escolha = int(input("Digite o número do usuário que deseja selecionar: "))
            if 1 <= escolha <= len(usuarios):
                usuario_selecionado = usuarios[escolha - 1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    usuario_selecionado['_id'] = str(usuario_selecionado['_id'])

    print("Dados do usuário selecionado:")
    print(json.dumps(usuario_selecionado, indent=4))

def update_usuario(db):
    usuario = listar_usuarios(db)
    if not usuario:
        return

    print("Dados do usuário selecionado:", usuario)

    mycol = db.usuario
    myquery = {"_id": usuario["_id"]}

    while True:
        print("\nEscolha uma opção para alterar:")
        print("1. Alterar Nome")
        print("2. Alterar Sobrenome")
        print("3. Alterar CPF")
        print("4. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == "1":
            novo_nome = input("Novo Nome: ")
            if novo_nome and novo_nome != usuario["nome"]:
                usuario["nome"] = novo_nome
                print("Nome atualizado.")
        elif opcao == "2":
            novo_sobrenome = input("Novo Sobrenome: ")
            if novo_sobrenome and novo_sobrenome != usuario["sobrenome"]:
                usuario["sobrenome"] = novo_sobrenome
                print("Sobrenome atualizado.")
        elif opcao == "3":
            novo_cpf = input("Novo CPF: ")
            if novo_cpf and novo_cpf != usuario["cpf"]:
                usuario["cpf"] = novo_cpf
                print("CPF atualizado.")
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

    newvalues = {"$set": usuario}
    mycol.update_one(myquery, newvalues)
    print("Dados atualizados com sucesso.")

def delete_usuario(db):
    usuario = listar_usuarios(db)
    if not usuario:
        return

    mycol_usuario = db.usuario
    mycol_favoritos = db.favoritos  

    myquery = {"_id": usuario["_id"]}
    result = mycol_usuario.delete_one(myquery)
    
    if result.deleted_count > 0:
        print(f"Usuário {usuario['nome']} {usuario['sobrenome']} deletado com sucesso.")
        
        favoritos_query = {"usuario_id": usuario["_id"]}
        favoritos_result = mycol_favoritos.delete_many(favoritos_query)
        
        print(f"{favoritos_result.deleted_count} favoritos deletados para o usuário {usuario['nome']}.")
    else:
        print("Erro ao deletar o usuário.")