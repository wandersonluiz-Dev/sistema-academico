"""Pessoas do sistema.

- ABSTRAÇÃO: `Pessoa` é abstrata e define o que todo aluno/professor tem.
- HERANÇA: `Aluno` e `Professor` especializam `Pessoa`.
- POLIMORFISMO: `descricao()` responde de forma diferente em cada subclasse.
- ENCAPSULAMENTO: atributos privados (`_nome`, `_email`) acessados por
  properties que validam o valor.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod

from .excecoes import ErroValidacao

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Pessoa(ABC):
    TIPO = ""

    def __init__(self, nome: str, email: str, id: int | None = None) -> None:
        self._id = id
        self.nome = nome
        self.email = email

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        self._id = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ErroValidacao("O nome deve ter pelo menos 3 caracteres.")
        self._nome = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        valor = (valor or "").strip().lower()
        if not _EMAIL_RE.match(valor):
            raise ErroValidacao(f"E-mail inválido: '{valor}'.")
        self._email = valor

    @property
    def tipo(self) -> str:
        return self.TIPO

    @abstractmethod
    def descricao(self) -> str:
        """Texto de apresentação da pessoa."""


class Aluno(Pessoa):
    TIPO = "aluno"

    def __init__(self, nome: str, email: str, ra: str, curso_id: int,
                 id: int | None = None) -> None:
        super().__init__(nome, email, id)
        ra = (ra or "").strip()
        if not ra:
            raise ErroValidacao("O RA (registro acadêmico) do aluno é obrigatório.")
        if not isinstance(curso_id, int) or curso_id <= 0:
            raise ErroValidacao("O curso do aluno é obrigatório.")
        self._ra = ra
        self._curso_id = curso_id

    @property
    def ra(self) -> str:
        return self._ra

    @property
    def curso_id(self) -> int:
        return self._curso_id

    def descricao(self) -> str:
        return f"Aluno {self.nome} (RA {self.ra})"


class Professor(Pessoa):
    TIPO = "professor"

    def __init__(self, nome: str, email: str, titulacao: str,
                 id: int | None = None) -> None:
        super().__init__(nome, email, id)
        titulacao = (titulacao or "").strip()
        if not titulacao:
            raise ErroValidacao("A titulação do professor é obrigatória.")
        self._titulacao = titulacao

    @property
    def titulacao(self) -> str:
        return self._titulacao

    def descricao(self) -> str:
        return f"Prof. {self.nome} ({self.titulacao})"
