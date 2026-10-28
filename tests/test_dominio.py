"""Testes unitários do domínio (orientação a objetos e validações)."""
import unittest

from sistema_academico.dominio.excecoes import ErroValidacao
from sistema_academico.dominio.pessoa import Aluno, Pessoa, Professor


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


if __name__ == "__main__":
    unittest.main()
