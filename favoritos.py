from produto import listar_produtos
from usuario import listar_usuarios
from bson import ObjectId

def add_favorito(db):
    usuario = listar_usuarios(db)
    if not usuario:
        return  

    mycol_favoritos = db.favoritos
    mycol_usuarios = db.usuario  

    produtos = listar_produtos(db)
    if not produtos:
        print("Nenhum produto disponível para adicionar aos favoritos.")
        return

    while True:
        try:
            escolha = int(input("Digite o número do produto que deseja adicionar aos favoritos: "))
            if 1 <= escolha <= len(produtos):
                produto_selecionado = produtos[escolha - 1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    favorito_existente = mycol_favoritos.find_one({"usuario_id": usuario["_id"], "produto_id": produto_selecionado["_id"]})
    if favorito_existente:
        print("Este produto já está na sua lista de favoritos.")
        return

    favorito = {
        "usuario_id": ObjectId(usuario["_id"]),
        "produto_id": ObjectId(produto_selecionado["_id"]),
        "nome": produto_selecionado["nome"]
    }
    x = mycol_favoritos.insert_one(favorito)

    mycol_usuarios.update_one(
        {"_id": ObjectId(usuario["_id"])},
        {"$addToSet": {
            "favoritos": {
                "produto_id": str(produto_selecionado["_id"]),
                "nome": produto_selecionado["nome"],
                "_id": str(x.inserted_id)  
            }
        }}
    )

    print(f"Produto '{produto_selecionado['nome']}' adicionado aos favoritos com sucesso.")

def read_favorito(db):
    usuario = listar_usuarios(db)
    if not usuario:
        return  

    mycol_favoritos = db.favoritos
    mycol_produto = db.produto

    favoritos = list(mycol_favoritos.find({"usuario_id": usuario["_id"]}))  
    
    if len(favoritos) == 0:  
        print("Nenhum produto na lista de favoritos.")
        return

    print("\nLista de produtos favoritos:")
    for favorito in favoritos:
        produto = mycol_produto.find_one({"_id": favorito["produto_id"]})
        if produto:
            print(f"Produto: {produto['nome']}, Descrição: {produto['descricao']}")
        else:
            print("Produto não encontrado.")


def delete_favorito(db):
    usuario = listar_usuarios(db)
    if not usuario:
        print("Nenhum usuário encontrado.")
        return  

    mycol_favoritos = db.favoritos
    mycol_produto = db.produto
    mycol_usuario = db.usuario  

    favoritos = list(mycol_favoritos.find({"usuario_id": usuario["_id"]}))  

    if len(favoritos) == 0:  
        print("Nenhum produto na lista de favoritos para remover.")
        return

    print("\nLista de produtos favoritos:")
    for i, favorito in enumerate(favoritos, 1):
        produto = mycol_produto.find_one({"_id": favorito["produto_id"]})
        if produto:
            print(f"{i}. Produto: {produto['nome']}, Descrição: {produto['descricao']}")
        else:
            print(f"{i}. Produto não encontrado.")

    while True:
        try:
            escolha = int(input("Digite o número do produto que deseja remover dos favoritos: "))
            if 1 <= escolha <= len(favoritos):
                favorito_selecionado = favoritos[escolha - 1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    resultado = mycol_favoritos.delete_one({"usuario_id": usuario["_id"], "produto_id": favorito_selecionado["produto_id"]})
    
    if resultado.deleted_count > 0:
        print(f"Produto removido dos favoritos com sucesso.")
        
        mycol_usuario.update_one(
            {"_id": usuario["_id"]},
            {"$pull": {"favoritos": {"produto_id": str(favorito_selecionado["produto_id"])}}}
        )
        print("Favorito removido também no documento do usuário.")
    else:
        print(f"Produto não encontrado nos favoritos.")
