"""Ponto de entrada: python main.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from config import settings  # noqa: E402
from sistema_academico.apresentacao.cli import CLI  # noqa: E402
from sistema_academico.montagem import montar_servicos  # noqa: E402
from sistema_academico.persistencia.conexao import abrir_conexao, inicializar_schema  # noqa: E402


def main() -> None:
    conexao = abrir_conexao(settings.CAMINHO_BANCO)
    inicializar_schema(conexao)
    CLI(montar_servicos(conexao)).executar()


if __name__ == "__main__":
    main()
