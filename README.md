# 🐍 Store Python - CRUD 🚀

**Store Python - CRUD** é uma aplicação simples desenvolvida em Python que implementa operações CRUD (Create, Read, Update, Delete) para gerenciamento de produtos. Utilizando o framework FastAPI, a aplicação permite criar, consultar, atualizar e deletar registros de produtos armazenados em um arquivo CSV. Os dados incluem informações como id, nome, marca, codigo, preco, quantidade, corredor e prateleira. Configurada com um Makefile para facilitar a instalação de dependências e execução, é uma solução leve e prática para controle básico de estoque.

- 📚 [**ROTEIRO**](https://github.com/WellersonPrenholato/store-python-csv/blob/master/Roteiro.pdf)


## 🎲 Banco de dados 🎲

O banco de dados da aplicação **Store - CRUD Python** é implementado como um arquivo CSV. Esse arquivo armazena os registros dos produtos de forma estruturada, contendo colunas como **id**, **nome**, **marca**, **codigo**, **preco**, **quantidade**, **corredor** e **prateleira**. A escolha do CSV como banco de dados torna a solução simples e portátil, eliminando a necessidade de um sistema de gerenciamento de banco de dados externo, embora seja mais adequada para cenários de baixa complexidade e sem alta concorrência.

O banco de dados neste código é um arquivo chamado **store.csv**, mas você pode alterá-lo livremente conforme sua preferência.


## 🚀 Execução

O código está configurado com um **Makefile**. Para executá-lo, instale as dependências usando o seguinte comando:

```python
  make depends
```

Em seguida, para executar o código, utilize o comando:

```python
  make run
```
 
Após rodar esse comando, você poderá realizar requisições à API.

## 🚧 Documentação da API 🚧

#### 📌 Retorna todos os itens

```http
  GET /localhost:8000/store
```

#### 📌 Retorna um item de acordo com o código
```http
  GET /localhost:8000/store/${codigo}
```

#### 📌 Insere um novo item

```http
  POST /localhost:8000/store
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `id`        | `int` | **Obrigatório**. O identificador único do produto. |
| `nome`      | `string` | **Obrigatório**. O nome do produto. |
| `marca`     | `string` | **Obrigatório**. A marca do produto. |
| `codigo`    | `int` | **Obrigatório**. O código do produto (ex.: código de barras). |
| `preco`     | `float` | **Obrigatório**. O preço do produto. |
| `quantidade`| `int` | **Obrigatório**. A quantidade disponível em estoque. |
| `corredor`  | `int` | **Obrigatório**. O corredor onde o produto está localizado. |
| `prateleira`| `int` | **Obrigatório**. A prateleira onde o produto está armazenado. |

#### 📌 Altera um item

```http
  PUT /localhost:8000/store/${codigo}
```
| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `nome`      | `string` | **Opcional**. O nome do produto. |
| `marca`     | `string` | **Opcional**. A marca do produto. |
| `codigo`    | `int` | **Opcional**. O código do produto (ex.: código de barras). |
| `preco`     | `float` | **Opcional**. O preço do produto. |
| `quantidade`| `int` | **Opcional**. A quantidade disponível em estoque. |
| `corredor`  | `int` | **Opcional**. O corredor onde o produto está localizado. |
| `prateleira`| `int` | **Opcional**. A prateleira onde o produto está armazenado. |

#### 📌 Deleta um item

```http
  DELETE /localhost:8000/store/${codigo}
```
