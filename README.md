# POO-TEMA-3-BIBLIOTECA-PESSOAL-DIGITAL

Projeto de programação que busca criar um sistema de gerenciamento de uma biblioteca pessoal digital. Desenvolver um { sistema de linha de comando (CLI) ou uma API mínima (FastAPI ou Flask, opcional) } para gerenciar uma biblioteca pessoal de livros e revistas digitais, permitindo o cadastro de publicações, o registro de leituras, o controle de status (lido/não lido/em leitura) e a geração de relatórios sobre o acervo. O sistema deve aplicar conceitos de encapsulamento, herança (simples e múltipla), métodos especiais, regras de negócio configuráveis

Projeto deve conter as seguintes funções:

## Cadastro de publicações
CRUD de publicações com: título, autor, ano, tipo (livro ou revista), gênero, número de páginas, status (NÃO LIDO, LENDO, LIDO).
Campo opcional de avaliação (0–10) e data de inclusão.

## Gerenciamento de status de leitura
Alterar status (iniciar leitura, concluir leitura).
Atualizar data de início e término automaticamente.
Impedir marcar como “LIDO” sem data de início.

## Anotações e destaques
Permitir registrar anotações associadas a uma publicação (texto livre).
Cada anotação deve ter data e trecho (opcional).
Listar anotações por publicação.

## Busca e filtros
Buscar publicações por título, autor, gênero ou status.
Filtrar por período de leitura (entre datas).

## Relatórios
Total de publicações cadastradas.
Quantidade e percentual de livros lidos, não lidos e em leitura.
Média das avaliações das publicações lidas.
Top 5 publicações mais bem avaliadas.

## Configurações (settings.json)
Parâmetros opcionais como: gênero favorito, limite de páginas para leituras simultâneas, meta anual de leituras.

