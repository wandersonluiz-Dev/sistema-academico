"""Testes unitários do domínio (orientação a objetos e validações)."""
import unittest

from sistema_academico.dominio.curso import Curso, Disciplina
from sistema_academico.dominio.excecoes import ErroValidacao
from sistema_academico.dominio.pessoa import Aluno, Pessoa, Professor
from sistema_academico.dominio.turma import Turma


class TestPessoa(unittest.TestCase):
    def test_pessoa_e_abstrata(self):
        with self.assertRaises(TypeError):
            Pessoa("Fulano", "f@x.com")  # type: ignore[abstract]

    def test_polimorfismo_descricao(self):
        pessoas = [Aluno("Ana Souza", "a@x.com", "2026001", 1),
                   Professor("Carlos Lima", "c@x.com", "Doutor")]
        descricoes = [p.descricao() for p in pessoas]   # mesma chamada, respostas diferentes
        self.assertIn("RA 2026001", descricoes[0])
        self.assertIn("Doutor", descricoes[1])

    def test_email_invalido(self):
        with self.assertRaises(ErroValidacao):
            Aluno("Ana Souza", "invalido", "1", 1)

    def test_email_normalizado(self):
        self.assertEqual(Aluno("Ana Souza", " ANA@X.com ", "1", 1).email, "ana@x.com")

    def test_nome_curto(self):
        with self.assertRaises(ErroValidacao):
            Professor("Al", "a@x.com", "Mestre")

    def test_aluno_exige_ra_e_curso(self):
        with self.assertRaises(ErroValidacao):
            Aluno("Ana Souza", "a@x.com", " ", 1)
        with self.assertRaises(ErroValidacao):
            Aluno("Ana Souza", "a@x.com", "1", 0)

    def test_professor_exige_titulacao(self):
        with self.assertRaises(ErroValidacao):
            Professor("Carlos Lima", "c@x.com", "")

    def test_encapsulamento_ra_somente_leitura(self):
        with self.assertRaises(AttributeError):
            Aluno("Ana Souza", "a@x.com", "1", 1).ra = "2"  # type: ignore[misc]


class TestCursoDisciplinaTurma(unittest.TestCase):
    def test_curso_valido_e_codigo_maiusculo(self):
        self.assertEqual(Curso("ads", "Sistemas", 5).codigo, "ADS")

    def test_curso_duracao_invalida(self):
        with self.assertRaises(ErroValidacao):
            Curso("ADS", "Sistemas", 0)

    def test_disciplina_carga_invalida(self):
        with self.assertRaises(ErroValidacao):
            Disciplina("ENG01", "Engenharia", 0, 1)

    def test_disciplina_tipo_media_invalido(self):
        with self.assertRaises(ErroValidacao):
            Disciplina("ENG01", "Engenharia", 80, 1, tipo_media="geometrica")

    def test_turma_semestre_invalido(self):
        for ruim in ("2026", "2026.3", "26.1", ""):
            with self.assertRaises(ErroValidacao):
                Turma(1, 1, ruim, 10)

    def test_turma_vagas(self):
        turma = Turma(1, 1, "2026.2", 2)
        self.assertTrue(turma.tem_vaga(1))
        self.assertFalse(turma.tem_vaga(2))
        with self.assertRaises(ErroValidacao):
            Turma(1, 1, "2026.2", 0)


if __name__ == "__main__":
    unittest.main()
