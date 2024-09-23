from produto import listar_produtos
from usuario import listar_usuarios
from datetime import datetime

def create_compra(db):
    mycol_compra = db.compra
    mycol_produto = db.produto

    usuario = listar_usuarios(db)
    if not usuario:
        return  

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

    quantidade_estoque = int(produto_selecionado["quantidade"])

    while True:
        try:
            quantidade = int(input(f"Quantidade (disponível: {quantidade_estoque}): "))
            if quantidade > quantidade_estoque:
                print(f"Estoque insuficiente. Apenas {quantidade_estoque} unidades disponíveis.")
            elif quantidade <= 0:
                print("Quantidade inválida. Digite um valor maior que zero.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    estado = input("Estado: ")

    data_compra = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    compra = {
        "usuario_id": usuario["_id"], 
        "produto_id": produto_selecionado["_id"], 
        "quantidade": quantidade,
        "estado": estado,
        "data_compra": data_compra
    }

    x = mycol_compra.insert_one(compra)

    nova_quantidade = quantidade_estoque - quantidade
    mycol_produto.update_one(
        {"_id": produto_selecionado["_id"]},
        {"$set": {"quantidade": nova_quantidade}}
    )

    print(f"Compra registrada com sucesso. ID: {x.inserted_id}")
    print(f"Estoque atualizado. Quantidade restante: {nova_quantidade}")


def listar_compras(db):
    mycol_compra = db.compra
    mycol_produto = db.produto

    
    usuario = listar_usuarios(db)
    if not usuario:
        return  

    compras = list(mycol_compra.find({"usuario_id": usuario["_id"]}))
    if not compras:
        print(f"Nenhuma compra registrada para o usuário {usuario['nome']}.")
        return

    print(f"\nLista de compras para o usuário {usuario['nome']}:")
    for compra in compras:
        produto = mycol_produto.find_one({"_id": compra["produto_id"]})
        produto_nome = produto["nome"] if produto else "Desconhecido"
        print(f"ID Compra: {compra['_id']}, Produto: {produto_nome}, Quantidade: {compra['quantidade']}, Estado: {compra['estado']}, Data da Compra: {compra['data_compra']}")
