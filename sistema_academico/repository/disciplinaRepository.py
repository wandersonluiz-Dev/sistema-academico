from sistema_academico.ui.database import conectar
from sistema_academico.domain.disciplina import Disciplina


class DisciplinaRepository:
    """Responsável exclusivamente pelo acesso aos dados de disciplinas."""

    def cadastrar(self, disciplina: Disciplina) -> Disciplina:
        with conectar() as conexao:
            cursor = conexao.execute(
                "INSERT INTO disciplinas (nome, carga_horaria) VALUES (?, ?)",
                (disciplina.nome, disciplina.carga_horaria),
            )
            return Disciplina(cursor.lastrowid, disciplina.nome, disciplina.carga_horaria)

    def listar(self) -> list[Disciplina]:
        with conectar() as conexao:
            linhas = conexao.execute(
                "SELECT id, nome, carga_horaria FROM disciplinas ORDER BY nome"
            ).fetchall()
        return [Disciplina(l["id"], l["nome"], l["carga_horaria"]) for l in linhas]

    def buscar_por_id(self, disciplina_id: int) -> Disciplina | None:
        with conectar() as conexao:
            l = conexao.execute(
                "SELECT id, nome, carga_horaria FROM disciplinas WHERE id = ?",
                (disciplina_id,),
            ).fetchone()
        return Disciplina(l["id"], l["nome"], l["carga_horaria"]) if l else None