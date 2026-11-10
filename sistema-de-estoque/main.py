from models import (
    GerenciadorEstoque,
    ProdutoNaoEncontradoError,
    QuantidadeInvalidaError,
    DadosInvalidosError,
)
from database import inicializar_banco


gerenciador = GerenciadorEstoque()


def ler_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("Digite um numero inteiro valido.")


def ler_decimal(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            return valor
        except ValueError:
            print("Digite um valor numerico valido.")


def cadastrar():
    print("\n--- CADASTRAR PRODUTO ---")
    nome = input("Nome: ").strip()
    preco = ler_decimal("Preco: R$ ")
    quantidade = ler_inteiro("Quantidade inicial: ")
    estoque_minimo = ler_inteiro("Estoque minimo: ")

    produto = gerenciador.cadastrar_produto(
        nome=nome,
        preco=preco,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo,
    )
    print(f"Produto '{produto.nome}' cadastrado com sucesso. ID: {produto.id}")


def listar():
    print("\n--- PRODUTOS CADASTRADOS ---")
    produtos = gerenciador.listar_produtos()

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        print(
            f"ID: {produto.id} | Nome: {produto.nome} | "
            f"Preco: R$ {produto.preco:.2f} | "
            f"Quantidade: {produto.quantidade} | "
            f"Estoque minimo: {produto.estoque_minimo}"
        )


def pesquisar():
    print("\n--- PESQUISAR PRODUTO ---")
    produto_id = ler_inteiro("Informe o ID do produto: ")
    produto = gerenciador.buscar_produto(produto_id)
    print(
        f"ID: {produto.id}\nNome: {produto.nome}\n"
        f"Preco: R$ {produto.preco:.2f}\n"
        f"Quantidade: {produto.quantidade}\n"
        f"Estoque minimo: {produto.estoque_minimo}"
    )


def registrar_entrada():
    print("\n--- ENTRADA DE ESTOQUE ---")
    produto_id = ler_inteiro("ID do produto: ")
    quantidade = ler_inteiro("Quantidade que deseja adicionar: ")
    produto = gerenciador.registrar_entrada(produto_id, quantidade)
    print(f"Entrada registrada. Estoque atual de {produto.nome}: {produto.quantidade}")


def registrar_saida():
    print("\n--- SAIDA DE ESTOQUE ---")
    produto_id = ler_inteiro("ID do produto: ")
    quantidade = ler_inteiro("Quantidade que deseja retirar: ")
    produto = gerenciador.registrar_saida(produto_id, quantidade)
    print(f"Saida registrada. Estoque atual de {produto.nome}: {produto.quantidade}")


def atualizar():
    print("\n--- ATUALIZAR PRODUTO ---")
    produto_id = ler_inteiro("ID do produto: ")
    nome = input("Novo nome (pressione Enter para manter): ").strip()
    preco_texto = input("Novo preco (pressione Enter para manter): ").strip()
    minimo_texto = input("Novo estoque minimo (pressione Enter para manter): ").strip()

    campos = {}
    if nome:
        campos["nome"] = nome
    if preco_texto:
        try:
            campos["preco"] = float(preco_texto.replace(",", "."))
        except ValueError:
            raise ValueError("O preco informado nao e valido.")
    if minimo_texto:
        try:
            campos["estoque_minimo"] = int(minimo_texto)
        except ValueError:
            raise ValueError("O estoque minimo deve ser um numero inteiro.")

    produto = gerenciador.atualizar_produto(produto_id, **campos)
    print(f"Produto atualizado: {produto.nome}")


def remover():
    print("\n--- REMOVER PRODUTO ---")
    produto_id = ler_inteiro("ID do produto: ")
    confirmacao = input("Confirma a exclusao? (s/n): ").strip().lower()
    if confirmacao == "s":
        gerenciador.remover_produto(produto_id)
        print("Produto removido com sucesso.")
    else:
        print("Exclusao cancelada.")


def listar_estoque_baixo():
    print("\n--- PRODUTOS COM ESTOQUE BAIXO ---")
    produtos = gerenciador.produtos_com_estoque_baixo()
    if not produtos:
        print("Nenhum produto com estoque baixo.")
        return
    for produto in produtos:
        print(
            f"ID: {produto.id} | {produto.nome} | "
            f"Quantidade: {produto.quantidade} | "
            f"Minimo: {produto.estoque_minimo}"
        )


def exibir_menu():
    print("\n========== SISTEMA DE ESTOQUE ==========")
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Pesquisar produto por ID")
    print("4 - Registrar entrada no estoque")
    print("5 - Registrar saida do estoque")
    print("6 - Atualizar produto")
    print("7 - Remover produto")
    print("8 - Consultar produtos com estoque baixo")
    print("0 - Sair")
    print("========================================")


def executar():
    inicializar_banco()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()

        try:
            if opcao == "1":
                cadastrar()
            elif opcao == "2":
                listar()
            elif opcao == "3":
                pesquisar()
            elif opcao == "4":
                registrar_entrada()
            elif opcao == "5":
                registrar_saida()
            elif opcao == "6":
                atualizar()
            elif opcao == "7":
                remover()
            elif opcao == "8":
                listar_estoque_baixo()
            elif opcao == "0":
                print("Sistema encerrado.")
                break
            else:
                print("Opcao invalida. Escolha uma opcao do menu.")
        except (
            ProdutoNaoEncontradoError,
            QuantidadeInvalidaError,
            DadosInvalidosError,
            ValueError,
            TypeError,
        ) as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    executar()
