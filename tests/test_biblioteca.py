"""Testes das regras de domínio, relatórios e persistência da biblioteca."""

from datetime import date, timedelta

import pytest

from scr.biblioteca.dominio.anotacao import Anotacao
from scr.biblioteca.dominio.livro import Livro
from scr.biblioteca.dominio.revista import Revista
from scr.biblioteca.persistencia.armazenamento_json import ArmazenamentoJSON
from scr.biblioteca.servicos.colecao import (
    Colecao,
    RelatorioAnual,
    RelatorioAvaliacoes,
    RelatorioStatus,
)
from scr.biblioteca.servicos.configuracoes import Configuracoes


def livro(titulo="Duna", autor="Frank Herbert", **kw):
    return Livro(titulo, autor, 1965, "Ficção", 500, "Editora", "ISBN", **kw)


def revista(titulo="Ciência", autor="Equipe", **kw):
    return Revista(titulo, autor, 2020, "Ciência", 80, 12, "Mensal", **kw)


# Validações, status de leitura, avaliações e anotações.
def test_cria_livro_e_revista():
    assert isinstance(livro(), Livro) and isinstance(revista(), Revista)

@pytest.mark.parametrize("campo,valor", [("titulo", " "), ("ano", 1499), ("paginas", 0)])
def test_validadores_de_atributos(campo, valor):
    with pytest.raises(ValueError): setattr(livro(), campo, valor)

def test_status_inicial(): assert livro().status == "NÃO LIDO"
def test_nao_conclui_sem_inicio():
    with pytest.raises(ValueError): livro().concluir_leitura()
def test_nao_marca_lido_sem_inicio():
    with pytest.raises(ValueError): setattr(livro(), "status", "LIDO")
def test_iniciar_define_data():
    p = livro(); p.iniciar_leitura(); assert p.data_inicio == date.today() and p.status == "LENDO"
def test_concluir_define_data():
    p = livro(); p.iniciar_leitura(); p.concluir_leitura(); assert p.status == "LIDO" and p.data_termino == date.today()
def test_avaliacao_precisa_leitura_concluida():
    with pytest.raises(ValueError): livro().avaliar(8)
def test_avaliacao_fora_da_faixa():
    p = livro(); p.iniciar_leitura(); p.concluir_leitura()
    with pytest.raises(ValueError): p.avaliar(11)
def test_avaliacao_valida():
    p = livro(); p.iniciar_leitura(); p.concluir_leitura(); p.avaliar(8); assert p.avaliacao == 8
def test_anotacao_data_e_trecho():
    a = Anotacao("nota", trecho="passagem"); assert a.data == date.today() and a.trecho == "passagem"
def test_anotacao_associada():
    p = livro(); p.adicionar_anotacao(Anotacao("nota")); assert len(p.listar_anotacoes()) == 1
def test_anotacoes_nao_expoem_lista_interna():
    p = livro(); copia = p.anotacoes; copia.append(Anotacao("externa")); assert not p.anotacoes


# Busca, regras da coleção e relatórios.
def test_colecao_rejeita_duplicata_sem_diferenciar_caixa():
    with pytest.raises(ValueError): Colecao([livro(), livro("duna", "frank herbert")])
def test_colecao_busca_genero_autor():
    c = Colecao([livro(), revista()]); assert len(c.buscar("ficção")) == 1 and len(c.buscar(autor="equipe")) == 1
def test_filtro_periodo_usa_data_de_inicio():
    p = livro(); p.iniciar_leitura(); assert Colecao([p]).filtrar_por_periodo(date.today(), date.today()) == [p]
def test_ordenacao_por_ano_e_comparacao():
    a, b = livro(), revista(); assert a < b and livro() == livro()
def test_str_repr():
    p = livro(); assert "Duna" in str(p) and "Livro" in repr(p)
def test_relatorio_status_percentual():
    c = Colecao([livro(), revista()]); r = c.relatorio(RelatorioStatus()); assert r["total"] == 2 and r["status"]["NÃO LIDO"]["percentual"] == 100
def test_relatorio_avaliacoes():
    p = livro(); p.iniciar_leitura(); p.concluir_leitura(); p.avaliar(9)
    r = RelatorioAvaliacoes().gerar([p]); assert r["media_lidas"] == 9 and r["top_5"] == [p]
def test_relatorio_anual():
    p = livro(); p.iniciar_leitura(); p.concluir_leitura()
    assert RelatorioAnual().gerar([p], date.today().year)["leituras_concluidas"] == 1
def test_limite_simultaneo():
    c = Colecao([livro(), revista()], Configuracoes(limite_leituras_simultaneas=1))
    c.iniciar_leitura(c.listar()[0])
    with pytest.raises(ValueError): c.iniciar_leitura(c.listar()[1])


# Persistência JSON e configurações.
def test_persistencia_json(tmp_path):
    p = livro(); p.iniciar_leitura(); p.adicionar_anotacao(Anotacao("nota", trecho="texto"))
    repo = ArmazenamentoJSON(tmp_path / "livros.json"); repo.salvar(Colecao([p])); q = repo.carregar()[0]
    assert q.titulo == p.titulo and q.status == p.status and q.anotacoes[0].trecho == "texto"
def test_settings_roundtrip(tmp_path):
    path = tmp_path / "settings.json"; c = Configuracoes("Ficção", 2, 12); c.salvar(path)
    lida = Configuracoes.carregar(path); assert lida.genero_favorito == "Ficção" and lida.meta_anual == 12
