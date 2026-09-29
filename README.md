# POO — TEMA 3: BIBLIOTECA PESSOAL DIGITAL

## Sobre o projeto
O projeto consiste no desenvolvimento de um sistema de linha de comando (CLI) ou uma API mínima (FastAPI ou Flask, opcional) para gerenciar uma biblioteca pessoal de livros e revistas digitais, permitindo o cadastro de publicações, o registro de leituras, o controle de status (lido/não lido/em leitura) e a geração de relatórios sobre o acervo. O sistema deve aplicar conceitos de encapsulamento, herança (simples e múltipla), métodos especiais, regras de negócio configuráveis. A persistência pode ser feita em JSON ou SQLite, com um repositório desacoplado do domínio.

## Objetivos
- Aplicar conceitos de Programação Orientada a Objetos (POO) na construção do sistema.
- Utilizar encapsulamento, abstração, herança, polimorfismo e métodos especiais.
- Permitir o gerenciamento e acompanhamento das leituras.
- Implementar regras de negócio para garantir a consistência dos dados.
- Disponibilizar relatórios e filtros para facilitar o gerenciamento do acervo.
- Utilizar persistência de dados por meio de JSON ou SQLite, mantendo-a separada da lógica do sistema.

---

#  UML textual

CLASSE ABSTRATA: Publicacao
--------------------------------

Atributos:
- titulo: str
- autor: str
- ano: int
- genero: str
- paginas: int
- status: StatusLeitura
- data_inclusao: date
- data_inicio: date | None
- data_termino: date | None
- anotacoes: list[Anotacao]

Métodos:
+ iniciar_leitura(): void
+ concluir_leitura(): void
+ adicionar_anotacao(anotacao: Anotacao): void
+ listar_anotacoes(): list[Anotacao]
+ __str__(): str
+ __repr__(): str
+ __lt__(outra: Publicacao): bool
+ __eq__(outra: Publicacao): bool
---

CLASSE: Livro
--------------------------------
Herda de: Publicacao, Avaliavel

Atributos:
- editora: str
- isbn: str

---

CLASSE: Revista
--------------------------------
Herda de: Publicacao, Avaliavel

Atributos:
- edicao: int
- periodicidade: str

---

CLASSE: Anotacao
--------------------------------
Atributos:
- texto: str
- data: date
- trecho: str | None

Métodos:
+ __str__(): str
+ __repr__(): str

---
CLASSE: Avaliavel <<mixin>>
--------------------------------

Atributos:
- avaliacao: float | None

Métodos:
+ avaliar(nota: float): void

---

CLASSE: Colecao
--------------------------------
Atributos:
- publicacoes: list[Publicacao]

Métodos:
+ adicionar(publicacao): void
+ remover(publicacao): void
+ buscar(termo): list[Publicacao]
+ filtrar_por_status(status): list[Publicacao]
+ filtrar_por_genero(genero): list[Publicacao]
+ filtrar_por_periodo(inicio, fim): list[Publicacao]
+ listar(): list[Publicacao]

Relacionamentos
---------------------------------
- `Livro` e `Revista` herdam de `Publicacao`.
- `Livro` e `Revista` também herdam de `Avaliavel`, caracterizando herança múltipla.
- Uma `Publicacao` pode possuir zero ou várias `Anotacao`.
- Uma `Colecao` pode agrupar zero ou várias `Publicacao`.

---

Diagrama UML completo:
--------------------------------
<img width="601" height="859" alt="image" src="https://github.com/user-attachments/assets/c9c68aef-6861-4622-b25b-c9da1fc9923d" />






