from sistema_academico.ui.database import conectar
from sistema_academico.domain.aluno import Aluno


class AlunoRepository:
    """Responsável exclusivamente pelo acesso aos dados de alunos."""

    def cadastrar(self, aluno: Aluno) -> Aluno:
        with conectar() as conexao:
            cursor = conexao.execute(
                "INSERT INTO alunos (nome, email) VALUES (?, ?)",
                (aluno.nome, aluno.email),
            )
            return Aluno(cursor.lastrowid, aluno.nome, aluno.email)

    def listar(self) -> list[Aluno]:
        with conectar() as conexao:
            linhas = conexao.execute(
                "SELECT id, nome, email FROM alunos ORDER BY nome"
            ).fetchall()
        return [Aluno(l["id"], l["nome"], l["email"]) for l in linhas]

    def buscar_por_id(self, aluno_id: int) -> Aluno | None:
        with conectar() as conexao:
            l = conexao.execute(
                "SELECT id, nome, email FROM alunos WHERE id = ?", (aluno_id,)
            ).fetchone()
        return Aluno(l["id"], l["nome"], l["email"]) if l else None