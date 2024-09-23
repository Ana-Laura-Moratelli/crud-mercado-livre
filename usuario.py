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

def validar_cpf(cpf):
    """Valida se o CPF possui 11 dígitos numéricos."""
    return cpf.isdigit() and len(cpf) == 11

def cpf_existe(db, cpf):
    """Verifica se o CPF já existe na coleção de usuários."""
    return db.usuario.find_one({"cpf": cpf}) is not None

def validar_cartao(numero, validade, cvc):
    """Valida o número do cartão, validade e CVC."""
    return (numero.isdigit() and len(numero) == 16 and
            validade.count('/') == 1 and 
            len(validade.split('/')[0]) == 2 and 
            len(validade.split('/')[1]) == 2 and 
            cvc.isdigit() and len(cvc) == 3)

def validar_endereco(num):
    """Valida se o número do endereço é um número."""
    return num.isdigit()

def validar_cep(cep):
    """Valida se o CEP possui 8 dígitos numéricos."""
    return cep.isdigit() and len(cep) == 8

def create_usuario(db):
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    
    while True:
        cpf = input("CPF (11 dígitos): ")
        if validar_cpf(cpf) and not cpf_existe(db, cpf):
            break
        else:
            print("CPF inválido ou já cadastrado. Tente novamente.")

    enderecos = []
    while True:
        print("Cadastro de Endereço:")
        rua = input("Rua: ")
        num = input("Número: ")
        if not validar_endereco(num):
            print("Número do endereço deve ser um valor numérico. Tente novamente.")
            continue
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        
        while True:
            cep = input("CEP (8 dígitos): ")
            if validar_cep(cep):
                break
            else:
                print("CEP inválido. Tente novamente.")

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
        while True:
            numero = input("Número do Cartão (16 dígitos): ")
            validade = input("Validade (MM/AA): ")
            cvc = input("CVC (3 dígitos): ")
            if validar_cartao(numero, validade, cvc):
                break
            else:
                print("Dados do cartão inválidos. Tente novamente.")

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
        print("4. Alterar Endereços")
        print("5. Alterar Cartões")
        print("6. Sair")

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
            while True:
                novo_cpf = input("Novo CPF (11 dígitos): ")
                if validar_cpf(novo_cpf) and (not cpf_existe(db, novo_cpf) or novo_cpf == usuario["cpf"]):
                    usuario["cpf"] = novo_cpf
                    print("CPF atualizado.")
                    break
                else:
                    print("CPF inválido ou já cadastrado. Tente novamente.")
        elif opcao == "4":
            while True:
                print("Endereços cadastrados:")
                for idx, end in enumerate(usuario["enderecos"]):
                    print(f"{idx + 1}. {end['rua']}, {end['num']} - {end['bairro']}")

                idx = int(input("Escolha o número do endereço para alterar (ou 0 para sair): "))
                if idx == 0:
                    break
                if 1 <= idx <= len(usuario["enderecos"]):
                    end = usuario["enderecos"][idx - 1]
                    print("Dados do endereço selecionado:", end)

                    while True:
                        print("\nEscolha o que deseja alterar:")
                        print("1. Alterar Rua")
                        print("2. Alterar Número")
                        print("3. Alterar Bairro")
                        print("4. Alterar Cidade")
                        print("5. Alterar Estado")
                        print("6. Alterar CEP")
                        print("7. Sair")

                        opcao_endereco = input("Digite o número da opção: ")

                        if opcao_endereco == "1":
                            end["rua"] = input("Nova Rua: ") or end["rua"]
                        elif opcao_endereco == "2":
                            while True:
                                num = input("Novo Número: ")
                                if validar_endereco(num):
                                    end["num"] = num
                                    break
                                else:
                                    print("Número inválido. Tente novamente.")
                        elif opcao_endereco == "3":
                            end["bairro"] = input("Novo Bairro: ") or end["bairro"]
                        elif opcao_endereco == "4":
                            end["cidade"] = input("Nova Cidade: ") or end["cidade"]
                        elif opcao_endereco == "5":
                            end["estado"] = input("Novo Estado: ") or end["estado"]
                        elif opcao_endereco == "6":
                            while True:
                                cep = input("Novo CEP (8 dígitos): ")
                                if validar_cep(cep):
                                    end["cep"] = cep
                                    break
                                else:
                                    print("CEP inválido. Tente novamente.")
                        elif opcao_endereco == "7":
                            break
                        else:
                            print("Opção inválida. Tente novamente.")
                    
                    print("Endereço atualizado.")
                else:
                    print("Endereço inválido.")
        elif opcao == "5":
            while True:
                print("Cartões cadastrados:")
                for idx, card in enumerate(usuario["cartoes"]):
                    print(f"{idx + 1}. {card['numero']} - {card['nomeCard']}")

                idx = int(input("Escolha o número do cartão para alterar (ou 0 para sair): "))
                if idx == 0:
                    break
                if 1 <= idx <= len(usuario["cartoes"]):
                    card = usuario["cartoes"][idx - 1]
                    print("Dados do cartão selecionado:", card)

                    while True:
                        print("\nEscolha o que deseja alterar:")
                        print("1. Alterar Número do Cartão")
                        print("2. Alterar Validade")
                        print("3. Alterar CVC")
                        print("4. Sair")

                        opcao_cartao = input("Digite o número da opção: ")

                        if opcao_cartao == "1":
                            while True:
                                numero = input("Novo Número do Cartão (16 dígitos): ")
                                if len(numero) == 16 and numero.isdigit():
                                    card["numero"] = numero
                                    break
                                else:
                                    print("Número do cartão inválido. Tente novamente.")
                        elif opcao_cartao == "2":
                            validade = input("Nova Validade (MM/AA): ")
                            card["validade"] = validade  # Adicionar validação se necessário
                        elif opcao_cartao == "3":
                            cvc = input("Novo CVC (3 dígitos): ")
                            card["cvc"] = cvc  # Adicionar validação se necessário
                        elif opcao_cartao == "4":
                            break
                        else:
                            print("Opção inválida. Tente novamente.")
                    
                    print("Cartão atualizado.")
                else:
                    print("Cartão inválido.")
        elif opcao == "6":
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