"""CLI da biblioteca: python main.py --help (ou python main.py cadastrar --help)."""
import argparse
from datetime import date
import json

from .dominio.anotacao import Anotacao
from .dominio.livro import Livro
from .dominio.revista import Revista
from .persistencia.armazenamento_json import ArmazenamentoJSON
from .servicos.colecao import (
    Colecao,
    RelatorioAvaliacoes,
    RelatorioAnual,
    RelatorioStatus,
)
from .servicos.configuracoes import Configuracoes


_TRADUCOES_ARGPARSE = {
    "usage: ": "uso: ",
    "positional arguments": "argumentos posicionais",
    "options": "opções",
    "show this help message and exit": "mostra esta mensagem de ajuda e sai",
    "error": "erro",
    "the following arguments are required: %s": "os seguintes argumentos são obrigatórios: %s",
    "invalid %(type)s value: %(value)r": "valor inválido para %(type)s: %(value)r",
    "invalid choice: %(value)r (choose from %(choices)s)": "opção inválida: %(value)r (escolha entre %(choices)s)",
}
argparse._ = lambda mensagem: _TRADUCOES_ARGPARSE.get(mensagem, mensagem)


class _ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._positionals.title = "argumentos posicionais"
        self._optionals.title = "opções"


def _parser():
    """Monta a interface de argumentos e subcomandos da CLI."""
    p = _ArgumentParser(prog="bib", description="Gerencie seu acervo digital")
    p._positionals.title = "argumentos posicionais"
    p._optionals.title = "opções"
    p._optionals._group_actions[0].help = "mostra esta mensagem de ajuda e sai"
    p.add_argument("--arquivo", default="scr/banco_de_dados/biblioteca.json")
    p.add_argument("--config", default="settings.json")
    subs = p.add_subparsers(dest="comando", required=True)
    c = subs.add_parser("cadastrar"); c.add_argument("tipo", choices=["livro", "revista"])
    for n, t in (("titulo", str), ("autor", str), ("ano", int), ("genero", str), ("paginas", int)): c.add_argument("--"+n, required=True, type=t)
    c.add_argument("--editora", default=""); c.add_argument("--isbn", default="")
    c.add_argument("--edicao", type=int, default=1); c.add_argument("--periodicidade", default="Mensal")
    c.add_argument("--status", default="NÃO LIDO", choices=["NÃO LIDO", "LENDO", "LIDO"])
    l = subs.add_parser("listar"); l.add_argument("--busca", default=""); l.add_argument("--autor"); l.add_argument("--genero"); l.add_argument("--status"); l.add_argument("--inicio", help="Data inicial da leitura (AAAA-MM-DD)"); l.add_argument("--fim", help="Data final da leitura (AAAA-MM-DD)")
    u = subs.add_parser("atualizar"); u.add_argument("titulo"); u.add_argument("autor"); u.add_argument("--novo-titulo"); u.add_argument("--novo-autor"); u.add_argument("--genero"); u.add_argument("--paginas", type=int)
    d = subs.add_parser("remover"); d.add_argument("titulo"); d.add_argument("autor")
    s = subs.add_parser("status"); s.add_argument("titulo"); s.add_argument("autor"); s.add_argument("acao", choices=["iniciar", "concluir"])
    s.add_argument("--avaliacao", type=float)
    a = subs.add_parser("anotar"); a.add_argument("titulo"); a.add_argument("autor"); a.add_argument("texto"); a.add_argument("--trecho")
    n = subs.add_parser("anotacoes"); n.add_argument("titulo"); n.add_argument("autor")
    r = subs.add_parser("relatorio"); r.add_argument("tipo", choices=["status", "avaliacoes", "anual"], default="status", nargs="?"); r.add_argument("--ano", type=int)
    cfg = subs.add_parser("configurar"); cfg.add_argument("--genero-favorito"); cfg.add_argument("--limite-leituras-simultaneas", type=int); cfg.add_argument("--meta-anual", type=int)
    return p


def _encontrar(colecao, titulo, autor):
    """Localiza uma publicação pelo título e autor, sem diferenciar caixa."""
    encontrados = [p for p in colecao.listar() if p.titulo.casefold() == titulo.casefold() and p.autor.casefold() == autor.casefold()]
    if not encontrados: raise ValueError("Publicação não encontrada")
    return encontrados[0]


def executar(argv=None):
    """Executa o comando recebido e persiste as alterações no acervo."""
    args = _parser().parse_args(argv)
    repo = ArmazenamentoJSON(args.arquivo)
    config = Configuracoes.carregar(args.config)
    colecao = Colecao(repo.carregar(), config)
    if args.comando == "cadastrar":
        cls = Livro if args.tipo == "livro" else Revista
        extras = {"editora": args.editora, "isbn": args.isbn} if cls is Livro else {"edicao": args.edicao, "periodicidade": args.periodicidade}
        pub = cls(args.titulo, args.autor, args.ano, args.genero, args.paginas, **extras)
        colecao.adicionar(pub)
        if args.status == "LENDO": colecao.iniciar_leitura(pub)
        elif args.status == "LIDO": raise ValueError("Cadastre como NÃO LIDO e use status iniciar/concluir")
        repo.salvar(colecao); print(pub)
    elif args.comando == "listar":
        resultados = colecao.buscar(args.busca, autor=args.autor, genero=args.genero, status=args.status)
        if args.inicio or args.fim:
            if not args.inicio or not args.fim: raise ValueError("Informe --inicio e --fim juntos")
            datas = (date.fromisoformat(args.inicio), date.fromisoformat(args.fim))
            por_periodo = set(colecao.filtrar_por_periodo(*datas))
            resultados = [pub for pub in resultados if pub in por_periodo]
        for pub in resultados: print(f"{pub} | {pub.status} | {pub.paginas} págs.")
    elif args.comando == "atualizar":
        pub = _encontrar(colecao, args.titulo, args.autor)
        titulo = args.novo_titulo or pub.titulo
        autor = args.novo_autor or pub.autor
        if any(p is not pub and p.titulo.casefold() == titulo.casefold() and p.autor.casefold() == autor.casefold() for p in colecao.listar()):
            raise ValueError("Já existe uma publicação com este título e autor")
        if args.novo_titulo: pub.titulo = args.novo_titulo
        if args.novo_autor: pub.autor = args.novo_autor
        if args.genero: pub.genero = args.genero
        if args.paginas is not None: pub.paginas = args.paginas
        repo.salvar(colecao); print("Publicação atualizada")
    elif args.comando == "remover":
        colecao.remover(_encontrar(colecao, args.titulo, args.autor)); repo.salvar(colecao); print("Publicação removida")
    elif args.comando == "status":
        pub = _encontrar(colecao, args.titulo, args.autor)
        if args.acao == "iniciar": colecao.iniciar_leitura(pub)
        else: pub.concluir_leitura()
        if args.avaliacao is not None: pub.avaliar(args.avaliacao)
        repo.salvar(colecao); print(f"Status atualizado: {pub.status}")
    elif args.comando == "anotar":
        pub = _encontrar(colecao, args.titulo, args.autor); pub.adicionar_anotacao(Anotacao(args.texto, trecho=args.trecho)); repo.salvar(colecao); print("Anotação registrada")
    elif args.comando == "anotacoes":
        for item in _encontrar(colecao, args.titulo, args.autor).anotacoes: print(f"{item.data}: {item}")
    elif args.comando == "relatorio":
        if args.tipo == "status": resultado = colecao.relatorio(RelatorioStatus())
        elif args.tipo == "avaliacoes": resultado = colecao.relatorio(RelatorioAvaliacoes()); resultado["top_5"] = [str(p) + f" ({p.avaliacao:g})" for p in resultado["top_5"]]
        else:
            resultado = RelatorioAnual().gerar(colecao.listar(), args.ano)
            meta = config.meta_anual
            resultado["meta"] = meta
            resultado["aviso"] = bool(meta is not None and resultado["leituras_concluidas"] < meta)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    elif args.comando == "configurar":
        config = Configuracoes(args.genero_favorito, args.limite_leituras_simultaneas, args.meta_anual); config.salvar(args.config); print("Configurações salvas")


if __name__ == "__main__":
    try: executar()
    except (ValueError, TypeError) as erro: raise SystemExit(f"Erro: {erro}")
