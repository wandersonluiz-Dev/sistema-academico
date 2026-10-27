"""Exceções de domínio: erros de regra de negócio tratados pela interface."""


class ErroDominio(Exception):
    """Base de todos os erros de regra de negócio."""


class ErroValidacao(ErroDominio):
    """Dado inválido (e-mail mal formado, nota fora do intervalo etc.)."""


class ErroNaoEncontrado(ErroDominio):
    """Registro inexistente."""


class ErroDuplicado(ErroDominio):
    """Violação de unicidade (código, RA ou e-mail já cadastrados)."""


class ErroRegraNegocio(ErroDominio):
    """Regra violada (turma lotada, aluno já matriculado, curso incompatível...)."""
