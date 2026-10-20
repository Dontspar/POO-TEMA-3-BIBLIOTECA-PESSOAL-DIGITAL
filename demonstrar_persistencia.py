"""Demonstra salvar e recarregar dados no JSON da biblioteca, sem CLI."""

from datetime import date

from scr.Anotacao import Anotacao
from scr.Colecao import Colecao
from scr.Livro import Livro
from scr.Persistência import ArmazenamentoJSON
from scr.Revista import Revista


def demonstrar():
    repositorio = ArmazenamentoJSON("banco_de_dados/biblioteca.json")
    colecao = Colecao(repositorio.carregar())

    # Não duplica os exemplos quando o script é executado novamente.
    if not any(p.titulo == "Ensaio sobre a Cegueira" for p in colecao.listar()):
        livro = Livro(
            titulo="Ensaio sobre a Cegueira",
            autor="José Saramago",
            ano=1995,
            genero="Romance",
            paginas=312,
            editora="Companhia das Letras",
            isbn="978-85-359-0277-5",
            data_inclusao=date.today(),
            anotacoes=[Anotacao("Trecho de exemplo", date.today(), "A cidade")],
        )
        livro.avaliar(4.5)
        livro.iniciar_leitura()
        colecao.adicionar(livro)

    if not any(p.titulo == "Ciência Hoje" for p in colecao.listar()):
        revista = Revista(
            titulo="Ciência Hoje",
            autor="Vários autores",
            ano=2025,
            genero="Ciência",
            paginas=80,
            edicao=400,
            periodicidade="Mensal",
        )
        revista.avaliar(5.0)
        colecao.adicionar(revista)

    repositorio.salvar(colecao)

    # Simula encerrar e iniciar de novo: os objetos vêm do arquivo gravado.
    recarregada = Colecao(repositorio.carregar())
    publicacoes = recarregada.listar()
    livro_recarregado = next(p for p in publicacoes if p.titulo == "Ensaio sobre a Cegueira")
    revista_recarregada = next(p for p in publicacoes if p.titulo == "Ciência Hoje")

    assert isinstance(livro_recarregado, Livro)
    assert livro_recarregado.avaliacao == 4.5
    assert livro_recarregado.anotacoes[0].texto == "Trecho de exemplo"
    assert livro_recarregado.status == "Lendo"
    assert isinstance(revista_recarregada, Revista)
    assert revista_recarregada.avaliacao == 5.0

    print("Persistência JSON OK")
    print(f"Arquivo atualizado: {repositorio.caminho.resolve()}")
    print(f"Publicações recarregadas: {len(publicacoes)}")
    print(f"Avaliação do livro: {livro_recarregado.avaliacao}")
    print(f"Data de início: {livro_recarregado.data_inicio}")


if __name__ == "__main__":
    demonstrar()
