from dataclasses import dataclass


@dataclass(frozen=True)
class Matricula:
    id: int | None
    aluno_id: int
    disciplina_id: int
    nota1: float | None = None
    nota2: float | None = None

    @property
    def media(self) -> float | None:
        """Média simples das duas avaliações; None enquanto faltar uma nota."""
        if self.nota1 is None or self.nota2 is None:
            return None
        return (self.nota1 + self.nota2) / 2

    @property
    def situacao(self) -> str:
        if self.media is None:
            return "Notas pendentes"
        return "Aprovado" if self.media >= 7 else "Reprovado"
