"""Interface de terminal (menus numerados).

Entrada e saída são injetadas para permitir testes automáticos.
"""
from __future__ import annotations

from typing import Callable

from ..dominio.excecoes import ErroDominio, ErroValidacao
from ..montagem import Servicos


class CLI:
    def __init__(self, servicos: Servicos,
                 entrada: Callable[[str], str] = input,
                 saida: Callable[[str], None] = print) -> None:
        self._s = servicos
        self._in = entrada
        self._out = saida

    # ---- menus -------------------------------------------------------------
    def executar(self) -> None:
        self._out("=== Sistema Acadêmico ===")
        self._menu("MENU PRINCIPAL", [
            ("Cursos e disciplinas", self._menu_cursos),
            ("Alunos e professores", self._menu_pessoas),
            ("Turmas", self._menu_turmas),
            ("Matrículas, notas e faltas", self._menu_matriculas),
        ], saida="Sair")
        self._out("Até logo!")

    def _menu(self, titulo: str, opcoes: list, saida: str = "Voltar") -> None:
        while True:
            self._out(f"\n--- {titulo} ---")
            for i, (rotulo, _) in enumerate(opcoes, start=1):
                self._out(f"{i} - {rotulo}")
            self._out(f"0 - {saida}")
            escolha = self._in("Opção: ").strip()
            if escolha == "0":
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(opcoes):
                self._out("Opção inválida.")
                continue
            try:
                opcoes[int(escolha) - 1][1]()
            except ErroDominio as erro:
                self._out(f"Erro: {erro}")

    def _menu_cursos(self) -> None:
        self._menu("CURSOS E DISCIPLINAS", [
            ("Cadastrar curso", self._cadastrar_curso),
            ("Cadastrar disciplina", self._cadastrar_disciplina),
            ("Listar cursos", self._listar_cursos),
            ("Listar disciplinas", self._listar_disciplinas),
        ])

    def _menu_pessoas(self) -> None:
        self._menu("ALUNOS E PROFESSORES", [
            ("Cadastrar aluno", self._cadastrar_aluno),
            ("Editar aluno", self._editar_aluno),
            ("Listar alunos", self._listar_alunos),
            ("Cadastrar professor", self._cadastrar_professor),
            ("Listar professores", self._listar_professores),
        ])

    def _menu_turmas(self) -> None:
        self._menu("TURMAS", [
            ("Criar turma", self._criar_turma),
            ("Listar turmas", self._listar_turmas),
            ("Alunos da turma", self._alunos_da_turma),
            ("Relatório da turma", self._relatorio_turma),
        ])

    def _menu_matriculas(self) -> None:
        self._menu("MATRÍCULAS, NOTAS E FALTAS", [
            ("Matricular aluno em turma", self._matricular),
            ("Cancelar matrícula", self._cancelar),
            ("Lançar nota", self._lancar_nota),
            ("Registrar faltas", self._registrar_faltas),
            ("Boletim do aluno", self._boletim),
        ])

    # ---- leitura de dados ---------------------------------------------------
    def _ler(self, rotulo: str) -> str:
        return self._in(f"{rotulo}: ").strip()

    def _ler_int(self, rotulo: str) -> int:
        try:
            return int(self._ler(rotulo))
        except ValueError:
            raise ErroValidacao(f"{rotulo} deve ser um número inteiro.") from None

    def _ler_float(self, rotulo: str, padrao: float | None = None) -> float:
        texto = self._ler(rotulo).replace(",", ".")
        if not texto and padrao is not None:
            return padrao
        try:
            return float(texto)
        except ValueError:
            raise ErroValidacao(f"{rotulo} deve ser um número.") from None

    # ---- cursos e disciplinas ----------------------------------------------
    def _cadastrar_curso(self) -> None:
        curso = self._s.cursos.cadastrar_curso(
            self._ler("Código"), self._ler("Nome"), self._ler_int("Duração (semestres)"))
        self._out(f"Curso cadastrado (id {curso.id}): {curso}")

    def _cadastrar_disciplina(self) -> None:
        disciplina = self._s.cursos.cadastrar_disciplina(
            self._ler("Código"), self._ler("Nome"), self._ler_int("Carga horária (h)"),
            self._ler_int("ID do curso"),
            self._ler("Tipo de média (aritmetica/ponderada) [aritmetica]") or "aritmetica")
        self._out(f"Disciplina cadastrada (id {disciplina.id}): {disciplina}")

    def _listar_cursos(self) -> None:
        for c in self._s.cursos.listar_cursos():
            self._out(f"[{c.id}] {c}")

    def _listar_disciplinas(self) -> None:
        for d in self._s.cursos.listar_disciplinas():
            self._out(f"[{d.id}] {d} - curso {d.curso_id}")

    # ---- alunos e professores ----------------------------------------------
    def _cadastrar_aluno(self) -> None:
        aluno = self._s.pessoas.cadastrar_aluno(
            self._ler("Nome"), self._ler("E-mail"), self._ler("RA"), self._ler_int("ID do curso"))
        self._out(f"Aluno cadastrado (id {aluno.id}): {aluno.descricao()}")

    def _editar_aluno(self) -> None:
        aluno_id = self._ler_int("ID do aluno")
        nome = self._ler("Novo nome (Enter mantém)")
        email = self._ler("Novo e-mail (Enter mantém)")
        if not nome and not email:
            self._out("Nada foi alterado.")
            return
        aluno = self._s.pessoas.editar_aluno(aluno_id, nome, email)
        self._out(f"Aluno atualizado: {aluno.nome} <{aluno.email}>")

    def _listar_alunos(self) -> None:
        alunos = self._s.pessoas.listar_alunos()

        if not alunos:
            self._out("Nenhum aluno cadastrado.")
            return

        for a in alunos:
            self._out(f"[{a.id}] {a.descricao()} <{a.email}> - curso {a.curso_id}")

    def _cadastrar_professor(self) -> None:
        prof = self._s.pessoas.cadastrar_professor(
            self._ler("Nome"), self._ler("E-mail"), self._ler("Titulação"))
        self._out(f"Professor cadastrado (id {prof.id}): {prof.descricao()}")

    def _listar_professores(self) -> None:
        for p in self._s.pessoas.listar_professores():
            self._out(f"[{p.id}] {p.descricao()} <{p.email}>")

    # ---- turmas --------------------------------------------------------------
    def _criar_turma(self) -> None:
        turma = self._s.turmas.criar(
            self._ler_int("ID da disciplina"), self._ler_int("ID do professor"),
            self._ler("Semestre (ex.: 2027.1)"), self._ler_int("Vagas"))
        self._out(f"Turma criada (id {turma.id}).")

    def _listar_turmas(self) -> None:
        for t in self._s.turmas.listar():
            self._out(f"[{t.id}] {t.disciplina} - Prof. {t.professor} - {t.semestre} "
                      f"- vagas {t.ocupadas}/{t.vagas}")

    def _alunos_da_turma(self) -> None:
        for r in self._s.matriculas.alunos_da_turma(self._ler_int("ID da turma")):
            self._out(self._linha_resultado(r, mostrar_aluno=True))

    def _relatorio_turma(self) -> None:
        r = self._s.matriculas.relatorio_turma(self._ler_int("ID da turma"))
        media = "-" if r.media_geral is None else f"{r.media_geral:.2f}"
        self._out(f"Turma {r.turma_id} - {r.disciplina} ({r.semestre})")
        self._out(f"Ocupação: {r.ocupadas}/{r.vagas} | Média geral: {media}")
        self._out(f"Aprovados: {r.aprovados} | Recuperação: {r.recuperacao} | "
                  f"Reprovados: {r.reprovados} | Em andamento: {r.em_andamento}")

    # ---- matrículas ----------------------------------------------------------
    def _matricular(self) -> None:
        self._s.matriculas.matricular(self._ler_int("ID do aluno"), self._ler_int("ID da turma"))
        self._out("Matrícula realizada com sucesso.")

    def _cancelar(self) -> None:
        self._s.matriculas.cancelar(self._ler_int("ID do aluno"), self._ler_int("ID da turma"))
        self._out("Matrícula cancelada.")

    def _lancar_nota(self) -> None:
        aluno, turma = self._ler_int("ID do aluno"), self._ler_int("ID da turma")
        valor = self._ler_float("Nota (0 a 10)")
        peso = self._ler_float("Peso [1]", padrao=1.0)
        descricao = self._ler("Descrição (ex.: Prova 1)")
        self._s.matriculas.lancar_nota(aluno, turma, valor, peso, descricao)
        self._out("Nota lançada.")

    def _registrar_faltas(self) -> None:
        m = self._s.matriculas.registrar_faltas(
            self._ler_int("ID do aluno"), self._ler_int("ID da turma"),
            self._ler_int("Quantidade de faltas (horas-aula)"))
        self._out(f"Faltas registradas. Total: {m.faltas}.")

    def _boletim(self) -> None:
        resultados = self._s.matriculas.boletim(self._ler_int("ID do aluno"))
        if not resultados:
            self._out("Nenhuma matrícula ativa.")
        for r in resultados:
            self._out(self._linha_resultado(r))

    @staticmethod
    def _linha_resultado(r, mostrar_aluno: bool = False) -> str:
        media = "-" if r.media is None else f"{r.media:.2f}"
        notas = ", ".join(f"{n.valor:g}" for n in r.notas) or "sem notas"
        inicio = f"{r.aluno:<25}" if mostrar_aluno else f"{r.disciplina} ({r.semestre})"
        return (f"{inicio} | notas: {notas} | média: {media} | "
                f"freq: {r.frequencia:.0%} | {r.situacao}")
