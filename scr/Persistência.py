import json
from datetime import date
from pathlib import Path

from .Anotacao import Anotacao
from .Livro import Livro
from .Revista import Revista


class ArmazenamentoJSON:
    def __init__(self, caminho="banco_de_dados/biblioteca.json"):
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
        anotacoes = [
            Anotacao(
                texto=a["texto"],
                data=date.fromisoformat(a["data"]),
                trecho=a["trecho"],
            )
            for a in item["anotacoes"]
        ]

        comuns = {
            "titulo": item["titulo"],
            "autor": item["autor"],
            "ano": item["ano"],
            "genero": item["genero"],
            "paginas": item["paginas"],
            "status": item["status"],
            "data_inclusao": date.fromisoformat(item["data_inclusao"]),
            "data_inicio": (
                date.fromisoformat(item["data_inicio"])
                if item["data_inicio"] else None
            ),
            "data_termino": (
                date.fromisoformat(item["data_termino"])
                if item["data_termino"] else None
            ),
            "anotacoes": anotacoes,
        }

        if item["tipo"] == "Livro":
            publicacao = Livro(**comuns, editora=item["editora"], isbn=item["isbn"])
        elif item["tipo"] == "Revista":
            publicacao = Revista(
                **comuns,
                edicao=item["edicao"],
                periodicidade=item["periodicidade"],
            )
        else:
            raise ValueError(f"Tipo de publicação desconhecido: {item['tipo']}")

        avaliacao = item.get("avaliacao")
        if avaliacao is not None:
            publicacao.avaliar(avaliacao)
        return publicacao
