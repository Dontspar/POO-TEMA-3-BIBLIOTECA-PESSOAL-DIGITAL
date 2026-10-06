class Avaliavel:
    """Mixin que adiciona avaliação às classes que a herdam."""



    @property
    def avaliacao(self) -> float | None:
        return self._avaliacao

    def avaliar(self, nota: float):
        self._avaliacao = nota

