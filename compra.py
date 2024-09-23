import json
from bson import ObjectId
from produto import listar_produtos

def comprar(db):
    mycol_compra = db.compra
    mycol_produto = db.produto

    # Listar produtos para selecionar
    produtos = listar_produtos(db)
    if not produtos:
        print("Nenhum produto disponível para registrar compra.")
        return

    while True:
        try:
            escolha = int(input("Digite o número do produto que deseja comprar: "))
            if 1 <= escolha <= len(produtos):
                produto_selecionado = produtos[escolha - 1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    # Coletar dados da compra
    quantidade = input("Quantidade: ")
    estado = input("Estado: ")
    data_compra = input("Data da compra: ")

    # Criar documento da compra
    compra = {
        "produto_id": produto_selecionado["_id"],  # Associar o ID do produto
        "quantidade": quantidade,
        "estado": estado,
        "data_compra": data_compra
    }

    # Inserir a compra no banco de dados
    x = mycol_compra.insert_one(compra)
    print(f"Compra registrada com sucesso. ID: {x.inserted_id}")


def listar_compras(db):
    mycol_compra = db.compra
    mycol_produto = db.produto

    compras = list(mycol_compra.find())
    if not compras:
        print("Nenhuma compra registrada.")
        return

    print("\nLista de compras:")
    for compra in compras:
        produto = mycol_produto.find_one({"_id": compra["produto_id"]})
        produto_nome = produto["nome"] if produto else "Desconhecido"
        print(f"ID Compra: {compra['_id']}, Produto: {produto_nome}, Quantidade: {compra['quantidade']}, Estado: {compra['estado']}, Data da Compra: {compra['data_compra']}")
