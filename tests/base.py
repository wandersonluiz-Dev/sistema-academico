"""Base comum: banco SQLite em memória + serviços montados + dados mínimos."""
import unittest

from sistema_academico.montagem import montar_servicos
from sistema_academico.persistencia.conexao import abrir_conexao, inicializar_schema


class BaseComServicos(unittest.TestCase):
    def setUp(self):
        self.conn = abrir_conexao(":memory:")
        inicializar_schema(self.conn)
        self.s = montar_servicos(self.conn)
        self.curso = self.s.cursos.cadastrar_curso("ADS", "Análise de Sistemas", 5)
        self.disciplina = self.s.cursos.cadastrar_disciplina(
            "ENG01", "Engenharia de Software", 80, self.curso.id, "ponderada")
        self.professor = self.s.pessoas.cadastrar_professor(
            "Prof. Carlos", "carlos@x.edu", "Mestre")
        self.aluno = self.s.pessoas.cadastrar_aluno(
            "Ana Souza", "ana@x.edu", "2026001", self.curso.id)
        self.turma = self.s.turmas.criar(
            self.disciplina.id, self.professor.id, "2026.2", 2)

    def tearDown(self):
        self.conn.close()

    def novo_aluno(self, n: int, curso_id=None):
        return self.s.pessoas.cadastrar_aluno(
            f"Aluno Numero{n}", f"aluno{n}@x.edu", f"RA{n}", curso_id or self.curso.id)
