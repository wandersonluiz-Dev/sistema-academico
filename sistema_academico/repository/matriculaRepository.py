from sistema_academico.ui.database import conectar
from sistema_academico.domain.matricula import Matricula


class MatriculaRepository:
    """Responsável por persistir matrículas e consultar seus dados."""

    def cadastrar(self, aluno_id: int, disciplina_id: int) -> Matricula:
        with conectar() as conexao:
            cursor = conexao.execute(
                "INSERT INTO matriculas (aluno_id, disciplina_id) VALUES (?, ?)",
                (aluno_id, disciplina_id),
            )
            return Matricula(cursor.lastrowid, aluno_id, disciplina_id)

    def buscar_por_id(self, matricula_id: int) -> Matricula | None:
        with conectar() as conexao:
            l = conexao.execute(
                "SELECT id, aluno_id, disciplina_id, nota1, nota2 "
                "FROM matriculas WHERE id = ?", (matricula_id,)
            ).fetchone()
        return self._para_objeto(l) if l else None

    def registrar_notas(self, matricula_id: int, nota1: float, nota2: float) -> None:
        with conectar() as conexao:
            cursor = conexao.execute(
                "UPDATE matriculas SET nota1 = ?, nota2 = ? WHERE id = ?",
                (nota1, nota2, matricula_id),
            )
            if cursor.rowcount == 0:
                raise ValueError("Matrícula não encontrada.")

    def listar_detalhadas(self) -> list[dict]:
        with conectar() as conexao:
            linhas = conexao.execute("""
                SELECT m.id, a.nome AS aluno, d.nome AS disciplina,
                       m.nota1, m.nota2
                FROM matriculas m
                JOIN alunos a ON a.id = m.aluno_id
                JOIN disciplinas d ON d.id = m.disciplina_id
                ORDER BY a.nome, d.nome
            """).fetchall()
        return [dict(l) for l in linhas]

    @staticmethod
    def _para_objeto(linha) -> Matricula:
        return Matricula(
            linha["id"], linha["aluno_id"], linha["disciplina_id"],
            linha["nota1"], linha["nota2"]
        )