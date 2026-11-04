"""Testes de integração dos repositórios com SQLite em memória."""
import unittest

from sistema_academico.dominio.avaliacao import Nota
from sistema_academico.dominio.curso import Curso, Disciplina
from sistema_academico.dominio.excecoes import ErroDuplicado, ErroNaoEncontrado
from sistema_academico.dominio.matricula import Matricula
from sistema_academico.dominio.pessoa import Aluno, Professor
from sistema_academico.persistencia.conexao import abrir_conexao, inicializar_schema
from sistema_academico.persistencia.curso_repository import CursoRepository, DisciplinaRepository
from sistema_academico.persistencia.matricula_repository import MatriculaRepository
from sistema_academico.persistencia.pessoa_repository import AlunoRepository, ProfessorRepository
from sistema_academico.persistencia.turma_repository import TurmaRepository
from sistema_academico.dominio.turma import Turma


class TestRepositorios(unittest.TestCase):
    def setUp(self):
        self.conn = abrir_conexao(":memory:")
        inicializar_schema(self.conn)
        self.cursos = CursoRepository(self.conn)
        self.curso = self.cursos.inserir(Curso("ADS", "Sistemas", 5))

    def tearDown(self):
        self.conn.close()

    def test_curso_salvar_buscar_listar(self):
        self.assertEqual(self.cursos.buscar_por_id(self.curso.id).codigo, "ADS")
        self.assertEqual(len(self.cursos.listar()), 1)
        self.assertIsNone(self.cursos.buscar_por_id(999))

    def test_codigo_de_curso_duplicado(self):
        with self.assertRaises(ErroDuplicado):
            self.cursos.inserir(Curso("ads", "Outro", 4))

    def test_disciplina_com_curso_inexistente(self):
        with self.assertRaises(ErroNaoEncontrado):
            DisciplinaRepository(self.conn).inserir(Disciplina("X1", "Disc", 40, 999))

    def test_aluno_ra_e_email_duplicados(self):
        repo = AlunoRepository(self.conn)
        repo.inserir(Aluno("Ana Souza", "a@x.com", "1", self.curso.id))
        with self.assertRaises(ErroDuplicado):
            repo.inserir(Aluno("Outra Ana", "b@x.com", "1", self.curso.id))
        with self.assertRaises(ErroDuplicado):
            repo.inserir(Aluno("Outra Ana", "a@x.com", "2", self.curso.id))

    def test_aluno_atualizar(self):
        repo = AlunoRepository(self.conn)
        aluno = repo.inserir(Aluno("Ana Souza", "a@x.com", "1", self.curso.id))
        aluno.nome = "Ana Maria Souza"
        repo.atualizar(aluno)
        self.assertEqual(repo.buscar_por_id(aluno.id).nome, "Ana Maria Souza")

    def test_matricula_com_notas_e_faltas(self):
        aluno = AlunoRepository(self.conn).inserir(Aluno("Ana Souza", "a@x.com", "1", self.curso.id))
        prof = ProfessorRepository(self.conn).inserir(Professor("Carlos Lima", "c@x.com", "Mestre"))
        disc = DisciplinaRepository(self.conn).inserir(Disciplina("E1", "Eng", 80, self.curso.id))
        turma = TurmaRepository(self.conn).inserir(Turma(disc.id, prof.id, "2026.2", 10))
        repo = MatriculaRepository(self.conn)

        m = repo.inserir(Matricula(aluno.id, turma.id))
        repo.adicionar_nota(m.id, Nota(8.5, 2, "Prova"))
        m.registrar_faltas(4, 80)
        repo.salvar_estado(m)

        lida = repo.buscar(aluno.id, turma.id)
        self.assertEqual(lida.faltas, 4)
        self.assertEqual(lida.notas[0].valor, 8.5)
        self.assertEqual(lida.notas[0].descricao, "Prova")
        self.assertEqual(repo.contar_ativas_por_turma(turma.id), 1)

        lida.cancelar()
        repo.salvar_estado(lida)
        self.assertEqual(repo.contar_ativas_por_turma(turma.id), 0)
        self.assertEqual(repo.listar_ativas_por_aluno(aluno.id), [])


if __name__ == "__main__":
    unittest.main()
