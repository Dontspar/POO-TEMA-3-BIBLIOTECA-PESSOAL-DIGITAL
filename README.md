# POO — TEMA 3: BIBLIOTECA PESSOAL DIGITAL

## Sobre o projeto

O **Biblioteca Pessoal Digital** é um sistema desenvolvido para gerenciar uma biblioteca pessoal de livros e revistas digitais.

O projeto será desenvolvido inicialmente como uma **interface de linha de comando (CLI)**, permitindo ao usuário cadastrar publicações, controlar seu progresso de leitura, adicionar anotações, realizar buscas e consultar relatórios sobre seu acervo.

O sistema tem como objetivo aplicar, na prática, conceitos de **Programação Orientada a Objetos (POO)**, incluindo encapsulamento, herança, abstração, composição/associação, métodos especiais, padrões de projeto e persistência de dados.

---

## Objetivos

O sistema deverá permitir:

* Cadastrar livros e revistas;
* Atualizar e remover publicações;
* Controlar o status de leitura;
* Registrar datas de início e término das leituras;
* Adicionar anotações e destaques;
* Pesquisar e filtrar publicações;
* Avaliar publicações concluídas;
* Gerar relatórios sobre o acervo;
* Configurar regras do sistema por meio de um arquivo `settings.json`;
* Persistir os dados para que não sejam perdidos ao encerrar o programa.

---

# Funcionalidades

## 1. Cadastro de publicações

O sistema permitirá realizar o CRUD (*Create, Read, Update, Delete*) das publicações.

Cada publicação possuirá, inicialmente, os seguintes dados:

* **Título**
* **Autor**
* **Ano de publicação**
* **Tipo** — livro ou revista
* **Gênero**
* **Número de páginas**
* **Status de leitura**
* **Avaliação** — opcional, de 0 a 10
* **Data de inclusão**

Os status disponíveis serão:

* `NÃO LIDO`
* `LENDO`
* `LIDO`

O sistema também deverá impedir o cadastro de duas publicações com o mesmo título e autor.

---

## 2. Gerenciamento de leitura

O usuário poderá alterar o status de leitura de uma publicação.

Ao iniciar uma leitura, a data de início será registrada automaticamente.

Ao concluir uma leitura, a data de término será registrada automaticamente.

### Regras

* Uma publicação não pode ser marcada como `LIDO` sem possuir uma data de início.
* Uma publicação só poderá receber uma avaliação depois de ser marcada como `LIDO`.
* A quantidade de publicações simultaneamente em `LENDO` não poderá ultrapassar o limite definido nas configurações.

---

## 3. Anotações e destaques

O usuário poderá criar anotações associadas a uma publicação.

Cada anotação possuirá:

* Texto da anotação;
* Data da anotação;
* Trecho destacado — opcional.

Será possível listar todas as anotações relacionadas a uma determinada publicação.

---

## 4. Busca e filtros

O sistema permitirá pesquisar publicações utilizando diferentes critérios:

* Título;
* Autor;
* Gênero;
* Status de leitura.

Também será possível filtrar publicações de acordo com o período em que suas leituras foram realizadas.

---

## 5. Relatórios

O sistema deverá gerar relatórios sobre o acervo.

Entre eles:

### Relatório do acervo

Exibe o número total de publicações cadastradas.

### Relatório de leitura

Apresenta:

* Quantidade de publicações `LIDO`;
* Quantidade de publicações `LENDO`;
* Quantidade de publicações `NÃO LIDO`;
* Percentual de cada categoria.

### Relatório de avaliações

Apresenta:

* Média das avaliações das publicações lidas;
* As 5 publicações mais bem avaliadas.

### Meta anual

O sistema utilizará a meta anual definida em `settings.json`.

Caso o número de leituras concluídas esteja abaixo da meta, o sistema emitirá um aviso ao usuário.

---

# Modelagem Orientada a Objetos

A estrutura principal do sistema será baseada nas seguintes classes:

<img width="344" height="587" alt="diagrama2 drawio" src="https://github.com/user-attachments/assets/5b7ea127-651c-4bec-b6bc-27f4c1f5b9c8" />

---

## Classes planejadas

### `Publicacao`

Classe abstrata que representa uma publicação genérica.

**Principais atributos:**

* `titulo`
* `autor`
* `ano`
* `genero`
* `paginas`
* `status`
* `avaliacao`
* `data_inclusao`
* `data_inicio`
* `data_termino`

**Principais responsabilidades:**

* Validar seus próprios dados;
* Controlar informações relacionadas à leitura;
* Alterar o status;
* Representar uma publicação de forma textual.

---

### `Livro`

Especialização de `Publicacao` que representa livros.

Poderá possuir características específicas de livros conforme a evolução do projeto.

---

### `Revista`

Especialização de `Publicacao` que representa revistas.

Poderá possuir características específicas de revistas conforme a evolução do projeto.

---

### `Anotacao`

Representa uma anotação associada a uma publicação.

**Atributos planejados:**

* `texto`
* `data`
* `trecho`

Uma publicação poderá possuir várias anotações.

Publicacao 1 ─────────── * Anotacao


---

### `Colecao`

Responsável por agrupar e gerenciar as publicações pertencentes à biblioteca do usuário.

Entre suas responsabilidades estarão:

* Adicionar publicações;
* Remover publicações;
* Buscar publicações;
* Filtrar publicações;
* Verificar duplicidade;
* Gerar informações utilizadas pelos relatórios.

---

# Encapsulamento e validações

O projeto utilizará `@property` para controlar o acesso e a alteração de determinados atributos.

Entre as validações planejadas:

* O título não poderá ser vazio;
* O ano deverá ser maior ou igual a `1500`;
* A avaliação deverá estar entre `0` e `10`;
* Uma avaliação somente poderá ser atribuída a uma publicação `LIDO`;
* Uma publicação não poderá ser concluída sem uma data de início.

Exemplo conceitual:

```python
@property
def titulo(self):
    return self._titulo

@titulo.setter
def titulo(self, valor):
    if not valor.strip():
        raise ValueError("O título não pode ser vazio.")

    self._titulo = valor
```

---

# Herança

A classe `Publicacao` será utilizada como classe base abstrata.    
<p align="center">
  <img width="500" alt="image" src="https://github.com/user-attachments/assets/aca7c990-af41-4671-8a2e-083a5ca203fe" />
</p>
Essa estrutura permite reutilizar atributos e comportamentos comuns entre livros e revistas, mantendo a possibilidade de cada classe possuir comportamentos específicos.

O projeto também deverá explorar **herança múltipla**, conforme exigido pelos requisitos da disciplina.

---

#  Métodos especiais

O sistema deverá utilizar pelo menos quatro métodos especiais de Python.

### `__str__`

Será utilizado para apresentar um resumo legível da publicação ao usuário.

### `__repr__`

Será utilizado para representar detalhadamente um objeto, principalmente durante depuração e desenvolvimento.

### `__lt__`

Permitirá comparar publicações utilizando o ano de publicação, possibilitando sua ordenação.

### `__eq__`

Permitirá verificar se duas publicações representam a mesma obra, considerando principalmente título e autor.

---

# Padrões de projeto

O projeto pretende utilizar padrões de projeto para separar responsabilidades.

Entre eles:

### Repository

Será utilizado para separar a lógica do domínio da persistência dos dados.

```
Domínio   --->    Repository    --->  JSON / SQLite
```

Dessa forma, as classes responsáveis pela biblioteca não precisarão conhecer diretamente os detalhes de armazenamento.

### State

O comportamento relacionado aos estados de leitura (`NÃO LIDO`, `LENDO` e `LIDO`) poderá ser organizado utilizando o padrão **State**, evitando concentrar todas as regras de mudança de estado em uma única estrutura condicional.

### Strategy

O padrão **Strategy** poderá ser utilizado para permitir diferentes estratégias de ordenação, filtragem ou geração de relatórios.

---

# Persistência

A persistência será implementada inicialmente utilizando JSON.

A responsabilidade de salvar e carregar os dados ficará separada das classes de domínio.

A estrutura planejada inclui um módulo:

dados.py

Com funções como:

salvar_publicacoes()
carregar_publicacoes()

A separação permitirá que o sistema possa futuramente trocar JSON por SQLite sem precisar modificar significativamente as classes de domínio.

---

# Configurações

As regras configuráveis serão armazenadas em:

settings.json

Exemplo de configuração planejada:
```
{
    "genero_favorito": "Ficção Científica",
    "limite_leituras_simultaneas": 3,
    "meta_anual": 12
}
```
Essas configurações poderão influenciar o comportamento do sistema.

Por exemplo, caso o limite de leituras simultâneas seja 3, o sistema deverá impedir que uma quarta publicação seja colocada no estado LENDO.

---

# Interface

A interface planejada será uma CLI (Command Line Interface).

Os comandos seguirão uma estrutura semelhante a:

bib cadastrar
bib listar
bib anotar
bib buscar
bib status
bib relatorio

A interface será responsável apenas pela interação com o usuário, enquanto as regras de negócio permanecerão nas classes e serviços do domínio.


---

# 📁 Estrutura planejada do projeto

```
biblioteca-pessoal/
│
├── README.md
├── settings.json
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── publicacao.py
│   ├── livro.py
│   ├── revista.py
│   ├── anotacao.py
│   ├── colecao.py
│   ├── dados.py
│   └── cli.py
│
└── tests/
    ├── test_publicacao.py
    ├── test_leitura.py
    ├── test_anotacao.py
    └── test_relatorios.py
```

A estrutura poderá ser modificada durante o desenvolvimento conforme novas necessidades forem identificadas.

---
# Regras de negócio

O sistema deverá respeitar as seguintes regras:

- Uma publicação não pode ser marcada como LIDO sem data de início.
- Uma avaliação só pode ser atribuída depois que a publicação for marcada como LIDO.
- Não podem existir duas publicações com o mesmo título e autor.
- A quantidade de leituras simultâneas não pode ultrapassar o limite configurado.
- O sistema deverá informar quando a quantidade de leituras concluídas estiver abaixo da meta anual.
- O ano de publicação deve ser maior ou igual a 1500.
- A avaliação deve estar entre 0 e 10.
- O título da publicação não pode ser vazio.

---
# Conceitos de POO aplicados

### O projeto foi planejado para aplicar os seguintes conceitos:

- Abstração;
- Encapsulamento;
- Herança simples;
- Herança múltipla;
- Associação;
- Composição;
- Polimorfismo;
- Propriedades com @property;
- Métodos especiais (dunder methods);
- Classes abstratas;
- Padrões de projeto;
- Separação entre domínio e persistência.

---

# Autoria
Feito por Tadeu Coêlho de Vasconcelos

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (POO).

Tema: Biblioteca Pessoal Digital.
