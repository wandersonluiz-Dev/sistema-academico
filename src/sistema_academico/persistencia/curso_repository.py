"""Repositórios de Curso e Disciplina."""
from __future__ import annotations

from ..dominio.curso import Curso, Disciplina
from .base import RepositorioBase


class CursoRepository(RepositorioBase):
    def inserir(self, curso: Curso) -> Curso:
        cursor = self._executar(
            "INSERT INTO cursos (codigo, nome, duracao_semestres) VALUES (?, ?, ?)",
            (curso.codigo, curso.nome, curso.duracao_semestres),
            "Já existe um curso com este código.",
        )
        curso.id = cursor.lastrowid
        return curso

    def buscar_por_id(self, id: int) -> Curso | None:
        linha = self._um("SELECT * FROM cursos WHERE id = ?", (id,))
        return self._mapear(linha) if linha else None

    def listar(self) -> list[Curso]:
        return [self._mapear(l) for l in self._todos("SELECT * FROM cursos ORDER BY nome")]

    @staticmethod
    def _mapear(l) -> Curso:
        return Curso(l["codigo"], l["nome"], l["duracao_semestres"], id=l["id"])


class DisciplinaRepository(RepositorioBase):
    def inserir(self, disciplina: Disciplina) -> Disciplina:
        cursor = self._executar(
            "INSERT INTO disciplinas (codigo, nome, carga_horaria, tipo_media, curso_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (disciplina.codigo, disciplina.nome, disciplina.carga_horaria,
             disciplina.tipo_media, disciplina.curso_id),
            "Já existe uma disciplina com este código.",
        )
        disciplina.id = cursor.lastrowid
        return disciplina

    def buscar_por_id(self, id: int) -> Disciplina | None:
        linha = self._um("SELECT * FROM disciplinas WHERE id = ?", (id,))
        return self._mapear(linha) if linha else None

    def listar(self, curso_id: int | None = None) -> list[Disciplina]:
        if curso_id is None:
            linhas = self._todos("SELECT * FROM disciplinas ORDER BY nome")
        else:
            linhas = self._todos(
                "SELECT * FROM disciplinas WHERE curso_id = ? ORDER BY nome", (curso_id,))
        return [self._mapear(l) for l in linhas]

    @staticmethod
    def _mapear(l) -> Disciplina:
        return Disciplina(l["codigo"], l["nome"], l["carga_horaria"], l["curso_id"],
                          l["tipo_media"], id=l["id"])
