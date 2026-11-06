# Casos de uso

**Ator:** Operador do sistema. A aplicação não possui autenticação; o ator representa a pessoa que utiliza os menus locais.

```mermaid
flowchart LR
  operador([Operador do sistema])
  subgraph sistema[ Sistema Acadêmico - terminal ]
    UC01([Cadastrar curso])
    UC02([Cadastrar disciplina])
    UC03([Listar cursos e disciplinas])
    UC04([Cadastrar aluno])
    UC05([Editar aluno])
    UC06([Listar alunos])
    UC07([Cadastrar professor])
    UC08([Listar professores])
    UC09([Criar turma])
    UC10([Listar turmas])
    UC11([Listar alunos da turma])
    UC12([Consultar relatório da turma])
    UC13([Matricular aluno])
    UC14([Cancelar matrícula])
    UC15([Lançar nota])
    UC16([Registrar faltas])
    UC17([Consultar boletim])
  end
  operador --- UC01
  operador --- UC02
  operador --- UC03
  operador --- UC04
  operador --- UC05
  operador --- UC06
  operador --- UC07
  operador --- UC08
  operador --- UC09
  operador --- UC10
  operador --- UC11
  operador --- UC12
  operador --- UC13
  operador --- UC14
  operador --- UC15
  operador --- UC16
  operador --- UC17
```

O desenho usa flowchart Mermaid para representar as funcionalidades oferecidas pelos menus; não é um diagrama de casos de uso UML desenhado com notação gráfica UML formal.
