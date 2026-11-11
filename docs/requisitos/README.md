# Requisitos do Sistema Acadêmico

## 1. Objetivo e escopo

O sistema organiza, por meio de uma aplicação de terminal, cursos, disciplinas, alunos, professores, turmas, matrículas, notas, faltas, boletim e relatório de turma. A versão analisada não possui API nem login.

## 3. Requisitos funcionais

| ID | Requisito funcional | Implementação no código |
|---|---|---|
| RF01 | Cadastrar curso. | `CursoService.cadastrar_curso` |
| RF02 | Cadastrar disciplina com carga horária e tipo de média. | `CursoService.cadastrar_disciplina` |
| RF03 | Cadastrar professor. | `PessoaService.cadastrar_professor` |
| RF04 | Cadastrar aluno vinculado a um curso. | `PessoaService.cadastrar_aluno` |
| RF05 | Editar dados do aluno. | `PessoaService.editar_aluno` |
| RF06 | Criar turma com disciplina, professor, semestre e vagas. | `TurmaService.criar` |
| RF07 | Matricular aluno em turma, validando vagas, curso compatível e duplicidade. | `MatriculaService.matricular` |
| RF08 | Cancelar matrícula. | `MatriculaService.cancelar` |
| RF09 | Lançar nota em matrícula ativa. | `MatriculaService.lancar_nota` |
| RF10 | Registrar faltas e calcular situação considerando média e frequência. | `MatriculaService.registrar_faltas`, `Matricula.media`, `Matricula.frequencia` e `calcular_situacao` |
| RF11 | Consultar boletim do aluno. | `MatriculaService.boletim` |
| RF12 | Listar alunos de uma turma com situação acadêmica. | `MatriculaService.alunos_da_turma` |
| RF13 | Gerar relatório da turma com ocupação, média geral e quantitativos por situação. | `MatriculaService.relatorio_turma` |
| RF14 | Listar cursos e disciplinas. | `CursoService.listar_cursos`, `CursoService.listar_disciplinas` |
| RF15 | Listar alunos, professores e turmas. | `PessoaService.listar_alunos`, `PessoaService.listar_professores`, `TurmaService.listar` |

## 4. Regras de negócio implementadas

1. O aluno só pode ser matriculado em disciplina vinculada ao curso ao qual pertence.
2. A turma não pode ultrapassar o número de vagas.
3. Não é permitida matrícula ativa duplicada do mesmo aluno na mesma turma.
4. Se já existir matrícula cancelada para o mesmo aluno/turma, a operação de matrícula reativa esse registro, desde que as demais validações sejam atendidas.
5. A nota deve estar entre 0 e 10.
6. O peso da nota deve ser maior que zero.
7. A quantidade registrada de faltas deve ser maior que zero e a soma não pode ultrapassar a carga horária da disciplina.
8. A frequência mínima padrão é 75%.
9. A média padrão para aprovação é 7,0; a partir de 4,0 o aluno fica em recuperação; abaixo de 4,0 fica reprovado. Os valores são definidos em `CriterioAprovacao` e podem ser alterados por configuração.
10. Se a frequência ficar abaixo do mínimo, a situação será `Reprovado por falta`, mesmo que a média seja alta.
11. Sem notas, a situação é `Em andamento`, desde que a frequência não determine reprovação por falta.

## 5. Requisitos não funcionais e critérios de verificação


| ID | Requisito não funcional | Critério de verificação |
|---|---|---|
| RNF01 | A aplicação deve executar em Python 3.10 ou superior. | Verificar a versão com `python --version` e executar `python main.py`. |
| RNF02 | A solução não deve depender de bibliotecas externas para executar as funções principais. | Conferir `requirements.txt` e executar a aplicação em ambiente Python limpo. |
| RNF03 | Os dados devem persistir entre execuções por meio de arquivo SQLite. | Cadastrar dado, encerrar a aplicação, iniciar novamente e consultar o registro. |
| RNF04 | O banco deve aplicar integridade referencial e restrições de valores. | Conferir `schema.sql` e executar os testes de persistência. |
| RNF05 | Os dados recebidos devem passar por validações de domínio antes de serem aceitos. | Executar testes de domínio para e-mail, nome, nota, peso, semestre, vagas e faltas. |
| RNF06 | A aplicação deve separar apresentação, serviços, domínio e persistência em módulos próprios. | Inspecionar os diretórios `apresentacao`, `aplicacao`, `dominio` e `persistencia`. |
| RNF07 | A aplicação deve apresentar mensagens para opções inválidas e erros de domínio sem encerrar abruptamente o menu. | Executar `tests/test_cli.py` e testar opção inválida no terminal. |
| RNF08 | O projeto deve possuir testes automatizados executáveis pela biblioteca `unittest`. | Executar `python -m unittest discover -s tests -t . -v`. |

## 6. Rastreabilidade e testes

- Matriz: `matriz_rastreabilidade.md`.
- Casos de teste: `casos_de_teste.md`.
- Suíte automatizada: diretório `../../tests/`.

## 7. Fora do escopo da versão 0.1.0

Não há API REST, login, controle de permissões, interface gráfica, integração externa, pagamento ou envio de notificações.

## 8. Manual

Consultar `manual_do_usuario.md`.
