import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).parent / "estoque.db"

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Permite acessar as colunas pelo nome:
    # linha["nome"], linha["preco"], etc.
    conexao.row_factory = sqlite3.Row

    return conexao

def inicializar_banco():
    conexao = conectar()

    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                preco REAL NOT NULL,
                estoque_minimo INTEGER NOT NULL DEFAULT 5
            )
        """)

        conexao.commit()

    finally:
        conexao.close()