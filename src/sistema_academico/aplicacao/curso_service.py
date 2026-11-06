"""Casos de uso: cursos e disciplinas (RF01, RF02, RF14)."""
from __future__ import annotations

from ..dominio.curso import Curso, Disciplina
from ..dominio.excecoes import ErroNaoEncontrado
from ..persistencia.curso_repository import CursoRepository, DisciplinaRepository


class CursoService:
    def __init__(self, cursos: CursoRepository, disciplinas: DisciplinaRepository) -> None:
        self._cursos = cursos
        self._disciplinas = disciplinas

    def cadastrar_curso(self, codigo: str, nome: str, duracao_semestres: int) -> Curso:
        return self._cursos.inserir(Curso(codigo, nome, duracao_semestres))

    def cadastrar_disciplina(self, codigo: str, nome: str, carga_horaria: int,
                             curso_id: int, tipo_media: str = "aritmetica") -> Disciplina:
        if self._cursos.buscar_por_id(curso_id) is None:
            raise ErroNaoEncontrado(f"Curso {curso_id} não encontrado.")
        return self._disciplinas.inserir(
            Disciplina(codigo, nome, carga_horaria, curso_id, tipo_media))

    def listar_cursos(self) -> list[Curso]:
        return self._cursos.listar()

    def listar_disciplinas(self, curso_id: int | None = None) -> list[Disciplina]:
        return self._disciplinas.listar(curso_id)
