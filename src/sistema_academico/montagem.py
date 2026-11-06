"""Montagem das dependências (repositórios -> serviços) a partir de uma conexão.

Usado por main.py, pelos testes e pelo script de dados de exemplo, evitando
repetir a ligação das peças em vários lugares.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from .aplicacao.curso_service import CursoService
from .aplicacao.matricula_service import MatriculaService
from .aplicacao.pessoa_service import PessoaService
from .aplicacao.turma_service import TurmaService
from .dominio.avaliacao import CriterioAprovacao
from .persistencia.curso_repository import CursoRepository, DisciplinaRepository
from .persistencia.matricula_repository import MatriculaRepository
from .persistencia.pessoa_repository import AlunoRepository, ProfessorRepository
from .persistencia.turma_repository import TurmaRepository


@dataclass(frozen=True)
class Servicos:
    cursos: CursoService
    pessoas: PessoaService
    turmas: TurmaService
    matriculas: MatriculaService


def montar_servicos(conexao: sqlite3.Connection,
                    criterio: CriterioAprovacao = CriterioAprovacao()) -> Servicos:
    cursos, disciplinas = CursoRepository(conexao), DisciplinaRepository(conexao)
    alunos, professores = AlunoRepository(conexao), ProfessorRepository(conexao)
    turmas, matriculas = TurmaRepository(conexao), MatriculaRepository(conexao)
    return Servicos(
        cursos=CursoService(cursos, disciplinas),
        pessoas=PessoaService(alunos, professores, cursos),
        turmas=TurmaService(turmas, disciplinas, professores, matriculas),
        matriculas=MatriculaService(matriculas, turmas, disciplinas, alunos, criterio),
    )
