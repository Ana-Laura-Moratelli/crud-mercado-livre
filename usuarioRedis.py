import json

#Endereço 

def sincronizar_endereco_mongo_para_redis(db, r, usuario_logado):
    mycol = db.usuario
    usuario = mycol.find_one({"username": usuario_logado})

    if not usuario:
        print("Usuário não encontrado no MongoDB.")
        return

    enderecos_mongo = usuario.get('enderecos', [])

    r.delete(f"usuario:{usuario_logado}:enderecos")

    for endereco in enderecos_mongo:
        rua = endereco['rua']  
        r.hset(f"usuario:{usuario_logado}:enderecos", rua, json.dumps(endereco))

    print("Sincronização do MongoDB para Redis realizada com sucesso!")

def adicionar_endereco_redis(r, usuario_logado):
    rua = input("Rua: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP (8 dígitos): ")

    endereco = {
        'rua': rua,
        'numero': numero,
        'bairro': bairro,
        'cidade': cidade,
        'estado': estado,
        'cep': cep
    }

    r.hset(f"usuario:{usuario_logado}:enderecos", rua, json.dumps(endereco))
    print("Endereço adicionado ao Redis com sucesso!")

def editar_endereco_redis(r, usuario_logado):
    enderecos = r.hgetall(f"usuario:{usuario_logado}:enderecos")

    if not enderecos:
        print("Nenhum endereço encontrado para edição.")
        return

    print("Endereços disponíveis:")
    for i, (rua, endereco_json) in enumerate(enderecos.items()):
        endereco = json.loads(endereco_json)
        print(f"{i + 1}. Rua: {endereco['rua']}, Número: {endereco['numero']}, Bairro: {endereco['bairro']}, Cidade: {endereco['cidade']}, Estado: {endereco['estado']}, CEP: {endereco['cep']}")

    indice = int(input("Escolha o índice do endereço que deseja alterar: ")) - 1

    if indice < 0 or indice >= len(enderecos):
        print("Índice inválido.")
        return

    rua_selecionada = list(enderecos.keys())[indice]
    endereco_selecionado = json.loads(enderecos[rua_selecionada])

    while True:
        print("\nEscolha o que deseja alterar:")
        print("1. Alterar Rua")
        print("2. Alterar Número")
        print("3. Alterar Bairro")
        print("4. Alterar Cidade")
        print("5. Alterar Estado")
        print("6. Alterar CEP")
        print("7. Sair")
        
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            nova_rua = input("Digite a nova rua: ")
            endereco_selecionado['rua'] = nova_rua
            r.hdel(f"usuario:{usuario_logado}:enderecos", rua_selecionada) 
            rua_selecionada = nova_rua  

        elif escolha == '2':
            novo_numero = input("Digite o novo número: ")
            endereco_selecionado['numero'] = novo_numero

        elif escolha == '3':
            novo_bairro = input("Digite o novo bairro: ")
            endereco_selecionado['bairro'] = novo_bairro

        elif escolha == '4':
            nova_cidade = input("Digite a nova cidade: ")
            endereco_selecionado['cidade'] = nova_cidade

        elif escolha == '5':
            novo_estado = input("Digite o novo estado: ")
            endereco_selecionado['estado'] = novo_estado

        elif escolha == '6':
            novo_cep = input("Digite o novo CEP: ")
            endereco_selecionado['cep'] = novo_cep

        elif escolha == '7':
            break
        
        else:
            print("Escolha inválida.")

    r.hset(f"usuario:{usuario_logado}:enderecos", rua_selecionada, json.dumps(endereco_selecionado))
    print("Endereço atualizado com sucesso!")

def remover_endereco_redis(r, usuario_logado):
    enderecos = r.hgetall(f"usuario:{usuario_logado}:enderecos")

    if not enderecos:
        print("Nenhum endereço encontrado no Redis.")
        return

    print("Endereços disponíveis:")
    for idx, (rua, _) in enumerate(enderecos.items(), 1):
        print(f"{idx} - Rua: {rua.decode('utf-8')}")

    indice = int(input("Digite o número do endereço a ser removido: "))

    if 1 <= indice <= len(enderecos):
        rua_selecionada = list(enderecos.keys())[indice - 1]
        r.hdel(f"usuario:{usuario_logado}:enderecos", rua_selecionada)
        print("Endereço removido do Redis com sucesso!")
    else:
        print("Índice inválido.")

def listar_endereco_redis(r, usuario_logado):
    chave_enderecos = f"usuario:{usuario_logado}:enderecos"

    enderecos = r.hgetall(chave_enderecos)

    if not enderecos:
        print("Nenhum endereço encontrado no Redis.")
        return

    print("Endereços no Redis:")
    for idx, (rua, endereco_json) in enumerate(enderecos.items(), 1):
        endereco_decoded = json.loads(endereco_json)
        print(f"{idx} - Rua: {rua.decode('utf-8')}, Número: {endereco_decoded['numero']}, "
              f"Bairro: {endereco_decoded['bairro']}, Cidade: {endereco_decoded['cidade']}, "
              f"Estado: {endereco_decoded['estado']}, CEP: {endereco_decoded['cep']}")

def sincronizar_endereco_redis_para_mongo(db, r, usuario_logado):
    mycol = db.usuario
    usuario = mycol.find_one({"username": usuario_logado})

    if not usuario:
        print("Usuário não encontrado no MongoDB.")
        return

    enderecos_redis = r.hgetall(f"usuario:{usuario_logado}:enderecos")

    if not enderecos_redis:
        print("Nenhum endereço encontrado no Redis para sincronizar.")
        return

    enderecos_mongo = []

    for _, endereco in enderecos_redis.items():
        enderecos_mongo.append(json.loads(endereco))

    mycol.update_one(
        {"_id": usuario['_id']},
        {"$set": {"enderecos": enderecos_mongo}}
    )

    r.delete(f"usuario:{usuario_logado}:enderecos")

    print("Sincronização com o MongoDB realizada com sucesso!")

#Cartão

def sincronizar_cartao_mongo_para_redis(db, r, usuario_logado):
    mycol = db.usuario
    usuario = mycol.find_one({"username": usuario_logado})

    if not usuario:
        print("Usuário não encontrado no MongoDB.")
        return
    
    cartoes_mongo = usuario.get('cartoes', [])

    if not cartoes_mongo:
        print("Nenhum cartão encontrado no MongoDB.")
        return

    
    r.delete(f"usuario:{usuario_logado}:cartoes")

    
    for cartao in cartoes_mongo:
        numero_cartao = cartao.get('numero_cartao') 
        if numero_cartao:  

            r.hset(f"usuario:{usuario_logado}:cartoes", numero_cartao, json.dumps(cartao))
            print(f"Cartão {numero_cartao} adicionado ao Redis.")
        else:
            print("Cartão sem número válido encontrado. Ignorando...")

    print("Sincronização do MongoDB para Redis realizada com sucesso!")

def adicionar_cartao_redis(r, usuario_logado):
    numero_cartao = input("Número do Cartão: ")
    nome_card = input("Nome do Titular: ")
    validade = input("Validade (MM/AA): ")
    cvc = input("cvc: ")

    cartao = {
        'numero_cartao': numero_cartao,
        'nome_card': nome_card,
        'validade': validade,
        'cvc': cvc
    }

    r.hset(f"usuario:{usuario_logado}:cartoes", numero_cartao, json.dumps(cartao))
    print("Cartão adicionado ao Redis com sucesso!")

def editar_cartao_redis(r, usuario_logado):
    chave_cartoes = f"usuario:{usuario_logado}:cartoes"
    cartoes = r.hgetall(chave_cartoes)

    if not cartoes:
        print("Nenhum cartão encontrado para edição.")
        return

    print("Cartões disponíveis:")
    for i, (numero_cartao, cartao_json) in enumerate(cartoes.items()):
        cartao = json.loads(cartao_json)
        print(f"{i + 1}. Número: {numero_cartao.decode('utf-8')}, "
              f"Titular: {cartao['nome_card']}, "  
              f"Validade: {cartao['validade']}, cvc: {cartao['cvc']}")

    indice = int(input("Escolha o índice do cartão que deseja alterar: ")) - 1

    if indice < 0 or indice >= len(cartoes):
        print("Índice inválido.")
        return

    numero_selecionado = list(cartoes.keys())[indice]
    cartao_selecionado = json.loads(cartoes[numero_selecionado])

    while True:
        print("\nEscolha o que deseja alterar:")
        print("1. Alterar Número do Cartão")
        print("2. Alterar Nome do Titular")
        print("3. Alterar Validade")
        print("4. Alterar cvc")
        print("5. Sair")
        
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            novo_numero = input("Digite o novo número do cartão: ")
            cartao_selecionado['numero_cartao'] = novo_numero
            r.hdel(chave_cartoes, numero_selecionado)
            numero_selecionado = novo_numero  

        elif escolha == '2':
            novo_nome = input("Digite o novo nome do titular: ")
            cartao_selecionado['nome_card'] = novo_nome 

        elif escolha == '3':
            nova_validade = input("Digite a nova validade (MM/AA): ")
            cartao_selecionado['validade'] = nova_validade

        elif escolha == '4':
            novo_cvc = input("Digite o novo cvc: ")
            cartao_selecionado['cvc'] = novo_cvc

        elif escolha == '5':
            break
        
        else:
            print("Escolha inválida.")

    
    r.hset(chave_cartoes, numero_selecionado, json.dumps(cartao_selecionado))
    print("Cartão atualizado com sucesso!")

def remover_cartao_redis(r, usuario_logado):
    chave_cartoes = f"usuario:{usuario_logado}:cartoes"
    cartoes = r.hgetall(chave_cartoes)

    if not cartoes:
        print("Nenhum cartão encontrado no Redis.")
        return

    print("Cartões disponíveis:")
    for idx, (numero, _) in enumerate(cartoes.items(), 1):
        print(f"{idx} - Número: {numero.decode('utf-8')}")

    indice = int(input("Digite o número do cartão a ser removido: "))

    if 1 <= indice <= len(cartoes):
        numero_selecionado = list(cartoes.keys())[indice - 1]
        r.hdel(chave_cartoes, numero_selecionado)
        print("Cartão removido do Redis com sucesso!")
    else:
        print("Índice inválido.")


def listar_cartao_redis(r, usuario_logado):
    chave_cartoes = f"usuario:{usuario_logado}:cartoes"
    cartoes = r.hgetall(chave_cartoes)

    if not cartoes:
        print("Nenhum cartão encontrado no Redis.")
        return

    print("Cartões no Redis:")
    for idx, (numero, cartao_json) in enumerate(cartoes.items(), 1):
        cartao_decoded = json.loads(cartao_json)

        # Acessando o campo corretamente como 'nomeCard'
        nome_card = cartao_decoded.get('nome_card', 'N/A')
        validade = cartao_decoded.get('validade', 'N/A')
        cvc = cartao_decoded.get('cvc', 'N/A')

        print(f"{idx} - Número: {numero.decode('utf-8')}, "
              f"Titular: {nome_card}, Validade: {validade}, cvc: {cvc}")

def sincronizar_cartao_redis_para_mongo(db, r, usuario_logado):
    mycol = db.usuario
    usuario = mycol.find_one({"username": usuario_logado})

    if not usuario:
        print("Usuário não encontrado no MongoDB.")
        return

    cartoes_redis = r.hgetall(f"usuario:{usuario_logado}:cartoes")

    if not cartoes_redis:
        print("Nenhum cartão encontrado no Redis para sincronizar.")
        return

    cartoes_mongo = []

    for _, cartao in cartoes_redis.items():
        cartoes_mongo.append(json.loads(cartao))

    mycol.update_one(
        {"_id": usuario['_id']},
        {"$set": {"cartoes": cartoes_mongo}}
    )

    r.delete(f"usuario:{usuario_logado}:cartoes")

    print("Sincronização de cartões com o MongoDB realizada com sucesso!")
