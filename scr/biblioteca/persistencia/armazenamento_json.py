"""Persistência do acervo em arquivos JSON."""

import json
from datetime import date
from pathlib import Path

from ..dominio.anotacao import Anotacao
from ..dominio.livro import Livro
from ..dominio.revista import Revista


class ArmazenamentoJSON:
    """Carrega e salva publicações, convertendo-as para o formato JSON."""

    def __init__(self, caminho="scr/banco_de_dados/biblioteca.json"):
        self.caminho = Path(caminho)

    def salvar(self, colecao):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        dados = [self._para_dict(p) for p in colecao.listar()]

        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    def carregar(self):
        if not self.caminho.exists():
            return []

        with self.caminho.open(encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

        # Um arquivo vazio equivale a uma biblioteca ainda sem publicações.
        dados = json.loads(conteudo) if conteudo else []
        if not isinstance(dados, list):
            raise ValueError("O arquivo do acervo deve conter uma lista JSON")

        return [self._para_publicacao(item) for item in dados]

    def _para_dict(self, p):
        dados = {
            "tipo": type(p).__name__,
            "titulo": p.titulo,
            "autor": p.autor,
            "ano": p.ano,
            "genero": p.genero,
            "paginas": p.paginas,
            "status": p.status,
            "data_inclusao": p.data_inclusao.isoformat(),
            "data_inicio": p.data_inicio.isoformat() if p.data_inicio else None,
            "data_termino": p.data_termino.isoformat() if p.data_termino else None,
            "anotacoes": [
                {
                    "texto": a.texto,
                    "data": a.data.isoformat(),
                    "trecho": a.trecho,
                }
                for a in p.anotacoes
            ],
            "avaliacao": p.avaliacao,
        }

        if isinstance(p, Livro):
            dados.update(editora=p.editora, isbn=p.isbn)
        elif isinstance(p, Revista):
            dados.update(edicao=p.edicao, periodicidade=p.periodicidade)

        return dados

    def _para_publicacao(self, item):
        if not isinstance(item, dict):
            raise ValueError("Cada publicação do acervo deve ser um objeto JSON")
        for campo in ("tipo", "titulo", "autor", "ano", "genero", "paginas"):
            if campo not in item:
                raise ValueError(
                    f"Campo obrigatório ausente no arquivo do acervo: {campo}"
                )

        anotacoes = [
            Anotacao(
                texto=a["texto"],
                data=date.fromisoformat(a["data"]) if a.get("data") else date.today(),
                trecho=a.get("trecho"),
            )
            for a in item.get("anotacoes", [])
        ]

        comuns = {
            "titulo": item["titulo"],
            "autor": item["autor"],
            "ano": item["ano"],
            "genero": item["genero"],
            "paginas": item["paginas"],
            "status": item.get("status", "NÃO LIDO"),
            "data_inclusao": date.fromisoformat(item["data_inclusao"]) if item.get("data_inclusao") else date.today(),
            "data_inicio": (
                date.fromisoformat(item["data_inicio"])
                if item.get("data_inicio") else None
            ),
            "data_termino": (
                date.fromisoformat(item["data_termino"])
                if item.get("data_termino") else None
            ),
            "anotacoes": anotacoes,
        }

        tipo = item.get("tipo")
        try:
            if tipo == "Livro":
                publicacao = Livro(
                    **comuns, editora=item["editora"], isbn=item["isbn"]
                )
            elif tipo == "Revista":
                publicacao = Revista(
                    **comuns,
                    edicao=item["edicao"],
                    periodicidade=item["periodicidade"],
                )
            else:
                raise ValueError(f"Tipo de publicação desconhecido: {tipo}")
        except KeyError as erro:
            raise ValueError(
                f"Campo obrigatório ausente no arquivo do acervo: {erro.args[0]}"
            ) from None

        avaliacao = item.get("avaliacao")
        if avaliacao is not None and publicacao.status == "LIDO":
            publicacao.avaliar(avaliacao)
        return publicacao
