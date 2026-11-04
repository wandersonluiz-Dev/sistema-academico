"""Matrícula do aluno em uma turma, com suas notas e faltas."""
from __future__ import annotations

from typing import Sequence

from .avaliacao import EstrategiaMedia, Nota
from .excecoes import ErroValidacao


class Matricula:
    def __init__(self, aluno_id: int, turma_id: int, id: int | None = None,
                 notas: Sequence[Nota] | None = None, faltas: int = 0,
                 ativa: bool = True) -> None:
        self.id = id
        self.aluno_id = aluno_id
        self.turma_id = turma_id
        self._notas: list[Nota] = list(notas or [])
        self._faltas = faltas
        self.ativa = ativa

    @property
    def notas(self) -> tuple[Nota, ...]:
        return tuple(self._notas)

    @property
    def faltas(self) -> int:
        return self._faltas

    def lancar_nota(self, valor: float, peso: float = 1.0, descricao: str = "") -> Nota:
        nota = Nota(valor, peso, (descricao or "").strip())  # valida valor e peso
        self._notas.append(nota)
        return nota

    def registrar_faltas(self, quantidade: int, carga_horaria: int) -> None:
        """Soma faltas (em horas-aula). Não pode passar da carga horária."""
        if quantidade <= 0:
            raise ErroValidacao("A quantidade de faltas deve ser maior que zero.")
        if self._faltas + quantidade > carga_horaria:
            raise ErroValidacao(
                f"Faltas excedem a carga horária da disciplina ({carga_horaria}h)."
            )
        self._faltas += quantidade

    def media(self, estrategia: EstrategiaMedia) -> float | None:
        return estrategia.calcular(self._notas) if self._notas else None

    def frequencia(self, carga_horaria: int) -> float:
        """Fração de presença (1.0 = 100%)."""
        return max(0.0, (carga_horaria - self._faltas) / carga_horaria)

    def cancelar(self) -> None:
        self.ativa = False

    def reativar(self) -> None:
        self.ativa = True
