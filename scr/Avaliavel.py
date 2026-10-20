"""         Classe Avaliável """
""" Classe para pegar avaliação de livros e armazená-la.
Atributos: 
    avaliacao
métodos:
avaliar
        imports de:
        datetime - pegar o tempo atual
        Anotação - Pergar anotações
        Avaliável - Pegar avaliação
        Publicação - Pegar atributos

    Falta tipificar algumas coisas como os returns
"""


class Avaliavel:
    """Mixin que adiciona avaliação às classes que a herdam.                    
    
    
    
    """



    def __init__(self):
        self._avaliacao: float | None = None

    @property
    def avaliacao(self) -> float | None:
        return self._avaliacao

    def avaliar(self, nota: float):
        self._avaliacao = nota

a1 = Avaliavel
