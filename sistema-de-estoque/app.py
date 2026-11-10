from flask import Flask, jsonify, request

from database import inicializar_banco
from models import (
    GerenciadorEstoque,
    ProdutoNaoEncontradoError,
    QuantidadeInvalidaError,
    DadosInvalidosError,
)

app = Flask(__name__)

gerenciador = GerenciadorEstoque()

# ==============================================================
# TRATAMENTO DE ERROS
# ==============================================================

@app.errorhandler(ProdutoNaoEncontradoError)
def tratar_produto_nao_encontrado(erro):
    return jsonify({
        "erro": str(erro)
    }), 404


@app.errorhandler(QuantidadeInvalidaError)
def tratar_quantidade_invalida(erro):
    return jsonify({
        "erro": str(erro)
    }), 400


@app.errorhandler(DadosInvalidosError)
def tratar_dados_invalidos(erro):
    return jsonify({
        "erro": str(erro)
    }), 400


# ==============================================================
# ROTA INICIAL
# ==============================================================

@app.route("/", methods=["GET"])
def raiz():
    return jsonify({
        "mensagem": "API de Estoque no ar!",
        "documentacao": "Use as rotas /produtos"
    })


# ==============================================================
# PRODUTOS
# ==============================================================

@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Envie um JSON com os dados do produto."
        }), 400

    if "nome" not in dados:
        return jsonify({
            "erro": "O campo 'nome' e obrigatorio."
        }), 400

    if "preco" not in dados:
        return jsonify({
            "erro": "O campo 'preco' e obrigatorio."
        }), 400

    try:
        produto = gerenciador.cadastrar_produto(
            nome=dados["nome"],
            quantidade=dados.get("quantidade", 0),
            preco=dados["preco"],
            estoque_minimo=dados.get("estoque_minimo", 5),
        )

        return jsonify(produto.to_dict()), 201

    except (TypeError, ValueError):
        return jsonify({
            "erro": "Quantidade, preco e estoque_minimo devem ser numeros validos."
        }), 400


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = gerenciador.listar_produtos()

    return jsonify([
        produto.to_dict()
        for produto in produtos
    ])


@app.route("/produtos/estoque-baixo", methods=["GET"])
def estoque_baixo():
    produtos = gerenciador.produtos_com_estoque_baixo()

    return jsonify([
        produto.to_dict()
        for produto in produtos
    ])


@app.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    produto = gerenciador.buscar_produto(produto_id)

    return jsonify(produto.to_dict())


@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({
            "erro": "Envie um JSON com os dados que deseja atualizar."
        }), 400

    try:
        produto = gerenciador.atualizar_produto(produto_id, **dados)
        return jsonify(produto.to_dict())

    except (TypeError, ValueError):
        return jsonify({
            "erro": "Os dados enviados possuem um formato invalido."
        }), 400


@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def remover_produto(produto_id):
    gerenciador.remover_produto(produto_id)

    return jsonify({
        "mensagem": "Produto removido com sucesso."
    })


# ==============================================================
# ENTRADA DE ESTOQUE
# ==============================================================

@app.route("/produtos/<int:produto_id>/entrada", methods=["POST"])
def registrar_entrada(produto_id):
    dados = request.get_json(silent=True)

    if not dados or "quantidade" not in dados:
        return jsonify({
            "erro": "Informe a quantidade da entrada."
        }), 400

    try:
        produto = gerenciador.registrar_entrada(produto_id, dados["quantidade"])
        return jsonify(produto.to_dict())

    except (TypeError, ValueError):
        return jsonify({
            "erro": "A quantidade deve ser um numero inteiro."
        }), 400


# ==============================================================
# SAIDA DE ESTOQUE
# ==============================================================

@app.route("/produtos/<int:produto_id>/saida", methods=["POST"])
def registrar_saida(produto_id):
    dados = request.get_json(silent=True)

    if not dados or "quantidade" not in dados:
        return jsonify({
            "erro": "Informe a quantidade da saida."
        }), 400

    try:
        produto = gerenciador.registrar_saida(produto_id, dados["quantidade"])
        return jsonify(produto.to_dict())

    except (TypeError, ValueError):
        return jsonify({
            "erro": "A quantidade deve ser um numero inteiro."
        }), 400


# ==============================================================
# INICIALIZACAO
# ==============================================================

if __name__ == "__main__":
    inicializar_banco()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )