"""Modelo de revista do acervo."""

from datetime import date

from .anotacao import Anotacao
from .avaliavel import Avaliavel
from .publicacao import Publicacao


class Revista(Publicacao, Avaliavel):
    """Publicação periódica, com número de edição e periodicidade."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        ano: int,
        genero: str,
        paginas: int,
        edicao: int,
        periodicidade: str,
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
        self._edicao = edicao
        self._periodicidade = periodicidade

    @property
    def edicao(self):
        return self._edicao

    @edicao.setter
    def edicao(self, valor: int):
        self._edicao = valor

    @property
    def periodicidade(self):
        return self._periodicidade

    @periodicidade.setter
    def periodicidade(self, valor: str):
        self._periodicidade = valor

    def __str__(self):
        return f"{self.titulo} — {self.autor} ({self.ano})"
