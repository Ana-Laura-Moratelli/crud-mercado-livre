import json

quantidade = input("Quantidade: ")
estado = input("Estado: ")
dataCompra = input("Data da compra: ")

usuario = {  #estou montando o obj final
    "quantidade" : quantidade,
    "estado" : estado,
    "dataCompra" : dataCompra,
}
print(json.dumps(usuario)) #estou transformando um obj em json (texto)

