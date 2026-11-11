# Modelo do banco de dados

## Tecnologia e inicialização

O banco utiliza SQLite. O arquivo `database/schema.sql` contém os comandos `CREATE TABLE IF NOT EXISTS`. A função `inicializar_schema()` lê esse arquivo e executa o esquema na conexão aberta pela aplicação.

## Tabelas e campos

| Tabela | Campos definidos no esquema | Finalidade |
|---|---|---|
| `cursos` | `id`, `codigo`, `nome`, `duracao_semestres` | Cadastro de cursos. Código único; duração maior que zero. |
| `disciplinas` | `id`, `codigo`, `nome`, `carga_horaria`, `tipo_media`, `curso_id` | Disciplinas vinculadas a curso. Tipo de média `aritmetica` ou `ponderada`. |
| `professores` | `id`, `nome`, `email`, `titulacao` | Cadastro de professores. E-mail único. |
| `alunos` | `id`, `ra`, `nome`, `email`, `curso_id` | Cadastro de alunos vinculados a curso. RA e e-mail únicos. |
| `turmas` | `id`, `disciplina_id`, `professor_id`, `semestre`, `vagas` | Oferta de disciplina por professor em um semestre. |
| `matriculas` | `id`, `aluno_id`, `turma_id`, `faltas`, `ativa` | Relação do aluno com a turma, com faltas e situação ativa. Par aluno/turma único. |
| `notas` | `id`, `matricula_id`, `descricao`, `valor`, `peso` | Notas vinculadas à matrícula. Valor entre 0 e 10 e peso maior que zero. |

## Relacionamentos

- Um curso pode possuir várias disciplinas.
- Um curso pode possuir vários alunos.
- Uma disciplina pode ser oferecida em várias turmas.
- Um professor pode estar associado a várias turmas.
- Um aluno pode possuir várias matrículas.
- Uma turma pode receber várias matrículas.
- Uma matrícula pode possuir várias notas.

## Restrições definidas no SQL

- Chaves primárias inteiras com `AUTOINCREMENT`.
- Chaves estrangeiras para as relações entre tabelas.
- `UNIQUE` para código de curso, código de disciplina, e-mail de professor, RA de aluno, e-mail de aluno e combinação aluno/turma.
- `CHECK` para duração e carga horária positivas, tipo de média permitido, vagas positivas, faltas não negativas, matrícula ativa em 0 ou 1, nota entre 0 e 10 e peso positivo.

