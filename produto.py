import json

nomeProduto = input("Nome: ")
descricao = input("Descrição: ")
preco = input("Preço: ")
quantidade = input("Quanidade: ")

usuario = {  #estou montando o obj final
    "nome" : nomeProduto,
    "descricao" : descricao,
    "preco" : preco,
    "quantidade": quantidade,
}
print(json.dumps(usuario)) #estou transformando um obj em json (texto)

