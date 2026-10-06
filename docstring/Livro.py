from datetime import date

from .Anotacao import Anotacao
from .Avaliavel import Avaliavel
from .Publicacao import Publicacao


class Livro(Publicacao, Avaliavel):
    """Representa um livro da biblioteca."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        ano: int,
        genero: str,
        paginas: int,
        editora: str,
        isbn: str,
        status: str = "Não lido",
        data_inclusao: date | None = None,
        data_inicio: date | None = None,
        data_termino: date | None = None,
        anotacoes: list[Anotacao] | None = None,
    ):
        super().__init__(
            titulo,
            autor,
            ano,
            genero,
            paginas,
            status,
            data_inclusao,
            data_inicio,
            data_termino,
            anotacoes,
        )
        Avaliavel.__init__(self)
        self._editora = editora
        self._isbn = isbn

    @property
    def editora(self):
        return self._editora

    @editora.setter
    def editora(self, valor: str):
        self._editora = valor

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str):
        self._isbn = valor

    def __str__(self):
        return f"{self.titulo} — {self.autor} ({self.ano})"