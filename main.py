"""Ponto de entrada da CLI da biblioteca."""

from scr.biblioteca.cli import executar


if __name__ == "__main__":
    try:
        executar()
    except (TypeError, ValueError) as erro:
        # Exibe erros de entrada sem um traceback para quem usa a CLI.
        raise SystemExit(f"Erro: {erro}")
