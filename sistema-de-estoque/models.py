from dataclasses import dataclass

from database import conectar


@dataclass
class Produto:
    id: int
    nome: str
    quantidade: int
    preco: float
    estoque_minimo: int

    @property
    def estoque_baixo(self) -> bool:
        return self.quantidade <= self.estoque_minimo

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "preco": self.preco,
            "estoque_minimo": self.estoque_minimo,
            "estoque_baixo": self.estoque_baixo,
        }


class ProdutoNaoEncontradoError(Exception):
    """Erro quando o produto informado nao existe."""


class QuantidadeInvalidaError(Exception):
    """Erro relacionado a quantidades invalidas."""


class DadosInvalidosError(Exception):
    """Erro quando os dados do produto sao invalidos."""


class GerenciadorEstoque:
    def _linha_para_produto(self, linha) -> Produto:
        return Produto(
            id=linha["id"],
            nome=linha["nome"],
            quantidade=linha["quantidade"],
            preco=linha["preco"],
            estoque_minimo=linha["estoque_minimo"],
        )

    # ==========================================================
    # PRODUTOS
    # ==========================================================

    def cadastrar_produto(
        self,
        nome: str,
        quantidade: int = 0,
        preco: float = 0.0,
        estoque_minimo: int = 5,
    ) -> Produto:
        if not nome or not nome.strip():
            raise DadosInvalidosError(
                "O nome do produto e obrigatorio."
            )

        if quantidade < 0:
            raise QuantidadeInvalidaError(
                "Quantidade inicial nao pode ser negativa."
            )

        if preco < 0:
            raise DadosInvalidosError(
                "O preco nao pode ser negativo."
            )

        if estoque_minimo < 0:
            raise QuantidadeInvalidaError(
                "O estoque minimo nao pode ser negativo."
            )

        conexao = conectar()

        try:
            cursor = conexao.execute(
                """
                INSERT INTO produtos
                (nome, quantidade, preco, estoque_minimo)
                VALUES (?, ?, ?, ?)
                """,
                (
                    nome.strip(),
                    quantidade,
                    preco,
                    estoque_minimo,
                ),
            )

            conexao.commit()
            produto_id = cursor.lastrowid
        finally:
            conexao.close()

        return self.buscar_produto(produto_id)

    def listar_produtos(self) -> list[Produto]:
        conexao = conectar()

        try:
            linhas = conexao.execute(
                """
                SELECT *
                FROM produtos
                ORDER BY nome
                """
            ).fetchall()

            return [
                self._linha_para_produto(linha)
                for linha in linhas
            ]
        finally:
            conexao.close()

    def buscar_produto(
        self,
        produto_id: int,
    ) -> Produto:
        conexao = conectar()

        try:
            linha = conexao.execute(
                """
                SELECT *
                FROM produtos
                WHERE id = ?
                """,
                (produto_id,),
            ).fetchone()
        finally:
            conexao.close()

        if linha is None:
            raise ProdutoNaoEncontradoError(
                f"Produto {produto_id} nao encontrado."
            )

        return self._linha_para_produto(linha)

    def atualizar_produto(
        self,
        produto_id: int,
        **campos,
    ) -> Produto:
        self.buscar_produto(produto_id)

        colunas_permitidas = {
            "nome",
            "preco",
            "estoque_minimo",
        }

        atualizacoes = {
            chave: valor
            for chave, valor in campos.items()
            if chave in colunas_permitidas
            and valor is not None
        }

        if not atualizacoes:
            return self.buscar_produto(produto_id)

        if "nome" in atualizacoes:
            if not isinstance(
                atualizacoes["nome"],
                str,
            ) or not atualizacoes["nome"].strip():
                raise DadosInvalidosError(
                    "O nome do produto nao pode ser vazio."
                )

            atualizacoes["nome"] = atualizacoes["nome"].strip()

        if "preco" in atualizacoes:
            if atualizacoes["preco"] < 0:
                raise DadosInvalidosError(
                    "O preco nao pode ser negativo."
                )

        if "estoque_minimo" in atualizacoes:
            if atualizacoes["estoque_minimo"] < 0:
                raise QuantidadeInvalidaError(
                    "O estoque minimo nao pode ser negativo."
                )

        set_clause = ", ".join(
            f"{coluna} = ?"
            for coluna in atualizacoes
        )

        valores = list(atualizacoes.values())
        valores.append(produto_id)

        conexao = conectar()

        try:
            conexao.execute(
                f"""
                UPDATE produtos
                SET {set_clause}
                WHERE id = ?
                """,
                valores,
            )
            conexao.commit()
        finally:
            conexao.close()

        return self.buscar_produto(produto_id)

    def remover_produto(
        self,
        produto_id: int,
    ):
        self.buscar_produto(produto_id)

        conexao = conectar()

        try:
            conexao.execute(
                """
                DELETE FROM produtos
                WHERE id = ?
                """,
                (produto_id,),
            )
            conexao.commit()
        finally:
            conexao.close()

    # ==========================================================
    # ESTOQUE
    # ==========================================================

    def registrar_entrada(
        self,
        produto_id: int,
        quantidade: int,
    ) -> Produto:
        if quantidade <= 0:
            raise QuantidadeInvalidaError(
                "Quantidade de entrada precisa ser maior que zero."
            )

        produto = self.buscar_produto(produto_id)
        nova_quantidade = produto.quantidade + quantidade

        conexao = conectar()

        try:
            conexao.execute(
                """
                UPDATE produtos
                SET quantidade = ?
                WHERE id = ?
                """,
                (
                    nova_quantidade,
                    produto_id,
                ),
            )
            conexao.commit()
        finally:
            conexao.close()

        return self.buscar_produto(produto_id)

    def registrar_saida(
        self,
        produto_id: int,
        quantidade: int,
    ) -> Produto:
        if quantidade <= 0:
            raise QuantidadeInvalidaError(
                "Quantidade de saida precisa ser maior que zero."
            )

        produto = self.buscar_produto(produto_id)

        if quantidade > produto.quantidade:
            raise QuantidadeInvalidaError(
                f"Estoque insuficiente: ha apenas {produto.quantidade} unidade(s) de '{produto.nome}'."
            )

        nova_quantidade = produto.quantidade - quantidade

        conexao = conectar()

        try:
            conexao.execute(
                """
                UPDATE produtos
                SET quantidade = ?
                WHERE id = ?
                """,
                (
                    nova_quantidade,
                    produto_id,
                ),
            )
            conexao.commit()
        finally:
            conexao.close()

        return self.buscar_produto(produto_id)

    def produtos_com_estoque_baixo(
        self,
    ) -> list[Produto]:
        return [
            produto
            for produto in self.listar_produtos()
            if produto.estoque_baixo
        ]
