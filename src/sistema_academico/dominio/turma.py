"""Turma: oferta de uma disciplina por um professor em um semestre."""
from __future__ import annotations

import re

from .excecoes import ErroValidacao

_SEMESTRE_RE = re.compile(r"^\d{4}\.[12]$")


class Turma:
    def __init__(self, disciplina_id: int, professor_id: int, semestre: str,
                 vagas: int, id: int | None = None) -> None:
        self.id = id
        if not isinstance(disciplina_id, int) or disciplina_id <= 0:
            raise ErroValidacao("A disciplina da turma é obrigatória.")
        if not isinstance(professor_id, int) or professor_id <= 0:
            raise ErroValidacao("O professor da turma é obrigatório.")
        semestre = (semestre or "").strip()
        if not _SEMESTRE_RE.match(semestre):
            raise ErroValidacao("Semestre inválido. Use o formato AAAA.S (ex.: 2026.2).")
        if not isinstance(vagas, int) or vagas <= 0:
            raise ErroValidacao("O número de vagas deve ser maior que zero.")
        self.disciplina_id = disciplina_id
        self.professor_id = professor_id
        self.semestre = semestre
        self.vagas = vagas

    def tem_vaga(self, ocupadas: int) -> bool:
        return ocupadas < self.vagas
