import sqlite3
from sistema_academico.domain.aluno import Aluno


class AlunoService:
    """Regras e validações relacionadas aos alunos."""

    def __init__(self, repository):
        self.repository = repository

    def cadastrar(self, nome: str, email: str) -> Aluno:
        nome = nome.strip()
        email = email.strip().lower()
        if len(nome) < 2:
            raise ValueError("O nome deve possuir pelo menos 2 caracteres.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Informe um e-mail válido.")
        try:
            return self.repository.cadastrar(Aluno(None, nome, email))
        except sqlite3.IntegrityError as erro:
            if "alunos.email" in str(erro):
                raise ValueError("Já existe um aluno cadastrado com esse e-mail.") from erro
            raise ValueError("Não foi possível cadastrar o aluno.") from erro

    def listar(self):
        return self.repository.listar()