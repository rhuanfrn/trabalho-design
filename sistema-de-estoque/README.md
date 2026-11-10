# Sistema de Gerenciamento de Estoque

## Descrição

O Sistema de Gerenciamento de Estoque é um projeto desenvolvido em Python para auxiliar no controle de produtos de um estoque. O programa permite cadastrar, consultar, atualizar e remover produtos, além de registrar entradas e saídas de mercadorias.

O projeto possui um menu interativo executado pelo terminal e uma API desenvolvida com Flask. Os dados são armazenados em um banco de dados SQLite.

## Integrantes

- Rhuan Carlos Franchi Romão
- Isabela Lorrayne Ferreira Baessa
- Enzo Martins Costa
- Julia Rodrigues dos Santos
- Jhonny Fontes

## Repositório

[GitHub — trabalho-design](https://github.com/rhuanfrn/trabalho-design)

## Funcionalidades

- Cadastro de produtos com nome, preço, quantidade e estoque mínimo.
- Listagem de todos os produtos cadastrados.
- Pesquisa de produto pelo ID.
- Registro de entrada de produtos no estoque.
- Registro de saída, impedindo que a quantidade fique negativa.
- Atualização de nome, preço e estoque mínimo.
- Exclusão de produtos.
- Consulta de produtos com estoque baixo.
- Validações para dados e quantidades informados.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- Programação Orientada a Objetos

## Organização dos arquivos

- `main.py`: menu interativo do sistema executado pelo terminal.
- `app.py`: API Flask e suas rotas.
- `models.py`: classe Produto, regras de negócio e operações do estoque.
- `database.py`: conexão e inicialização do banco de dados SQLite.
- `requirements.txt`: dependências necessárias para executar a API.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/rhuanfrn/trabalho-design.git
```

Entre na pasta do repositório:

```bash
cd trabalho-design
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o menu do sistema

```bash
python main.py
```

O banco de dados `estoque.db` será criado automaticamente na primeira execução.

### 4. Executar a API Flask (opcional)

Em outro terminal, execute:

```bash
python app.py
```

A API ficará disponível em `http://127.0.0.1:5000`.

## Principais rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Mensagem inicial |
| POST | `/produtos` | Cadastrar produto |
| GET | `/produtos` | Listar produtos |
| GET | `/produtos/estoque-baixo` | Listar produtos com estoque baixo |
| GET | `/produtos/<id>` | Buscar produto |
| PUT | `/produtos/<id>` | Atualizar produto |
| DELETE | `/produtos/<id>` | Remover produto |
| POST | `/produtos/<id>/entrada` | Registrar entrada |
| POST | `/produtos/<id>/saida` | Registrar saída |

## Validações

O sistema verifica, entre outras condições, se o nome do produto foi informado, se os valores de preço e estoque são válidos e se a quantidade de saída não ultrapassa o estoque disponível.

## Colaboração

Todos os integrantes devem contribuir com o código ou com a documentação do projeto. As alterações podem ser registradas no Git com `git add` e `git commit` e enviadas ao repositório remoto com `git push`.
