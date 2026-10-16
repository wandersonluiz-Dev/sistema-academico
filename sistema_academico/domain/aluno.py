from dataclasses import dataclass


@dataclass(frozen=True)
class Aluno:
    id: int | None
    nome: str
    email: str