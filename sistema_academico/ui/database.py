import sqlite3
from pathlib import Path

# O arquivo do banco fica na raiz do projeto, independentemente da pasta atual.
CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "sistema_academico.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                carga_horaria INTEGER NOT NULL CHECK (carga_horaria > 0)
            );

            CREATE TABLE IF NOT EXISTS matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                disciplina_id INTEGER NOT NULL,
                nota1 REAL,
                nota2 REAL,
                UNIQUE (aluno_id, disciplina_id),
                FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE RESTRICT,
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE RESTRICT,
                CHECK (nota1 IS NULL OR (nota1 >= 0 AND nota1 <= 10)),
                CHECK (nota2 IS NULL OR (nota2 >= 0 AND nota2 <= 10))
            );
        """)
