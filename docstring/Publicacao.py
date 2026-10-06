"""         Classe Publicacao """
""" Classe-base para livros e revistas.
Atributos:
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

        Todos com @property
        De título até status com método @taranam.setter

        imports de:
        abc - standartizar a classe abstrata de Publicação 
        datetime - pegar o tempo atual

    Falta tipificar algumas coisas como os returns
"""


from abc import ABC, abstractmethod
from datetime import date, time, dt

from .Anotacao import Anotacao


def data_atual() -> date:
    return date.today(dt.strftime("%Y-%m-%d %H:%M"))




class Publicacao(ABC):

    def __init__(
        self,
        titulo: str,
        autor: str,
        ano: int,
        genero: str,
        paginas: int,
        status: str = "Não lido",
        data_inclusao: date | None = None,
        data_inicio: date | None = None,
        data_termino: date | None = None,
        anotacoes: list[Anotacao] | None = None,
    ): 
        self._titulo = titulo
        self._autor = autor
        self._ano = ano
        self._genero = genero
        self._paginas = paginas
        self._status = status
        self._data_inclusao = data_inclusao or data_atual()
        self._data_inicio = data_inicio
        self._data_termino = data_termino
        self._anotacoes = list(anotacoes) if anotacoes is not None else []

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        self._titulo = valor

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, valor: str):
        self._autor = valor

    @property
    def ano(self):
        return self._ano

    @ano.setter
    def ano(self, valor: int):
        self._ano = valor

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, valor: str):
        self._genero = valor

    @property
    def paginas(self):
        return self._paginas

    @paginas.setter
    def paginas(self, valor: int):
        self._paginas = valor

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor: str):
        self._status = valor

    @property
    def data_inclusao(self):
        return self._data_inclusao

    @property
    def data_inicio(self):
        return self._data_inicio

    @property
    def data_termino(self):
        return self._data_termino

    @property
    def anotacoes(self):
        return self.listar_anotacoes()

    def iniciar_leitura(self):
        if self._status != "Lendo":
            self._status = "Lendo"
            self._data_inicio = data_atual()

    def concluir_leitura(self):
        self._status = "Lido"
        self._data_termino = data_atual()

    def adicionar_anotacao(self, anotacao: Anotacao):
        self._anotacoes.append(anotacao)

    def listar_anotacoes(self):
        return self._anotacoes.copy()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return (
            f"{type(self).__name__}(titulo={self.titulo!r}, "
            f"autor={self.autor!r}, ano={self.ano!r})"
        )

    def __lt__(self, outra: object):
        if not isinstance(outra, Publicacao):
            return NotImplemented
        return (self.titulo.casefold(), self.ano) < (
            outra.titulo.casefold(),
            outra.ano,
        )

    def __eq__(self, outra: object):
        if not isinstance(outra, Publicacao):
            return NotImplemented
        return (
            type(self) is type(outra)
            and self.titulo == outra.titulo
            and self.autor == outra.autor
            and self.ano == outra.ano
        )