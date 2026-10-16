from dataclasses import dataclass


@dataclass(frozen=True)
class Disciplina:
    id: int | None
    nome: str
    carga_horaria: int