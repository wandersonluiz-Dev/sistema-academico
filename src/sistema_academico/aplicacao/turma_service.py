"""Casos de uso: turmas (RF06, RF15)."""
from __future__ import annotations

from dataclasses import dataclass

from ..dominio.excecoes import ErroNaoEncontrado
from ..dominio.turma import Turma
from ..persistencia.curso_repository import DisciplinaRepository
from ..persistencia.matricula_repository import MatriculaRepository
from ..persistencia.pessoa_repository import ProfessorRepository
from ..persistencia.turma_repository import TurmaRepository


@dataclass(frozen=True)
class ResumoTurma:
    id: int
    disciplina: str
    professor: str
    semestre: str
    vagas: int
    ocupadas: int


class TurmaService:
    def __init__(self, turmas: TurmaRepository, disciplinas: DisciplinaRepository,
                 professores: ProfessorRepository, matriculas: MatriculaRepository) -> None:
        self._turmas = turmas
        self._disciplinas = disciplinas
        self._professores = professores
        self._matriculas = matriculas

    def criar(self, disciplina_id: int, professor_id: int, semestre: str, vagas: int) -> Turma:
        if self._disciplinas.buscar_por_id(disciplina_id) is None:
            raise ErroNaoEncontrado(f"Disciplina {disciplina_id} não encontrada.")
        if self._professores.buscar_por_id(professor_id) is None:
            raise ErroNaoEncontrado(f"Professor {professor_id} não encontrado.")
        return self._turmas.inserir(Turma(disciplina_id, professor_id, semestre, vagas))

    def listar(self) -> list[ResumoTurma]:
        resumos = []
        for t in self._turmas.listar():
            disciplina = self._disciplinas.buscar_por_id(t.disciplina_id)
            professor = self._professores.buscar_por_id(t.professor_id)
            resumos.append(ResumoTurma(
                t.id, disciplina.nome, professor.nome, t.semestre, t.vagas,
                self._matriculas.contar_ativas_por_turma(t.id)))
        return resumos
