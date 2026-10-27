"""Configurações do sistema.

O caminho do banco pode ser alterado pela variável de ambiente
SISTEMA_ACADEMICO_DB (útil para testes e para ambientes diferentes).
"""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

CAMINHO_BANCO = os.environ.get(
    "SISTEMA_ACADEMICO_DB", str(RAIZ / "database" / "academico.db")
)
