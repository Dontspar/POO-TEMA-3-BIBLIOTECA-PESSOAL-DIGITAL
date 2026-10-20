from datetime import date

from .Publicacao import Publicacao


class Colecao:
    """Agrupa publicações e oferece operações de busca e filtragem."""

    def __init__(self, publicacoes: list[Publicacao] | None = None):
        self._publicacoes = list(publicacoes) if publicacoes is not None else []

    @property
    def publicacoes(self):
        return self.listar()

    def adicionar(self, publicacao: Publicacao):
        self._publicacoes.append(publicacao)

    def remover(self, publicacao: Publicacao):
        self._publicacoes.remove(publicacao)

    def listar(self):
        return self._publicacoes.copy()

    def buscar(self, termo: str):
        termo = termo.casefold()
        return [
            publicacao
            for publicacao in self._publicacoes
            if termo in publicacao.titulo.casefold()
            or termo in publicacao.autor.casefold()
        ]

    def filtrar_por_status(self, status: str):
        return [
            publicacao
            for publicacao in self._publicacoes
            if publicacao.status == status
        ]

    def filtrar_por_genero(self, genero: str):
        genero = genero.casefold()
        return [
            publicacao
            for publicacao in self._publicacoes
            if publicacao.genero.casefold() == genero
        ]

    def filtrar_por_periodo(
        self, inicio: date, fim: date
    ):
        return [
            publicacao
            for publicacao in self._publicacoes
            if inicio <= publicacao.data_inclusao <= fim
        ]