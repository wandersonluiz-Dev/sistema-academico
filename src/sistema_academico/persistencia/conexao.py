"""Conexão com o SQLite e criação do esquema."""
from __future__ import annotations

import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
ARQUIVO_SCHEMA = RAIZ / "database" / "schema.sql"


def abrir_conexao(caminho: str = ":memory:") -> sqlite3.Connection:
    if caminho != ":memory:":
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_schema(conexao: sqlite3.Connection) -> None:
    conexao.executescript(ARQUIVO_SCHEMA.read_text(encoding="utf-8"))
    conexao.commit()
