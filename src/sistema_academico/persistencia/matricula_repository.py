"""Repositório de Matrícula (inclui as notas da matrícula)."""
from __future__ import annotations

from ..dominio.avaliacao import Nota
from ..dominio.matricula import Matricula
from .base import RepositorioBase


class MatriculaRepository(RepositorioBase):
    def inserir(self, matricula: Matricula) -> Matricula:
        cursor = self._executar(
            "INSERT INTO matriculas (aluno_id, turma_id, faltas, ativa) VALUES (?, ?, ?, ?)",
            (matricula.aluno_id, matricula.turma_id, matricula.faltas, int(matricula.ativa)),
            "O aluno já possui matrícula nesta turma.",
        )
        matricula.id = cursor.lastrowid
        return matricula

    def salvar_estado(self, matricula: Matricula) -> Matricula:
        """Persiste faltas e situação (ativa/cancelada)."""
        self._executar(
            "UPDATE matriculas SET faltas = ?, ativa = ? WHERE id = ?",
            (matricula.faltas, int(matricula.ativa), matricula.id),
        )
        return matricula

    def adicionar_nota(self, matricula_id: int, nota: Nota) -> None:
        self._executar(
            "INSERT INTO notas (matricula_id, descricao, valor, peso) VALUES (?, ?, ?, ?)",
            (matricula_id, nota.descricao, nota.valor, nota.peso),
        )

    def buscar_por_id(self, id: int) -> Matricula | None:
        linha = self._um("SELECT * FROM matriculas WHERE id = ?", (id,))
        return self._mapear(linha) if linha else None

    def buscar(self, aluno_id: int, turma_id: int) -> Matricula | None:
        linha = self._um(
            "SELECT * FROM matriculas WHERE aluno_id = ? AND turma_id = ?", (aluno_id, turma_id))
        return self._mapear(linha) if linha else None

    def listar_ativas_por_aluno(self, aluno_id: int) -> list[Matricula]:
        return [self._mapear(l) for l in self._todos(
            "SELECT * FROM matriculas WHERE aluno_id = ? AND ativa = 1 ORDER BY id", (aluno_id,))]

    def listar_ativas_por_turma(self, turma_id: int) -> list[Matricula]:
        return [self._mapear(l) for l in self._todos(
            "SELECT * FROM matriculas WHERE turma_id = ? AND ativa = 1 ORDER BY id", (turma_id,))]

    def contar_ativas_por_turma(self, turma_id: int) -> int:
        return self._um(
            "SELECT COUNT(*) FROM matriculas WHERE turma_id = ? AND ativa = 1", (turma_id,))[0]

    def _mapear(self, l) -> Matricula:
        notas = [Nota(n["valor"], n["peso"], n["descricao"]) for n in self._todos(
            "SELECT * FROM notas WHERE matricula_id = ? ORDER BY id", (l["id"],))]
        return Matricula(l["aluno_id"], l["turma_id"], id=l["id"], notas=notas,
                         faltas=l["faltas"], ativa=bool(l["ativa"]))
