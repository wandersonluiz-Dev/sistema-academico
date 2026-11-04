"""Repositório de Turma."""
from __future__ import annotations

from ..dominio.turma import Turma
from .base import RepositorioBase


class TurmaRepository(RepositorioBase):
    def inserir(self, turma: Turma) -> Turma:
        cursor = self._executar(
            "INSERT INTO turmas (disciplina_id, professor_id, semestre, vagas) VALUES (?, ?, ?, ?)",
            (turma.disciplina_id, turma.professor_id, turma.semestre, turma.vagas),
        )
        turma.id = cursor.lastrowid
        return turma

    def buscar_por_id(self, id: int) -> Turma | None:
        linha = self._um("SELECT * FROM turmas WHERE id = ?", (id,))
        return self._mapear(linha) if linha else None

    def listar(self) -> list[Turma]:
        return [self._mapear(l) for l in
                self._todos("SELECT * FROM turmas ORDER BY semestre DESC, id")]

    @staticmethod
    def _mapear(l) -> Turma:
        return Turma(l["disciplina_id"], l["professor_id"], l["semestre"], l["vagas"], id=l["id"])
