"""Curso e Disciplina."""
from __future__ import annotations

from .avaliacao import ESTRATEGIAS
from .excecoes import ErroValidacao


def _texto_obrigatorio(valor: str, campo: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        raise ErroValidacao(f"{campo} é obrigatório.")
    return valor


class Curso:
    def __init__(self, codigo: str, nome: str, duracao_semestres: int,
                 id: int | None = None) -> None:
        self.id = id
        self.codigo = _texto_obrigatorio(codigo, "O código do curso").upper()
        self.nome = _texto_obrigatorio(nome, "O nome do curso")
        if not isinstance(duracao_semestres, int) or duracao_semestres <= 0:
            raise ErroValidacao("A duração do curso deve ser um número de semestres maior que zero.")
        self.duracao_semestres = duracao_semestres

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome} ({self.duracao_semestres} semestres)"


class Disciplina:
    def __init__(self, codigo: str, nome: str, carga_horaria: int, curso_id: int,
                 tipo_media: str = "aritmetica", id: int | None = None) -> None:
        self.id = id
        self.codigo = _texto_obrigatorio(codigo, "O código da disciplina").upper()
        self.nome = _texto_obrigatorio(nome, "O nome da disciplina")
        if not isinstance(carga_horaria, int) or carga_horaria <= 0:
            raise ErroValidacao("A carga horária deve ser um número inteiro maior que zero.")
        if not isinstance(curso_id, int) or curso_id <= 0:
            raise ErroValidacao("O curso da disciplina é obrigatório.")
        tipo_media = (tipo_media or "").strip().lower()
        if tipo_media not in ESTRATEGIAS:
            raise ErroValidacao(
                f"Tipo de média inválido: '{tipo_media}'. Use: {', '.join(ESTRATEGIAS)}."
            )
        self.carga_horaria = carga_horaria
        self.curso_id = curso_id
        self.tipo_media = tipo_media

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome} ({self.carga_horaria}h, média {self.tipo_media})"
