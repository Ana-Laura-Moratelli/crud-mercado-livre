import json
import bcrypt
from bson.objectid import ObjectId

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

def cpf_existe(db, cpf):
    """Verifica se o CPF já existe na coleção de usuários."""
    return db.usuario.find_one({"cpf": cpf}) is not None

def username_existe(db, username):
    return db.usuario.find_one({"username": username}) is not None

def create_senha():
    while True:
        senha = input("Crie uma senha (mínimo 8 caracteres, incluindo letras e números): ")
        if len(senha) >= 8 and any(char.isdigit() for char in senha) and any(char.isalpha() for char in senha):
            senha_confirma = input("Confirme a senha: ")
            if senha == senha_confirma:
                senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                return senha_hashed
            else:
                print("As senhas não coincidem. Tente novamente.")
        else:
            print("A senha deve ter no mínimo 8 caracteres e incluir letras e números.")

def create_usuario(db):
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    
    while True:
        username = input("Username: ")
        if not username_existe(db, username):
            break
        else:
            print("Username já cadastrado. Tente novamente com outro.")

    senha = create_senha()
    
    while True:
        cpf = input("CPF (11 dígitos): ")
        if validar_cpf(cpf) and not cpf_existe(db, cpf):
            break
        else:
            print("CPF inválido ou já cadastrado. Tente novamente.")

    # Cadastro de Endereço
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

    # Cadastro  Cartões
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

    usuario = {
        "nome": nome, 
        "sobrenome": sobrenome, 
        "username": username, 
        "senha": senha,  
        "cpf": cpf, 
        "enderecos": enderecos, 
        "cartoes": cartoes
    }
    x = mycol.insert_one(usuario)
    print("Usuário inserido com sucesso. ID:", x.inserted_id)

def read_usuario(db):
    mycol = db.usuario
    mycol_produto = db.produto
    mycol_compra = db.compra

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

    def convert_objectid(data):
        if isinstance(data, ObjectId):
            return str(data)
        elif isinstance(data, dict):
            return {k: convert_objectid(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [convert_objectid(i) for i in data]
        elif isinstance(data, bytes):
            return data.decode("utf-8", "ignore")  
        else:
            return data

    favoritos_ids = usuario_selecionado.get("favoritos", [])
    favoritos_detalhes = []

    if favoritos_ids:
        valid_favoritos_ids = []
        for fav in favoritos_ids:
            if isinstance(fav, dict) and 'produto_id' in fav:
                valid_favoritos_ids.append(fav['produto_id'])
            else:
                print(f"ID inválido encontrado nos favoritos: {fav}")

        if valid_favoritos_ids:
            favoritos_produtos = list(mycol_produto.find({"_id": {"$in": [ObjectId(fav_id) for fav_id in valid_favoritos_ids]}}))
            favoritos_detalhes = [{"produto_id": str(produto["_id"]), "nome": produto["nome"]} for produto in favoritos_produtos]

    usuario_selecionado["favoritos"] = favoritos_detalhes

    compras_usuario = list(mycol_compra.find({"usuario_id": usuario_selecionado["_id"]}))
    compras_detalhadas = []

    for compra in compras_usuario:
        produto = mycol_produto.find_one({"_id": ObjectId(compra["produto_id"])})
        if produto:
            compra_detalhe = {
                "produto_id": str(produto["_id"]),
                "nome_produto": produto["nome"],
                "quantidade": compra["quantidade"],
                "estado": compra["estado"],
                "data_compra": compra["data_compra"],
                "_id": str(compra["_id"])
            }
            compras_detalhadas.append(compra_detalhe)
        else:
            print(f"Produto não encontrado para a compra: {compra}")

    usuario_selecionado["compras"] = compras_detalhadas

    usuario_selecionado = convert_objectid(usuario_selecionado)

    print("Dados do usuário selecionado:")
    print(json.dumps(usuario_selecionado, indent=4))

def uptade_senha(usuario):
    print("Atualização de Senha:")
    while True:
        senha_atual = input("Digite a senha atual: ")
        if bcrypt.checkpw(senha_atual.encode('utf-8'), usuario["senha"]):
            while True:
                nova_senha = input("Nova Senha (mínimo 8 caracteres, incluindo letras e números): ")
                if len(nova_senha) >= 8 and any(char.isdigit() for char in nova_senha) and any(char.isalpha() for char in nova_senha):
                    confirma_senha = input("Confirme a nova senha: ")
                    if nova_senha == confirma_senha:
                        usuario["senha"] = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
                        print("Senha atualizada com sucesso.")
                        return usuario
                    else:
                        print("As senhas não coincidem. Tente novamente.")
                else:
                    print("A senha deve ter no mínimo 8 caracteres e incluir letras e números.")
        else:
            print("Senha atual incorreta. Tente novamente.")

def uptade_username(db, usuario):
    print("Atualização de Username:")
    while True:
        novo_username = input("Digite o novo Username: ")
        if novo_username and novo_username != usuario["username"]:
            if not username_existe(db, novo_username):
                usuario["username"] = novo_username
                print("Username atualizado com sucesso.")
                return usuario
            else:
                print("Username já está em uso. Tente outro.")
        else:
            print("Novo username não pode ser o mesmo que o atual ou vazio.")
    
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
        print("6. Alterar Username")
        print("7. Alterar Senha")
        print("8. Sair")

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
                            card["validade"] = validade  
                        elif opcao_cartao == "3":
                            cvc = input("Novo CVC (3 dígitos): ")
                            card["cvc"] = cvc  
                        elif opcao_cartao == "4":
                            break
                        else:
                            print("Opção inválida. Tente novamente.")
                    
                    print("Cartão atualizado.")
                else:
                    print("Cartão inválido.")
        elif opcao == "6":
            usuario = uptade_username(db, usuario)
        elif opcao == "7":
            usuario = uptade_senha(usuario)
        elif opcao == "8":
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