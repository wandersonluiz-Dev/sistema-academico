import sqlite3
from sistema_academico.domain.disciplina import Disciplina


class DisciplinaService:
    """Regras e validações relacionadas às disciplinas."""

    def __init__(self, repository):
        self.repository = repository

    def cadastrar(self, nome: str, carga_horaria: int) -> Disciplina:
        nome = nome.strip()
        if len(nome) < 2:
            raise ValueError("O nome da disciplina deve possuir pelo menos 2 caracteres.")
        if carga_horaria <= 0:
            raise ValueError("A carga horária deve ser maior que zero.")
        try:
            return self.repository.cadastrar(Disciplina(None, nome, carga_horaria))
        except sqlite3.IntegrityError as erro:
            raise ValueError("Já existe uma disciplina com esse nome.") from erro

    def listar(self):
        return self.repository.listar()