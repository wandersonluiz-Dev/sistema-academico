# Diagrama entidade-relacionamento

Diagrama derivado das sete tabelas declaradas em `database/schema.sql`.

```mermaid
erDiagram
  CURSOS ||--o{ DISCIPLINAS : possui
  CURSOS ||--o{ ALUNOS : vincula
  DISCIPLINAS ||--o{ TURMAS : ofertada_em
  PROFESSORES ||--o{ TURMAS : ministra
  ALUNOS ||--o{ MATRICULAS : realiza
  TURMAS ||--o{ MATRICULAS : recebe
  MATRICULAS ||--o{ NOTAS : possui

  CURSOS {
    INTEGER id PK
    TEXT codigo UK
    TEXT nome
    INTEGER duracao_semestres
  }
  DISCIPLINAS {
    INTEGER id PK
    TEXT codigo UK
    TEXT nome
    INTEGER carga_horaria
    TEXT tipo_media
    INTEGER curso_id FK
  }
  PROFESSORES {
    INTEGER id PK
    TEXT nome
    TEXT email UK
    TEXT titulacao
  }
  ALUNOS {
    INTEGER id PK
    TEXT ra UK
    TEXT nome
    TEXT email UK
    INTEGER curso_id FK
  }
  TURMAS {
    INTEGER id PK
    INTEGER disciplina_id FK
    INTEGER professor_id FK
    TEXT semestre
    INTEGER vagas
  }
  MATRICULAS {
    INTEGER id PK
    INTEGER aluno_id FK
    INTEGER turma_id FK
    INTEGER faltas
    INTEGER ativa
  }
  NOTAS {
    INTEGER id PK
    INTEGER matricula_id FK
    TEXT descricao
    REAL valor
    REAL peso
  }
```

As restrições de unicidade e os `CHECK` estão descritos em `../arquitetura/modelo_banco.md` e no próprio `database/schema.sql`.
