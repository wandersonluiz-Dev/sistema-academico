"""Casos de uso: matrículas, notas, faltas, boletim e relatório
(RF07, RF08, RF09, RF10, RF11, RF12, RF13)."""
from __future__ import annotations

from dataclasses import dataclass

from ..dominio.avaliacao import CriterioAprovacao, Nota, calcular_situacao, obter_estrategia
from ..dominio.curso import Disciplina
from ..dominio.excecoes import ErroNaoEncontrado, ErroRegraNegocio
from ..dominio.matricula import Matricula
from ..dominio.pessoa import Aluno
from ..dominio.turma import Turma
from ..persistencia.curso_repository import DisciplinaRepository
from ..persistencia.matricula_repository import MatriculaRepository
from ..persistencia.pessoa_repository import AlunoRepository
from ..persistencia.turma_repository import TurmaRepository


@dataclass(frozen=True)
class ResultadoDisciplina:
    aluno: str
    turma_id: int
    disciplina: str
    semestre: str
    notas: tuple[Nota, ...]
    media: float | None
    frequencia: float
    situacao: str


@dataclass(frozen=True)
class RelatorioTurma:
    turma_id: int
    disciplina: str
    semestre: str
    vagas: int
    ocupadas: int
    media_geral: float | None
    aprovados: int
    recuperacao: int
    reprovados: int
    em_andamento: int


class MatriculaService:
    def __init__(self, matriculas: MatriculaRepository, turmas: TurmaRepository,
                 disciplinas: DisciplinaRepository, alunos: AlunoRepository,
                 criterio: CriterioAprovacao = CriterioAprovacao()) -> None:
        self._matriculas = matriculas
        self._turmas = turmas
        self._disciplinas = disciplinas
        self._alunos = alunos
        self._criterio = criterio

    # ---- matrícula (RF07, RF08) -------------------------------------------
    def matricular(self, aluno_id: int, turma_id: int) -> Matricula:
        aluno = self._aluno(aluno_id)
        turma, disciplina = self._turma_e_disciplina(turma_id)
        if aluno.curso_id != disciplina.curso_id:
            raise ErroRegraNegocio("A disciplina não pertence ao curso do aluno.")
        existente = self._matriculas.buscar(aluno_id, turma_id)
        if existente is not None and existente.ativa:
            raise ErroRegraNegocio("O aluno já está matriculado nesta turma.")
        if not turma.tem_vaga(self._matriculas.contar_ativas_por_turma(turma_id)):
            raise ErroRegraNegocio("Turma lotada: não há vagas disponíveis.")
        if existente is not None:       # matrícula cancelada antes: reativa
            existente.reativar()
            return self._matriculas.salvar_estado(existente)
        return self._matriculas.inserir(Matricula(aluno_id, turma_id))

    def cancelar(self, aluno_id: int, turma_id: int) -> Matricula:
        matricula = self._matricula_ativa(aluno_id, turma_id)
        matricula.cancelar()
        return self._matriculas.salvar_estado(matricula)

    # ---- notas e faltas (RF09, RF10) ---------------------------------------
    def lancar_nota(self, aluno_id: int, turma_id: int, valor: float,
                    peso: float = 1.0, descricao: str = "") -> Nota:
        matricula = self._matricula_ativa(aluno_id, turma_id)
        nota = matricula.lancar_nota(valor, peso, descricao)
        self._matriculas.adicionar_nota(matricula.id, nota)
        return nota

    def registrar_faltas(self, aluno_id: int, turma_id: int, quantidade: int) -> Matricula:
        matricula = self._matricula_ativa(aluno_id, turma_id)
        _, disciplina = self._turma_e_disciplina(turma_id)
        matricula.registrar_faltas(quantidade, disciplina.carga_horaria)
        return self._matriculas.salvar_estado(matricula)

    # ---- consultas (RF11, RF12, RF13) --------------------------------------
    def boletim(self, aluno_id: int) -> list[ResultadoDisciplina]:
        aluno = self._aluno(aluno_id)
        return [self._resultado(m, aluno)
                for m in self._matriculas.listar_ativas_por_aluno(aluno_id)]

    def alunos_da_turma(self, turma_id: int) -> list[ResultadoDisciplina]:
        self._turma_e_disciplina(turma_id)
        return [self._resultado(m, self._aluno(m.aluno_id))
                for m in self._matriculas.listar_ativas_por_turma(turma_id)]

    def relatorio_turma(self, turma_id: int) -> RelatorioTurma:
        turma, disciplina = self._turma_e_disciplina(turma_id)
        resultados = self.alunos_da_turma(turma_id)
        medias = [r.media for r in resultados if r.media is not None]
        contar = lambda s: sum(1 for r in resultados if r.situacao == s)
        return RelatorioTurma(
            turma_id=turma.id, disciplina=disciplina.nome, semestre=turma.semestre,
            vagas=turma.vagas, ocupadas=len(resultados),
            media_geral=round(sum(medias) / len(medias), 2) if medias else None,
            aprovados=contar("Aprovado"), recuperacao=contar("Recuperação"),
            reprovados=contar("Reprovado") + contar("Reprovado por falta"),
            em_andamento=contar("Em andamento"))

    # ---- auxiliares ---------------------------------------------------------
    def _resultado(self, matricula: Matricula, aluno: Aluno) -> ResultadoDisciplina:
        turma, disciplina = self._turma_e_disciplina(matricula.turma_id)
        media = matricula.media(obter_estrategia(disciplina.tipo_media))
        frequencia = matricula.frequencia(disciplina.carga_horaria)
        return ResultadoDisciplina(
            aluno=aluno.nome, turma_id=turma.id, disciplina=disciplina.nome,
            semestre=turma.semestre, notas=matricula.notas, media=media,
            frequencia=frequencia,
            situacao=calcular_situacao(media, frequencia, self._criterio))

    def _aluno(self, aluno_id: int) -> Aluno:
        aluno = self._alunos.buscar_por_id(aluno_id)
        if aluno is None:
            raise ErroNaoEncontrado(f"Aluno {aluno_id} não encontrado.")
        return aluno

    def _turma_e_disciplina(self, turma_id: int) -> tuple[Turma, Disciplina]:
        turma = self._turmas.buscar_por_id(turma_id)
        if turma is None:
            raise ErroNaoEncontrado(f"Turma {turma_id} não encontrada.")
        return turma, self._disciplinas.buscar_por_id(turma.disciplina_id)

    def _matricula_ativa(self, aluno_id: int, turma_id: int) -> Matricula:
        self._aluno(aluno_id)
        self._turma_e_disciplina(turma_id)
        matricula = self._matriculas.buscar(aluno_id, turma_id)
        if matricula is None or not matricula.ativa:
            raise ErroNaoEncontrado("O aluno não possui matrícula ativa nesta turma.")
        return matricula