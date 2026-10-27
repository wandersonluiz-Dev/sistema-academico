"""Avaliação: notas, cálculo de média e situação do aluno.

PADRÃO DE PROJETO: Strategy.
Problema que resolve: disciplinas diferentes calculam a média de formas
diferentes (aritmética, ponderada). Com um `if` dentro de uma função única,
cada nova regra obrigaria a alterar código já testado.
Por que é melhor que a solução simples: cada regra é uma classe própria,
intercambiável e testada isoladamente; o resto do sistema só conhece a
interface `EstrategiaMedia` (polimorfismo + abstração).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

from .excecoes import ErroValidacao


@dataclass(frozen=True)
class Nota:
    valor: float
    peso: float = 1.0
    descricao: str = ""

    def __post_init__(self) -> None:
        if not (0.0 <= self.valor <= 10.0):
            raise ErroValidacao(f"A nota deve estar entre 0 e 10 (recebido: {self.valor}).")
        if self.peso <= 0:
            raise ErroValidacao("O peso da nota deve ser maior que zero.")


class EstrategiaMedia(ABC):
    @abstractmethod
    def calcular(self, notas: Sequence[Nota]) -> float:
        """Retorna a média (0 a 10) arredondada em 2 casas."""

    @staticmethod
    def _exigir_notas(notas: Sequence[Nota]) -> None:
        if not notas:
            raise ErroValidacao("É necessário ao menos uma nota para calcular a média.")


class MediaAritmetica(EstrategiaMedia):
    def calcular(self, notas: Sequence[Nota]) -> float:
        self._exigir_notas(notas)
        return round(sum(n.valor for n in notas) / len(notas), 2)


class MediaPonderada(EstrategiaMedia):
    def calcular(self, notas: Sequence[Nota]) -> float:
        self._exigir_notas(notas)
        soma_pesos = sum(n.peso for n in notas)
        return round(sum(n.valor * n.peso for n in notas) / soma_pesos, 2)


ESTRATEGIAS: dict[str, type[EstrategiaMedia]] = {
    "aritmetica": MediaAritmetica,
    "ponderada": MediaPonderada,
}


def obter_estrategia(nome: str) -> EstrategiaMedia:
    classe = ESTRATEGIAS.get((nome or "").strip().lower())
    if classe is None:
        raise ErroValidacao(
            f"Tipo de média inválido: '{nome}'. Use: {', '.join(ESTRATEGIAS)}."
        )
    return classe()


@dataclass(frozen=True)
class CriterioAprovacao:
    """Regras de aprovação da instituição (altere aqui se a regra mudar)."""
    media_aprovacao: float = 7.0
    media_recuperacao: float = 4.0
    frequencia_minima: float = 0.75


def calcular_situacao(media: float | None, frequencia: float,
                      criterio: CriterioAprovacao = CriterioAprovacao()) -> str:
    if frequencia < criterio.frequencia_minima:
        return "Reprovado por falta"
    if media is None:
        return "Em andamento"
    if media >= criterio.media_aprovacao:
        return "Aprovado"
    if media >= criterio.media_recuperacao:
        return "Recuperação"
    return "Reprovado"
