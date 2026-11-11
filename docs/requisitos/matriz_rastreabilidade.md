# Matriz de rastreabilidade


| Requisito | Operação/componente | Testes relacionados |
|---|---|---|
| RF01 | `CursoService.cadastrar_curso` | `tests/test_servicos.py` — `test_rf01_curso_duplicado` |
| RF02 | `CursoService.cadastrar_disciplina` | `tests/test_servicos.py` — `test_rf02_disciplina_em_curso_inexistente` |
| RF03 | `PessoaService.cadastrar_professor` | `tests/test_servicos.py` — cobertura de cadastro/listagem em `test_rf14_rf15_listagens`; domínio em `test_dominio.py` |
| RF04 | `PessoaService.cadastrar_aluno` | `tests/test_servicos.py` — `test_rf04_aluno_em_curso_inexistente` |
| RF05 | `PessoaService.editar_aluno` | `tests/test_servicos.py` — `test_rf05_editar_aluno`, `test_rf05_editar_aluno_inexistente_ou_email_invalido` |
| RF06 | `TurmaService.criar` | `tests/test_servicos.py` — `test_rf06_turma_com_professor_inexistente` |
| RF07 | `MatriculaService.matricular` | `tests/test_servicos.py` — `test_rf07_matricular_ocupa_vaga`, `test_matricula_duplicada`, `test_turma_lotada`, `test_curso_incompativel` |
| RF08 | `MatriculaService.cancelar` | `tests/test_servicos.py` — `test_rf08_cancelar_libera_vaga_e_permite_rematricula`, `test_cancelar_sem_matricula` |
| RF09 | `MatriculaService.lancar_nota` | `tests/test_servicos.py` — `test_rf09_rf11_boletim_media_ponderada`, `test_nota_invalida_nao_e_gravada`; `tests/test_dominio.py` |
| RF10 | Registro de faltas e cálculo da situação | `tests/test_servicos.py` — `test_rf10_faltas_reprovam_por_frequencia`, `test_faltas_acima_da_carga_horaria`; `tests/test_avaliacao.py` |
| RF11 | `MatriculaService.boletim` | `tests/test_servicos.py` — `test_rf09_rf11_boletim_media_ponderada`, `test_sem_notas_em_andamento` |
| RF12 | `MatriculaService.alunos_da_turma` | `tests/test_servicos.py` — `test_rf12_alunos_da_turma` |
| RF13 | `MatriculaService.relatorio_turma` | `tests/test_servicos.py` — `test_rf13_relatorio_da_turma`, `test_relatorio_turma_sem_notas` |
| RF14 | Listagem de cursos e disciplinas | `tests/test_servicos.py` — `test_rf14_rf15_listagens` |
| RF15 | Listagem de alunos, professores e turmas | `tests/test_servicos.py` — `test_rf14_rf15_listagens` |

## Requisitos não funcionais

| Requisito | Verificação existente ou necessária |
|---|---|
| RNF01 | Verificar versão instalada e execução em Python 3.10+. |
| RNF02 | `requirements.txt` registra ausência de dependência externa obrigatória. Testar em ambiente limpo. |
| RNF03 | Persistência exercitada em `tests/test_persistencia.py`; complementar com teste de reinício da aplicação, se necessário. |
| RNF04 | Restrições no `database/schema.sql` e `tests/test_persistencia.py`. |
| RNF05 | `tests/test_dominio.py` e `tests/test_avaliacao.py`. |
| RNF06 | Verificação estrutural por revisão do código. |
| RNF07 | `tests/test_cli.py`. |
| RNF08 | Execução da suíte `unittest`; resultado da cópia analisada: 66 testes aprovados. |

## Limitação

O pacote ZIP não inclui relatório de cobertura de código nem ferramenta de cobertura. Portanto, não se declara percentual de cobertura.
