"""Teste de aceitação: fluxo completo pelo terminal com entradas simuladas."""
import unittest

from sistema_academico.apresentacao.cli import CLI
from sistema_academico.montagem import montar_servicos
from sistema_academico.persistencia.conexao import abrir_conexao, inicializar_schema


def executar_cli(entradas):
    conn = abrir_conexao(":memory:")
    inicializar_schema(conn)
    it = iter(entradas)
    saida = []
    CLI(montar_servicos(conn), entrada=lambda _="": next(it), saida=saida.append).executar()
    conn.close()
    return "\n".join(saida)


class TestFluxoCLI(unittest.TestCase):
    def test_fluxo_completo(self):
        texto = executar_cli([
            "1", "1", "ADS", "Análise de Sistemas", "5",                 # curso
            "2", "ENG01", "Engenharia de Software", "80", "1", "ponderada",  # disciplina
            "0",
            "2", "4", "Carlos Lima", "carlos@x.edu", "Mestre",          # professor
            "1", "Ana Souza", "ana@x.edu", "2026001", "1",              # aluno
            "0",
            "3", "1", "1", "1", "2026.2", "30", "0",                    # turma
            "4", "1", "1", "1",                                         # matricular
            "3", "1", "1", "9", "2", "Prova 1",                         # nota 9 peso 2
            "4", "1", "1", "4",                                         # 4 faltas
            "5", "1",                                                   # boletim
            "0", "0",
        ])
        self.assertIn("Curso cadastrado", texto)
        self.assertIn("Matrícula realizada com sucesso.", texto)
        self.assertIn("Engenharia de Software (2026.2) | notas: 9 | média: 9.00 | freq: 95% | Aprovado", texto)
        self.assertIn("Até logo!", texto)

    def test_erros_sao_mostrados_sem_derrubar_o_programa(self):
        texto = executar_cli([
            "1", "1", "ADS", "Sistemas", "abc",     # duração não numérica
            "0", "9", "0",                          # volta, opção inválida, sai
        ])
        self.assertIn("Erro: Duração (semestres) deve ser um número inteiro.", texto)
        self.assertIn("Opção inválida.", texto)

    def test_regra_de_negocio_aparece_como_erro(self):
        texto = executar_cli(["4", "1", "1", "1", "0", "0"])   # matricular aluno/turma inexistentes
        self.assertIn("Erro: Aluno 1 não encontrado.", texto)


if __name__ == "__main__":
    unittest.main()
