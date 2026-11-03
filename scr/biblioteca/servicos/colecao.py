"""Operações do acervo e estratégias para gerar relatórios."""

from datetime import date

from ..dominio.publicacao import (
    Publicacao,
    STATUS_LIDO,
    STATUS_LENDO,
    STATUS_NAO_LIDO,
    normalizar_status,
)


class RelatorioStatus:
    """Resume a quantidade e a proporção de publicações por status."""

    def gerar(self, publicacoes):
        total = len(publicacoes)
        status = {}
        for valor in (STATUS_LIDO, STATUS_NAO_LIDO, STATUS_LENDO):
            quantidade = sum(publicacao.status == valor for publicacao in publicacoes)
            status[valor] = {
                "quantidade": quantidade,
                "percentual": quantidade / total * 100 if total else 0.0,
            }
        return {"total": total, "status": status}


class RelatorioAvaliacoes:
    """Calcula a média e retorna as cinco publicações mais bem avaliadas."""

    def gerar(self, publicacoes):
        avaliadas = [
            publicacao
            for publicacao in publicacoes
            if publicacao.status == STATUS_LIDO and publicacao.avaliacao is not None
        ]
        media = (
            sum(publicacao.avaliacao for publicacao in avaliadas) / len(avaliadas)
            if avaliadas
            else None
        )
        melhores = sorted(
            avaliadas, key=lambda publicacao: publicacao.avaliacao, reverse=True
        )[:5]
        return {"media_lidas": media, "top_5": melhores}


class RelatorioAnual:
    """Conta publicações concluídas no ano solicitado."""

    def gerar(self, publicacoes, ano=None):
        ano = ano or date.today().year
        concluidas = [
            publicacao
            for publicacao in publicacoes
            if publicacao.status == STATUS_LIDO
            and publicacao.data_termino is not None
            and publicacao.data_termino.year == ano
        ]
        return {"ano": ano, "leituras_concluidas": len(concluidas)}


class Colecao:
    """Gerencia publicações, busca, status de leitura e regras do acervo."""

    def __init__(self, publicacoes=None, configuracoes=None):
        self._publicacoes = list(publicacoes or [])
        self.configuracoes = configuracoes
        for publicacao in self._publicacoes:
            self._validar_publicacao(publicacao)
        self._verificar_duplicidade()
        self._validar_limite_leituras()

    @staticmethod
    def _validar_publicacao(publicacao):
        if not isinstance(publicacao, Publicacao):
            raise TypeError("A coleção aceita apenas Publicacao")

    def _verificar_duplicidade(self, ignorar=None):
        chaves = set()
        for publicacao in self._publicacoes:
            if publicacao is ignorar:
                continue
            chave = (publicacao.titulo.casefold(), publicacao.autor.casefold())
            if chave in chaves:
                raise ValueError("Já existe uma publicação com este título e autor")
            chaves.add(chave)

    def _validar_limite_leituras(self, adicionando=None, substituindo=None):
        limite = getattr(self.configuracoes, "limite_leituras_simultaneas", None)
        if limite is None:
            return

        ativas = sum(
            publicacao.status == STATUS_LENDO
            for publicacao in self._publicacoes
            if publicacao is not substituindo
        )
        if adicionando is True or (
            adicionando is not None and adicionando.status == STATUS_LENDO
        ):
            ativas += 1
        if ativas > limite:
            raise ValueError(f"Limite de {limite} leitura(s) simultânea(s) atingido")

    def _indice_por_identidade(self, publicacao):
        for indice, cadastrada in enumerate(self._publicacoes):
            if cadastrada is publicacao:
                return indice
        raise ValueError("Publicação não pertence à coleção")

    @property
    def publicacoes(self):
        return self.listar()

    def adicionar(self, publicacao):
        self._validar_publicacao(publicacao)
        if any(cadastrada == publicacao for cadastrada in self._publicacoes):
            raise ValueError("Já existe uma publicação com este título e autor")
        self._validar_limite_leituras(adicionando=publicacao)
        self._publicacoes.append(publicacao)

    def remover(self, publicacao):
        indice = self._indice_por_identidade(publicacao)
        del self._publicacoes[indice]

    def iniciar_leitura(self, publicacao):
        self._indice_por_identidade(publicacao)
        if publicacao.status != STATUS_LENDO:
            self._validar_limite_leituras(
                adicionando=True, substituindo=publicacao
            )
        publicacao.iniciar_leitura()

    def atualizar(self, atual, substituta):
        self._validar_publicacao(substituta)
        indice = self._indice_por_identidade(atual)
        if any(
            cadastrada == substituta and cadastrada is not atual
            for cadastrada in self._publicacoes
        ):
            raise ValueError("Já existe uma publicação com este título e autor")
        self._validar_limite_leituras(adicionando=substituta, substituindo=atual)
        self._publicacoes[indice] = substituta

    def listar(self):
        return self._publicacoes.copy()

    def buscar(self, termo="", autor=None, genero=None, status=None):
        termo = termo.casefold()
        alvo_status = normalizar_status(status) if status else None
        return [
            publicacao
            for publicacao in self._publicacoes
            if (
                not termo
                or termo in publicacao.titulo.casefold()
                or termo in publicacao.autor.casefold()
                or termo in publicacao.genero.casefold()
            )
            and (not autor or autor.casefold() in publicacao.autor.casefold())
            and (not genero or genero.casefold() in publicacao.genero.casefold())
            and (not alvo_status or publicacao.status == alvo_status)
        ]

    def filtrar_por_status(self, status):
        return self.buscar(status=status)

    def filtrar_por_genero(self, genero):
        return self.buscar(genero=genero)

    def filtrar_por_periodo(self, inicio, fim):
        if inicio > fim:
            raise ValueError("Data inicial deve ser anterior à data final")
        return [
            publicacao
            for publicacao in self._publicacoes
            if publicacao.data_inicio is not None
            and inicio <= publicacao.data_inicio <= fim
        ]

    def relatorio(self, estrategia=None):
        return (estrategia or RelatorioStatus()).gerar(self._publicacoes)
