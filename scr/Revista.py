"""         Classe Revista """
""" Representa uma revista da biblioteca.
Atributos do superinit:
        titulo: str,
        autor: str,
        ano: int,
        genero: str,
        paginas: int,
        status: str = "Não lido",
        data_inclusao: date | None = None,
        data_inicio: date | None = None,
        data_termino: date | None = None,
        anotacoes: list[Anotacao] | None = None

        + os métodos da Classe avaliável:

        Atributos prórprios:
        self._edicao = edicao
        self._periodicidade = periodicidade


        Todos com @property e @setter


    Falta tipificar algumas coisas como os returns e os de avaliável
"""


from datetime import date

from .Anotacao import Anotacao
from .Avaliavel import Avaliavel
from .Publicacao import Publicacao


class Revista(Publicacao, Avaliavel):
    """Representa uma revista da biblioteca."""

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
