class Publicacao(abstrata):                   #Lembrar de colocar import de abstrata
    # Classe abstrata, representando Publicação, que vai "moldar" Livros e Revistas com os principais atributos

    def iniciar_leitura(self):
        pass

    def concluir_leitura(self):
        pass

    def adicionar_anotacao(self, anotacao):
        pass

    def listar_anotacoes(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __lt__(self, outra):
        pass

    def __eq__(self, outra):
        pass