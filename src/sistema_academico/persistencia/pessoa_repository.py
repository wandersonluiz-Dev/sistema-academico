"""Repositórios de Aluno e Professor."""
from __future__ import annotations

from ..dominio.pessoa import Aluno, Professor
from .base import RepositorioBase


class AlunoRepository(RepositorioBase):
    def inserir(self, aluno: Aluno) -> Aluno:
        cursor = self._executar(
            "INSERT INTO alunos (ra, nome, email, curso_id) VALUES (?, ?, ?, ?)",
            (aluno.ra, aluno.nome, aluno.email, aluno.curso_id),
            "Já existe um aluno com este RA ou e-mail.",
        )
        aluno.id = cursor.lastrowid
        return aluno

    def atualizar(self, aluno: Aluno) -> Aluno:
        self._executar(
            "UPDATE alunos SET nome = ?, email = ? WHERE id = ?",
            (aluno.nome, aluno.email, aluno.id),
            "Já existe um aluno com este e-mail.",
        )
        return aluno

    def buscar_por_id(self, id: int) -> Aluno | None:
        linha = self._um("SELECT * FROM alunos WHERE id = ?", (id,))
        return self._mapear(linha) if linha else None

    def listar(self) -> list[Aluno]:
        return [self._mapear(l) for l in self._todos("SELECT * FROM alunos ORDER BY nome")]

    @staticmethod
    def _mapear(l) -> Aluno:
        return Aluno(l["nome"], l["email"], l["ra"], l["curso_id"], id=l["id"])


class ProfessorRepository(RepositorioBase):
    def inserir(self, professor: Professor) -> Professor:
        cursor = self._executar(
            "INSERT INTO professores (nome, email, titulacao) VALUES (?, ?, ?)",
            (professor.nome, professor.email, professor.titulacao),
            "Já existe um professor com este e-mail.",
        )
        professor.id = cursor.lastrowid
        return professor

    def buscar_por_id(self, id: int) -> Professor | None:
        linha = self._um("SELECT * FROM professores WHERE id = ?", (id,))
        return self._mapear(linha) if linha else None

    def listar(self) -> list[Professor]:
        return [self._mapear(l) for l in self._todos("SELECT * FROM professores ORDER BY nome")]

    @staticmethod
    def _mapear(l) -> Professor:
        return Professor(l["nome"], l["email"], l["titulacao"], id=l["id"])
