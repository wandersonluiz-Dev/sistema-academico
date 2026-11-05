"""Casos de uso: alunos e professores (RF03, RF04, RF05, RF15)."""
from __future__ import annotations

from ..dominio.excecoes import ErroNaoEncontrado
from ..dominio.pessoa import Aluno, Professor
from ..persistencia.curso_repository import CursoRepository
from ..persistencia.pessoa_repository import AlunoRepository, ProfessorRepository


class PessoaService:
    def __init__(self, alunos: AlunoRepository, professores: ProfessorRepository,
                 cursos: CursoRepository) -> None:
        self._alunos = alunos
        self._professores = professores
        self._cursos = cursos

    def cadastrar_professor(self, nome: str, email: str, titulacao: str) -> Professor:
        return self._professores.inserir(Professor(nome, email, titulacao))

    def cadastrar_aluno(self, nome: str, email: str, ra: str, curso_id: int) -> Aluno:
        if self._cursos.buscar_por_id(curso_id) is None:
            raise ErroNaoEncontrado(f"Curso {curso_id} não encontrado.")
        return self._alunos.inserir(Aluno(nome, email, ra, curso_id))

    def editar_aluno(self, aluno_id: int, nome: str | None = None,
                     email: str | None = None) -> Aluno:
        aluno = self._alunos.buscar_por_id(aluno_id)
        if aluno is None:
            raise ErroNaoEncontrado(f"Aluno {aluno_id} não encontrado.")
        if nome:
            aluno.nome = nome      # setters validam
        if email:
            aluno.email = email
        return self._alunos.atualizar(aluno)

    def listar_alunos(self) -> list[Aluno]:
        return self._alunos.listar()

    def listar_professores(self) -> list[Professor]:
        return self._professores.listar()
