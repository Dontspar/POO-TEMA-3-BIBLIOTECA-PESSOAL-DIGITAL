"""Modelo abstrato e regras comuns das publicações."""
from abc import ABC, abstractmethod
from datetime import date

from .anotacao import Anotacao


STATUS_NAO_LIDO = "NÃO LIDO"
STATUS_LENDO = "LENDO"
STATUS_LIDO = "LIDO"
STATUS_VALIDOS = {STATUS_NAO_LIDO, STATUS_LENDO, STATUS_LIDO}


def normalizar_status(valor: str) -> str:
    aliases = {"NAO LIDO": STATUS_NAO_LIDO, "NÃO LIDO": STATUS_NAO_LIDO,
               "NÃO LIDA": STATUS_NAO_LIDO, "NAO LIDA": STATUS_NAO_LIDO,
               "LENDO": STATUS_LENDO, "LIDO": STATUS_LIDO, "LIDA": STATUS_LIDO}
    try:
        return aliases[valor.strip().upper()]
    except (AttributeError, KeyError):
        raise ValueError("Status deve ser NÃO LIDO, LENDO ou LIDO") from None


class Publicacao(ABC):
    """Base abstrata com os dados e o ciclo de leitura das publicações."""

    def __init__(self, titulo, autor, ano, genero, paginas, status=STATUS_NAO_LIDO,
                 data_inclusao=None, data_inicio=None, data_termino=None, anotacoes=None):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.paginas = paginas
        self._data_inclusao = data_inclusao or date.today()
        self._data_inicio = data_inicio
        self._data_termino = data_termino
        self._anotacoes = list(anotacoes or [])
        self._status = STATUS_NAO_LIDO
        self.status = status
        if self._status == STATUS_LENDO and self._data_inicio is None:
            self._data_inicio = date.today()
        if self._status == STATUS_LIDO:
            if self._data_inicio is None:
                raise ValueError("Uma publicação LIDA precisa ter data de início")
            self._data_termino = self._data_termino or date.today()

    @property
    def titulo(self): return self._titulo
    @titulo.setter
    def titulo(self, valor):
        if not isinstance(valor, str) or not valor.strip(): raise ValueError("Título não pode ser vazio")
        self._titulo = valor.strip()

    @property
    def autor(self): return self._autor
    @autor.setter
    def autor(self, valor):
        if not isinstance(valor, str) or not valor.strip(): raise ValueError("Autor não pode ser vazio")
        self._autor = valor.strip()

    @property
    def ano(self): return self._ano
    @ano.setter
    def ano(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 1500: raise ValueError("Ano deve ser um inteiro igual ou superior a 1500")
        self._ano = valor

    @property
    def genero(self): return self._genero
    @genero.setter
    def genero(self, valor):
        if not isinstance(valor, str) or not valor.strip(): raise ValueError("Gênero não pode ser vazio")
        self._genero = valor.strip()

    @property
    def paginas(self): return self._paginas
    @paginas.setter
    def paginas(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0: raise ValueError("Número de páginas deve ser positivo")
        self._paginas = valor

    @property
    def status(self): return self._status
    @status.setter
    def status(self, valor):
        novo = normalizar_status(valor)
        if novo == STATUS_LIDO and getattr(self, "_data_inicio", None) is None:
            raise ValueError("Inicie a leitura antes de marcar como LIDO")
        if novo == STATUS_LENDO and getattr(self, "_data_inicio", None) is None:
            self._data_inicio = date.today()
        if novo == STATUS_NAO_LIDO and getattr(self, "_status", None) == STATUS_LENDO:
            self._data_termino = None
        if novo == STATUS_LIDO:
            self._data_termino = getattr(self, "_data_termino", None) or date.today()
        self._status = novo

    @property
    def data_inclusao(self): return self._data_inclusao
    @property
    def data_inicio(self): return self._data_inicio
    @property
    def data_termino(self): return self._data_termino
    @property
    def anotacoes(self): return self.listar_anotacoes()

    def iniciar_leitura(self):
        if self.status == STATUS_LENDO: return
        self._data_inicio = date.today()
        self._data_termino = None
        self._status = STATUS_LENDO

    def concluir_leitura(self):
        if self._data_inicio is None: raise ValueError("Inicie a leitura antes de concluir")
        self._data_termino = date.today()
        self._status = STATUS_LIDO

    def adicionar_anotacao(self, anotacao):
        if not isinstance(anotacao, Anotacao): raise TypeError("Esperada uma Anotacao")
        self._anotacoes.append(anotacao)
    def listar_anotacoes(self): return self._anotacoes.copy()

    @abstractmethod
    def __str__(self): ...
    def __repr__(self):
        return f"{type(self).__name__}(titulo={self.titulo!r}, autor={self.autor!r}, ano={self.ano!r}, status={self.status!r})"
    def __lt__(self, outra):
        if not isinstance(outra, Publicacao): return NotImplemented
        return self.ano < outra.ano
    def __eq__(self, outra):
        if not isinstance(outra, Publicacao): return NotImplemented
        return (self.titulo.casefold(), self.autor.casefold()) == (outra.titulo.casefold(), outra.autor.casefold())
    def __hash__(self): return hash((self.titulo.casefold(), self.autor.casefold()))
