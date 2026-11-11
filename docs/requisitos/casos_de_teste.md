# Casos de teste

Os casos abaixo foram organizados a partir dos métodos existentes nos arquivos `tests/test_*.py`. A coluna de resultado descreve o comportamento esperado/verificado pelo teste. A suíte executada na cópia analisada totalizou 66 testes aprovados.

| ID | Cenário | Resultado esperado | Teste existente |
|---|---|---|---|
| CT01 | Calcular média aritmética de notas | Retornar média simples arredondada em duas casas | `test_avaliacao.py::test_aritmetica` |
| CT02 | Calcular média ponderada | Considerar os pesos das notas | `test_avaliacao.py::test_ponderada` |
| CT03 | Tentar calcular média sem notas | Gerar erro de validação | `test_avaliacao.py::test_sem_notas` |
| CT04 | Informar nota fora de 0 a 10 ou peso não positivo | Rejeitar os dados | `test_avaliacao.py::test_nota_e_peso_invalidos` |
| CT05 | Frequência abaixo do mínimo com nota alta | Situação `Reprovado por falta` | `test_avaliacao.py::test_reprovado_por_falta_mesmo_com_nota_alta` |
| CT06 | Criar pessoa com e-mail inválido | Gerar erro de validação | `test_dominio.py::test_email_invalido` |
| CT07 | Cadastrar aluno sem RA ou curso válido | Rejeitar cadastro | `test_dominio.py::test_aluno_exige_ra_e_curso` |
| CT08 | Criar turma com semestre inválido | Rejeitar formato diferente de `AAAA.S` | `test_dominio.py::test_turma_semestre_invalido` |
| CT09 | Registrar faltas acima da carga horária | Rejeitar operação | `test_dominio.py::test_faltas_acima_da_carga` |
| CT10 | Matricular aluno de curso incompatível | Rejeitar matrícula | `test_servicos.py::test_curso_incompativel` |
| CT11 | Matricular aluno em turma lotada | Rejeitar matrícula | `test_servicos.py::test_turma_lotada` |
| CT12 | Matricular novamente aluno já matriculado | Rejeitar duplicidade ativa | `test_servicos.py::test_matricula_duplicada` |
| CT13 | Cancelar matrícula e matricular novamente | Liberar vaga e reativar matrícula existente | `test_servicos.py::test_rf08_cancelar_libera_vaga_e_permite_rematricula` |
| CT14 | Lançar nota em matrícula ativa e consultar boletim | Persistir nota e exibir média/situação | `test_servicos.py::test_rf09_rf11_boletim_media_ponderada` |
| CT15 | Informar opção inválida ou provocar erro de domínio na CLI | Exibir mensagem e manter o menu em execução | `test_cli.py` |

## Execução

Na raiz do projeto:

```bash
python -m unittest discover -s tests -t . -v
```

Resultado observado nesta cópia: `Ran 66 tests ... OK`.
