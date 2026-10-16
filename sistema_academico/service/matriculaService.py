from sistema_academico.domain.matricula import Matricula


class MatriculaService:
    """Orquestra matrículas e aplica regras acadêmicas."""

    def __init__(self, matricula_repository, aluno_repository, disciplina_repository):
        self.repository = matricula_repository
        self.alunos = aluno_repository
        self.disciplinas = disciplina_repository

    def matricular(self, aluno_id: int, disciplina_id: int) -> Matricula:
        if self.alunos.buscar_por_id(aluno_id) is None:
            raise ValueError("Aluno não encontrado.")
        if self.disciplinas.buscar_por_id(disciplina_id) is None:
            raise ValueError("Disciplina não encontrada.")
        try:
            return self.repository.cadastrar(aluno_id, disciplina_id)
        except Exception as erro:
            # A restrição UNIQUE do SQLite impede matrícula duplicada.
            if "UNIQUE constraint failed" in str(erro):
                raise ValueError("Esse aluno já está matriculado nessa disciplina.") from erro
            raise

    def registrar_notas(self, matricula_id: int, nota1: float, nota2: float):
        for nota in (nota1, nota2):
            if not 0 <= nota <= 10:
                raise ValueError("As notas devem estar entre 0 e 10.")
        if self.repository.buscar_por_id(matricula_id) is None:
            raise ValueError("Matrícula não encontrada.")
        self.repository.registrar_notas(matricula_id, nota1, nota2)

    def listar(self):
        return self.repository.listar_detalhadas()
