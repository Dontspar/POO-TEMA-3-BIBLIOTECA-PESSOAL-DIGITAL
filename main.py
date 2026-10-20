from scr.Colecao import Colecao
from scr.Persistência import ArmazenamentoJSON

def carregar_biblioteca(caminho="banco_de_dados/biblioteca.json"):
    repositorio = ArmazenamentoJSON(caminho)
    return repositorio, Colecao(repositorio.carregar())


if __name__ == "__main__":
    repositorio, colecao = carregar_biblioteca()
    print(f"Biblioteca carregada: {len(colecao.listar())} publicação(ões).")
