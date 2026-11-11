# Manual do usuário

## 1. Iniciar

1. Abra um terminal na pasta raiz do repositório.
2. Confirme que o Python 3.10 ou superior está instalado.
3. Execute:

```bash
python main.py
```

O banco SQLite padrão é criado em `database/academico.db` na primeira execução. O programa apresenta o título `Sistema Acadêmico` e o menu principal.

## 2. Menu principal

O menu principal apresenta quatro grupos:

1. Cursos e disciplinas.
2. Alunos e professores.
3. Turmas.
4. Matrículas, notas e faltas.

Digite o número da opção desejada. A opção `0` volta ao menu anterior; no menu principal, encerra a navegação.

## 3. Ordem recomendada para uma demonstração

Para realizar uma matrícula, é necessário ter os registros relacionados previamente cadastrados:

1. Em **Cursos e disciplinas**, cadastre um curso.
2. Cadastre uma disciplina, informando carga horária, ID do curso e tipo de média (`aritmetica` ou `ponderada`).
3. Em **Alunos e professores**, cadastre um aluno com nome, e-mail, RA e ID do curso.
4. Cadastre um professor com nome, e-mail e titulação.
5. Em **Turmas**, crie uma turma informando ID da disciplina, ID do professor, semestre no formato `AAAA.S` (por exemplo, `2026.2`) e número de vagas.
6. Em **Matrículas, notas e faltas**, matricule o aluno informando ID do aluno e ID da turma.
7. Lance uma ou mais notas, informe peso (padrão 1) e descrição.
8. Registre faltas em horas-aula, se necessário.
9. Consulte o boletim do aluno ou o relatório da turma.

## 4. Funções disponíveis

### Cursos e disciplinas
- Cadastrar curso.
- Cadastrar disciplina.
- Listar cursos.
- Listar disciplinas.

### Alunos e professores
- Cadastrar aluno.
- Editar nome e/ou e-mail de aluno (Enter mantém o valor atual).
- Listar alunos.
- Cadastrar professor.
- Listar professores.

### Turmas
- Criar turma.
- Listar turmas, com disciplina, professor, semestre e ocupação.
- Listar alunos da turma com notas, média, frequência e situação.
- Consultar relatório com ocupação, média geral e quantidades por situação.

### Matrículas, notas e faltas
- Matricular aluno em turma.
- Cancelar matrícula.
- Lançar nota (0 a 10), peso maior que zero e descrição opcional.
- Registrar faltas em horas-aula.
- Consultar boletim do aluno.

## 5. Regras importantes

- O aluno deve pertencer ao mesmo curso da disciplina da turma.
- A turma não pode ultrapassar o limite de vagas.
- Não é permitido manter matrícula ativa duplicada do mesmo aluno na mesma turma.
- Matrícula cancelada pode ser reativada ao matricular novamente, se houver vaga e as regras forem atendidas.
- Nota deve estar entre 0 e 10; peso deve ser maior que zero.
- Faltas devem ser positivas e não podem ultrapassar a carga horária.
- A frequência mínima padrão é 75%; média padrão para aprovação é 7,0 e para recuperação é 4,0.

## 6. Dados de demonstração

O script opcional `python scripts/popular_dados.py` cadastra dados de exemplo. Como ele insere registros novamente ao ser executado, utilize banco novo ou faça backup para evitar duplicidades.

## 7. Encerrar

No menu principal, escolha `0 - Sair`. Os registros permanecem no arquivo SQLite utilizado pela aplicação.
