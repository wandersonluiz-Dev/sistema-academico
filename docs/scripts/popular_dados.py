"""Popula o banco com dados de exemplo para a demonstração.

Uso:  python scripts/popular_dados.py
(Usa o mesmo banco do sistema; rode com um banco novo para evitar duplicidade.)
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ))

from config import settings  # noqa: E402
from sistema_academico.montagem import montar_servicos  # noqa: E402
from sistema_academico.persistencia.conexao import abrir_conexao, inicializar_schema  # noqa: E402


def main() -> None:
    conexao = abrir_conexao(settings.CAMINHO_BANCO)
    inicializar_schema(conexao)
    s = montar_servicos(conexao)

    curso = s.cursos.cadastrar_curso("ADS", "Análise e Desenvolvimento de Sistemas", 5)
    eng = s.cursos.cadastrar_disciplina("ENG01", "Engenharia de Software", 80, curso.id, "ponderada")
    poo = s.cursos.cadastrar_disciplina("POO01", "Programação Orientada a Objetos", 80, curso.id)

    prof = s.pessoas.cadastrar_professor("Christian Azonyetin", "christian@faculdade.edu", "Mestre")
    ana = s.pessoas.cadastrar_aluno("Ana Souza", "ana@aluno.edu", "2026001", curso.id)
    bruno = s.pessoas.cadastrar_aluno("Bruno Lima", "bruno@aluno.edu", "2026002", curso.id)

    turma = s.turmas.criar(eng.id, prof.id, "2026.2", 30)
    s.turmas.criar(poo.id, prof.id, "2026.2", 30)

    for aluno in (ana, bruno):
        s.matriculas.matricular(aluno.id, turma.id)
    s.matriculas.lancar_nota(ana.id, turma.id, 8.0, 1, "Prova 1")
    s.matriculas.lancar_nota(ana.id, turma.id, 9.0, 2, "Projeto")
    s.matriculas.lancar_nota(bruno.id, turma.id, 5.0, 1, "Prova 1")
    s.matriculas.registrar_faltas(bruno.id, turma.id, 4)
    print("Dados de exemplo criados. Execute: python main.py")


if __name__ == "__main__":
    main()
