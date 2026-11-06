"""Testes de integração dos casos de uso (RF01 a RF15)."""
from sistema_academico.dominio.avaliacao import CriterioAprovacao
from sistema_academico.dominio.excecoes import (
    ErroDuplicado, ErroNaoEncontrado, ErroRegraNegocio, ErroValidacao,
)
from sistema_academico.montagem import montar_servicos
from tests.base import BaseComServicos


class TestCadastros(BaseComServicos):
    def test_rf01_curso_duplicado(self):
        with self.assertRaises(ErroDuplicado):
            self.s.cursos.cadastrar_curso("ADS", "Outro", 4)

    def test_rf02_disciplina_em_curso_inexistente(self):
        with self.assertRaises(ErroNaoEncontrado):
            self.s.cursos.cadastrar_disciplina("X1", "Disc", 40, 999)

    def test_rf04_aluno_em_curso_inexistente(self):
        with self.assertRaises(ErroNaoEncontrado):
            self.s.pessoas.cadastrar_aluno("Bia Costa", "b@x.edu", "9", 999)

    def test_rf05_editar_aluno(self):
        aluno = self.s.pessoas.editar_aluno(self.aluno.id, nome="Ana Maria Souza")
        self.assertEqual(aluno.nome, "Ana Maria Souza")
        self.assertEqual(aluno.email, "ana@x.edu")        # não informado: mantém

    def test_rf05_editar_aluno_inexistente_ou_email_invalido(self):
        with self.assertRaises(ErroNaoEncontrado):
            self.s.pessoas.editar_aluno(999, nome="Fulano")
        with self.assertRaises(ErroValidacao):
            self.s.pessoas.editar_aluno(self.aluno.id, email="ruim")

    def test_rf06_turma_com_professor_inexistente(self):
        with self.assertRaises(ErroNaoEncontrado):
            self.s.turmas.criar(self.disciplina.id, 999, "2026.2", 10)

    def test_rf14_rf15_listagens(self):
        self.assertEqual(len(self.s.cursos.listar_cursos()), 1)
        self.assertEqual(len(self.s.cursos.listar_disciplinas(self.curso.id)), 1)
        self.assertEqual(len(self.s.pessoas.listar_alunos()), 1)
        self.assertEqual(len(self.s.pessoas.listar_professores()), 1)
        resumo = self.s.turmas.listar()[0]
        self.assertEqual((resumo.vagas, resumo.ocupadas), (2, 0))


class TestMatricula(BaseComServicos):
    def test_rf07_matricular_ocupa_vaga(self):
        self.s.matriculas.matricular(self.aluno.id, self.turma.id)
        self.assertEqual(self.s.turmas.listar()[0].ocupadas, 1)

    def test_matricula_duplicada(self):
        self.s.matriculas.matricular(self.aluno.id, self.turma.id)
        with self.assertRaises(ErroRegraNegocio):
            self.s.matriculas.matricular(self.aluno.id, self.turma.id)

    def test_turma_lotada(self):
        self.s.matriculas.matricular(self.aluno.id, self.turma.id)
        self.s.matriculas.matricular(self.novo_aluno(2).id, self.turma.id)
        with self.assertRaises(ErroRegraNegocio):
            self.s.matriculas.matricular(self.novo_aluno(3).id, self.turma.id)

    def test_curso_incompativel(self):
        outro = self.s.cursos.cadastrar_curso("DIR", "Direito", 10)
        aluno_direito = self.novo_aluno(5, curso_id=outro.id)
        with self.assertRaises(ErroRegraNegocio):
            self.s.matriculas.matricular(aluno_direito.id, self.turma.id)

    def test_aluno_ou_turma_inexistente(self):
        with self.assertRaises(ErroNaoEncontrado):
            self.s.matriculas.matricular(999, self.turma.id)
        with self.assertRaises(ErroNaoEncontrado):
            self.s.matriculas.matricular(self.aluno.id, 999)

    def test_rf08_cancelar_libera_vaga_e_permite_rematricula(self):
        self.s.matriculas.matricular(self.aluno.id, self.turma.id)
        self.s.matriculas.cancelar(self.aluno.id, self.turma.id)
        self.assertEqual(self.s.turmas.listar()[0].ocupadas, 0)
        self.s.matriculas.matricular(self.aluno.id, self.turma.id)   # reativa
        self.assertEqual(self.s.turmas.listar()[0].ocupadas, 1)

    def test_cancelar_sem_matricula(self):
        with self.assertRaises(ErroNaoEncontrado):
            self.s.matriculas.cancelar(self.aluno.id, self.turma.id)

    def test_lancar_nota_exige_matricula_ativa(self):
        with self.assertRaises(ErroNaoEncontrado):
            self.s.matriculas.lancar_nota(self.aluno.id, self.turma.id, 8)


class TestNotasBoletimRelatorio(BaseComServicos):
    def setUp(self):
        super().setUp()
        self.m = self.s.matriculas
        self.m.matricular(self.aluno.id, self.turma.id)

    def test_rf09_rf11_boletim_media_ponderada(self):
        # disciplina configurada como "ponderada"
        self.m.lancar_nota(self.aluno.id, self.turma.id, 10, peso=3, descricao="Projeto")
        self.m.lancar_nota(self.aluno.id, self.turma.id, 5, peso=2, descricao="Prova")
        r = self.m.boletim(self.aluno.id)[0]
        self.assertEqual(r.media, 8.0)
        self.assertEqual(r.situacao, "Aprovado")
        self.assertEqual(len(r.notas), 2)

    def test_nota_invalida_nao_e_gravada(self):
        with self.assertRaises(ErroValidacao):
            self.m.lancar_nota(self.aluno.id, self.turma.id, 12)
        self.assertEqual(self.m.boletim(self.aluno.id)[0].notas, ())

    def test_sem_notas_em_andamento(self):
        self.assertEqual(self.m.boletim(self.aluno.id)[0].situacao, "Em andamento")

    def test_rf10_faltas_reprovam_por_frequencia(self):
        self.m.lancar_nota(self.aluno.id, self.turma.id, 10)
        self.m.registrar_faltas(self.aluno.id, self.turma.id, 21)   # 21/80 -> 73,75%
        r = self.m.boletim(self.aluno.id)[0]
        self.assertEqual(r.situacao, "Reprovado por falta")
        self.assertAlmostEqual(r.frequencia, 0.7375)

    def test_faltas_acima_da_carga_horaria(self):
        with self.assertRaises(ErroValidacao):
            self.m.registrar_faltas(self.aluno.id, self.turma.id, 81)

    def test_rf12_alunos_da_turma(self):
        outro = self.novo_aluno(2)
        self.m.matricular(outro.id, self.turma.id)
        self.m.lancar_nota(outro.id, self.turma.id, 4)
        nomes = {r.aluno: r.situacao for r in self.m.alunos_da_turma(self.turma.id)}
        self.assertEqual(nomes["Ana Souza"], "Em andamento")
        self.assertEqual(nomes["Aluno Numero2"], "Recuperação")

    def test_rf13_relatorio_da_turma(self):
        outro = self.novo_aluno(2)
        self.m.matricular(outro.id, self.turma.id)
        self.m.lancar_nota(self.aluno.id, self.turma.id, 9)
        self.m.lancar_nota(outro.id, self.turma.id, 3)
        rel = self.m.relatorio_turma(self.turma.id)
        self.assertEqual((rel.aprovados, rel.reprovados, rel.recuperacao), (1, 1, 0))
        self.assertEqual(rel.media_geral, 6.0)
        self.assertEqual((rel.ocupadas, rel.vagas), (2, 2))

    def test_relatorio_turma_sem_notas(self):
        rel = self.m.relatorio_turma(self.turma.id)
        self.assertIsNone(rel.media_geral)
        self.assertEqual(rel.em_andamento, 1)

    def test_criterio_de_aprovacao_alterado_manutencao_adaptativa(self):
        self.m.lancar_nota(self.aluno.id, self.turma.id, 6.0)
        self.assertEqual(self.m.boletim(self.aluno.id)[0].situacao, "Recuperação")
        flexivel = montar_servicos(self.conn, CriterioAprovacao(media_aprovacao=6.0))
        self.assertEqual(flexivel.matriculas.boletim(self.aluno.id)[0].situacao, "Aprovado")
