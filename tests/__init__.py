"""Testes do Sistema Acadêmico.

Adiciona `src/` ao caminho de importação para que os testes funcionem tanto com
unittest quanto com pytest, sem instalar o pacote.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
