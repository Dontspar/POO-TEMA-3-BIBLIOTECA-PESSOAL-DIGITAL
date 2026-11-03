"""Mixin de avaliação: só permite avaliar publicações já concluídas."""
import math

from .publicacao import STATUS_LIDO


class Avaliavel:
    def __init__(self): self._avaliacao = None
    @property
    def avaliacao(self): return self._avaliacao
    def avaliar(self, nota):
        if getattr(self, "status", None) != STATUS_LIDO:
            raise ValueError("A avaliação só pode ser registrada após a leitura")
        if isinstance(nota, bool) or not isinstance(nota, (int, float)) or not math.isfinite(nota) or not 0 <= nota <= 10:
            raise ValueError("Avaliação deve estar entre 0 e 10")
        self._avaliacao = float(nota)
