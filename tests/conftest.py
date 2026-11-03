import sys
from pathlib import Path

# Inclui a raiz do projeto no caminho de importação durante os testes.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
