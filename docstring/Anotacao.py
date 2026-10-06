from datetime import date


class Anotacao:
    """Representa uma anotação associada a uma publicação.
    Init: atributos:
    texto, data do datetime, trecho da publicacao
    """

    def __init__(
        self, texto: str, data: date | None = None, trecho: str | None = None
    ): 
        self._texto = texto
        self._data = data or date.today()
        self._trecho = trecho

    @property
    def texto(self):
        return self._texto

    @texto.setter
    def texto(self, valor: str):
        self._texto = valor

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, valor: date):
        self._data = valor

    @property
    def trecho(self) -> str | None:
        return self._trecho

    @trecho.setter
    def trecho(self, valor: str | None):
        self._trecho = valor

    def __str__(self):
        if self._trecho:
            return f"{self._texto} (trecho: {self._trecho})"
        return self._texto

    def __repr__(self):
        return (
            f"Anotacao(texto={self.texto!r}, data={self.data!r}, "
            f"trecho={self.trecho!r})"
        )
