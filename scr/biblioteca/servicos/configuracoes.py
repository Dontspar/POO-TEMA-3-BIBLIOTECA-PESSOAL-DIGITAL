"""Carregamento e validação das regras opcionais do acervo."""

import json
from pathlib import Path


class Configuracoes:
    """Preferências e limites opcionais da biblioteca."""

    def __init__(
        self,
        genero_favorito=None,
        limite_leituras_simultaneas=None,
        meta_anual=None,
    ):
        if genero_favorito is not None and not isinstance(genero_favorito, str):
            raise TypeError("genero_favorito deve ser um texto")
        if limite_leituras_simultaneas is not None and (
            isinstance(limite_leituras_simultaneas, bool)
            or not isinstance(limite_leituras_simultaneas, int)
        ):
            raise TypeError("limite_leituras_simultaneas deve ser um inteiro")
        if limite_leituras_simultaneas is not None and limite_leituras_simultaneas < 1:
            raise ValueError("limite_leituras_simultaneas deve ser positivo")
        if meta_anual is not None and (
            isinstance(meta_anual, bool) or not isinstance(meta_anual, int)
        ):
            raise TypeError("meta_anual deve ser um inteiro")
        if meta_anual is not None and meta_anual < 0:
            raise ValueError("meta_anual não pode ser negativa")

        self.genero_favorito = genero_favorito
        self.limite_leituras_simultaneas = limite_leituras_simultaneas
        self.meta_anual = meta_anual

    @classmethod
    def carregar(cls, caminho="settings.json"):
        path = Path(caminho)
        if not path.exists():
            return cls()
        with path.open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if not isinstance(dados, dict):
            raise ValueError("O arquivo de configurações deve conter um objeto JSON")
        return cls(**dados)

    def salvar(self, caminho="settings.json"):
        path = Path(caminho)
        path.parent.mkdir(parents=True, exist_ok=True)
        dados = {
            "genero_favorito": self.genero_favorito,
            "limite_leituras_simultaneas": self.limite_leituras_simultaneas,
            "meta_anual": self.meta_anual,
        }
        with path.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
