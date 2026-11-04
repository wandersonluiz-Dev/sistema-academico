"""PADRÃO DE PROJETO: Repository.

Problema que resolve: os serviços não devem conhecer SQL nem o módulo sqlite3.
Eles conversam com repositórios que se comportam como "coleções" de entidades
(`inserir`, `buscar_por_id`, `listar`).

Por que é melhor que a solução simples: espalhar SQL pelas regras de negócio
deixaria o sistema preso ao banco. Com o Repository, o SQL fica em um só lugar
por entidade; trocar de banco ou mudar uma tabela não afeta as regras.

Esta classe base concentra o que é comum: executar SQL e traduzir erros do
SQLite para exceções do domínio.
"""
from __future__ import annotations

import sqlite3

from ..dominio.excecoes import ErroDuplicado, ErroNaoEncontrado


class RepositorioBase:
    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conn = conexao

    def _executar(self, sql: str, parametros: tuple = (),
                  msg_duplicado: str = "Registro duplicado.") -> sqlite3.Cursor:
        try:
            cursor = self._conn.execute(sql, parametros)
            self._conn.commit()
            return cursor
        except sqlite3.IntegrityError as exc:
            self._conn.rollback()
            if "FOREIGN KEY" in str(exc):
                raise ErroNaoEncontrado("Registro relacionado não encontrado.") from exc
            raise ErroDuplicado(msg_duplicado) from exc

    def _um(self, sql: str, parametros: tuple = ()) -> sqlite3.Row | None:
        return self._conn.execute(sql, parametros).fetchone()

    def _todos(self, sql: str, parametros: tuple = ()) -> list[sqlite3.Row]:
        return self._conn.execute(sql, parametros).fetchall()
