"""Testes do padrão Strategy (média) e da situação do aluno (RF10)."""
import unittest

from sistema_academico.dominio.avaliacao import (
    CriterioAprovacao, MediaAritmetica, MediaPonderada, Nota,
    calcular_situacao, obter_estrategia,
)
from sistema_academico.dominio.excecoes import ErroValidacao


class TestEstrategiasDeMedia(unittest.TestCase):
    def test_aritmetica(self):
        self.assertEqual(MediaAritmetica().calcular([Nota(6), Nota(8), Nota(10)]), 8.0)

    def test_ponderada(self):
        self.assertEqual(MediaPonderada().calcular([Nota(10, 3), Nota(5, 2)]), 8.0)

    def test_estrategias_intercambiaveis(self):
        notas = [Nota(10, 3), Nota(5, 1)]
        self.assertEqual(MediaAritmetica().calcular(notas), 7.5)
        self.assertEqual(MediaPonderada().calcular(notas), 8.75)

    def test_obter_estrategia_por_nome(self):
        self.assertIsInstance(obter_estrategia("Ponderada"), MediaPonderada)
        with self.assertRaises(ErroValidacao):
            obter_estrategia("inexistente")

    def test_sem_notas(self):
        with self.assertRaises(ErroValidacao):
            MediaAritmetica().calcular([])

    def test_nota_e_peso_invalidos(self):
        for args in ((10.5,), (-1,), (5, 0)):
            with self.assertRaises(ErroValidacao):
                Nota(*args)


class TestSituacao(unittest.TestCase):
    def test_faixas_de_media(self):
        self.assertEqual(calcular_situacao(7.0, 1.0), "Aprovado")
        self.assertEqual(calcular_situacao(6.99, 1.0), "Recuperação")
        self.assertEqual(calcular_situacao(4.0, 1.0), "Recuperação")
        self.assertEqual(calcular_situacao(3.99, 1.0), "Reprovado")

    def test_reprovado_por_falta_mesmo_com_nota_alta(self):
        self.assertEqual(calcular_situacao(10.0, 0.74), "Reprovado por falta")

    def test_frequencia_minima_exata(self):
        self.assertEqual(calcular_situacao(8.0, 0.75), "Aprovado")

    def test_sem_notas_em_andamento(self):
        self.assertEqual(calcular_situacao(None, 1.0), "Em andamento")

    def test_criterio_configuravel(self):
        mais_flexivel = CriterioAprovacao(media_aprovacao=6.0)
        self.assertEqual(calcular_situacao(6.0, 1.0, mais_flexivel), "Aprovado")


if __name__ == "__main__":
    unittest.main()
