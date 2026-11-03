"""Facade funcional de persistência, desacoplada dos comandos CLI."""
from .armazenamento_json import ArmazenamentoJSON


def salvar_publicacoes(publicacoes, caminho="scr/banco_de_dados/biblioteca.json"):
    """Salva uma coleção ou uma lista de publicações no arquivo JSON."""
    from ..servicos.colecao import Colecao
    ArmazenamentoJSON(caminho).salvar(publicacoes if isinstance(publicacoes, Colecao) else Colecao(publicacoes))


def carregar_publicacoes(caminho="scr/banco_de_dados/biblioteca.json"):
    """Retorna as publicações armazenadas no arquivo JSON."""
    return ArmazenamentoJSON(caminho).carregar()
