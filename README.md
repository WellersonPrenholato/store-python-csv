# 🐍 Store Python - CRUD 🚀

**Store Python - CRUD** é uma aplicação desenvolvida em Python para gerenciamento de produtos em estoque. O projeto possui duas interfaces:

- **API REST** com FastAPI para integração com outros sistemas
- **Menu CLI** interativo no terminal para uso direto

Os dados são armazenados em arquivo CSV e incluem: **id**, **nome**, **marca**, **codigo**, **preco**, **quantidade**, **corredor** e **prateleira**.

- 📚 [**ROTEIRO**](https://github.com/WellersonPrenholato/store-python-csv/blob/master/Roteiro.pdf)


## 📁 Estrutura do Projeto

```
├── main.py              # API REST (FastAPI)
├── menu.py              # Interface CLI (menu interativo)
├── model.py             # Modelos Pydantic (validação de dados)
├── store_service.py     # Camada de serviço (lógica de negócio + CSV)
├── store.csv            # Banco de dados CSV
├── .env                 # Configuração do ambiente
├── requirements.txt     # Dependências
├── Makefile             # Comandos de execução
└── tests/               # Testes automatizados
    ├── test_model.py
    ├── test_store_service.py
    └── test_api.py
```


## 🎲 Banco de Dados

O banco de dados é implementado como um arquivo CSV (`store.csv`), contendo as colunas:

| Coluna       | Tipo    | Descrição                          |
| :----------- | :------ | :--------------------------------- |
| `id`         | `int`   | Identificador único (auto gerado)  |
| `nome`       | `string`| Nome do produto                    |
| `marca`      | `string`| Marca do produto                   |
| `codigo`     | `int`   | Código do produto (ex.: código de barras) |
| `preco`      | `float` | Preço do produto                   |
| `quantidade` | `int`   | Quantidade em estoque              |
| `corredor`   | `int`   | Corredor no mercado                |
| `prateleira` | `int`   | Prateleira no corredor             |

O nome do arquivo CSV pode ser alterado via variável de ambiente `CSV_FILENAME` no arquivo `.env`.


## 🚀 Instalação e Execução

### Instalar dependências

```bash
make depends
```

### Executar a API REST

```bash
make run
```

Após rodar, a API estará disponível em `http://localhost:8000`. A documentação interativa (Swagger) pode ser acessada em `http://localhost:8000/docs`.

### Executar o Menu CLI

```bash
make menu
```


## 🖥️ Menu Interativo (CLI)

O menu interativo permite operar o sistema diretamente pelo terminal.

### Menu Principal

```
****************************************
      STORE - MENU PRINCIPAL
****************************************
  1 - Cadastrar produto
  2 - Descadastrar produto
  3 - Inserir item
  4 - Remover item
  5 - Listar produtos
  6 - Sair
****************************************
```

#### 1 - Cadastrar produto
Registra um novo produto no banco de dados. O usuário informa: **nome**, **marca**, **código**, **preço**, **quantidade**, **corredor** e **prateleira**. O **id** é gerado automaticamente. Se o código já existir, a operação é rejeitada.

#### 2 - Descadastrar produto
Remove um produto do banco de dados pelo seu **código**. Antes de remover, exibe os dados do produto e solicita confirmação.

#### 3 - Inserir item
Adiciona unidades ao estoque de um produto existente. O usuário informa o **código** do produto e a **quantidade** a ser adicionada.

#### 4 - Remover item
Remove unidades do estoque de um produto existente. O usuário informa o **código** e a **quantidade** a ser removida. Se a quantidade solicitada for maior que o estoque disponível, a operação é bloqueada.

#### 5 - Listar produtos
Redireciona para o **sub-menu de listagem**.

#### 6 - Sair
Encerra o programa.

### Sub-menu de Listagem

```
****************************************
       LISTAR PRODUTOS
****************************************
  1 - Por código
  2 - Por nome
  3 - Por marca
  4 - Por preço
  5 - Por quantidade
  6 - Por localização
  7 - Todos os produtos
  8 - Retornar ao menu anterior
****************************************
```

| Opção | Filtro | Entrada do usuário |
| :---- | :----- | :----------------- |
| 1 | Código exato | Código do produto |
| 2 | Nome (busca parcial, case-insensitive) | Texto a buscar |
| 3 | Marca (busca parcial, case-insensitive) | Texto a buscar |
| 4 | Faixa de preço | Preço mínimo e máximo |
| 5 | Faixa de quantidade | Quantidade mínima e máxima |
| 6 | Localização (corredor + prateleira) | Corredor e prateleira |
| 7 | Exibe todos os produtos | Nenhuma |
| 8 | Retorna ao menu principal | — |

A opção **Por localização** apresenta todos os produtos que estejam no **mesmo corredor e prateleira** informados.

Os resultados são exibidos em formato de tabela:

```
****************************************
  TODOS OS PRODUTOS (5 produto(s))
****************************************
ID    Nome            Marca        Código     Preço   Qtd  Cor  Prat
----------------------------------------------------------------------
1     Arroz           Sepe         324        10.99     3    3     9
2     Macarrao        Barilla      789         8.50     7    4     6
3     Azeite          Gallo        1010       20.90     2    1     2
4     Feijao          Preto        222         7.99     3   12     6
5     Tomate          Branca       18          3.99     2   11     8
----------------------------------------------------------------------
```


## 🚧 Documentação da API REST

### Retorna todos os produtos

```http
GET http://localhost:8000/store
```

### Retorna um produto por código

```http
GET http://localhost:8000/store/{codigo}
```

### Cadastra um novo produto

```http
POST http://localhost:8000/store
```

**Body (JSON):**

| Parâmetro    | Tipo     | Regra                    |
| :----------- | :------- | :----------------------- |
| `nome`       | `string` | Obrigatório, 1-100 caracteres |
| `marca`      | `string` | Obrigatório, 1-100 caracteres |
| `codigo`     | `int`    | Obrigatório, > 0        |
| `preco`      | `float`  | Obrigatório, > 0        |
| `quantidade` | `int`    | Obrigatório, >= 0       |
| `corredor`   | `int`    | Obrigatório, > 0        |
| `prateleira` | `int`    | Obrigatório, > 0        |

> O `id` é gerado automaticamente e não deve ser enviado.

### Atualiza um produto

```http
PUT http://localhost:8000/store/{codigo}
```

Body com os mesmos campos do POST.

### Deleta um produto

```http
DELETE http://localhost:8000/store/{codigo}
```

### Códigos de resposta

| Código | Descrição |
| :----- | :-------- |
| `200`  | Operação realizada com sucesso |
| `201`  | Produto criado com sucesso |
| `404`  | Produto não encontrado |
| `409`  | Código de produto já existe |
| `422`  | Dados inválidos (validação) |


## 🧪 Testes

O projeto possui testes automatizados com **pytest** organizados em três camadas:

| Arquivo | Camada | O que testa |
| :------ | :----- | :---------- |
| `tests/test_model.py` | Model | Validações Pydantic (campos vazios, negativos, limites, obrigatórios) |
| `tests/test_store_service.py` | Service | CRUD no CSV (criar, listar, buscar, atualizar, deletar, duplicatas, CSV vazio) |
| `tests/test_api.py` | API | Endpoints HTTP (status codes, validação de input, persistência entre requests) |

### Executar todos os testes

```bash
make test
```

### Executar testes por camada

```bash
make test-model      # Testes do modelo (validação)
make test-service    # Testes do serviço (lógica de negócio)
make test-api        # Testes da API (endpoints HTTP)
```

> Os testes utilizam arquivos CSV temporários e **nunca alteram** o `store.csv` real.


## ⚙️ Configuração (.env)

| Variável       | Padrão      | Descrição                  |
| :------------- | :---------- | :------------------------- |
| `CSV_FILENAME` | `store.csv` | Nome do arquivo CSV        |
| `HOST`         | `0.0.0.0`  | Host do servidor           |
| `PORT`         | `8000`      | Porta do servidor          |
| `DEBUG`        | `false`     | Ativa modo debug e reload  |


## 📦 Dependências

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic v2
- Pandas
- python-dotenv
- pytest (dev)
- httpx (dev)
