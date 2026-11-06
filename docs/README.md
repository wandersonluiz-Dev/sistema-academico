# Documentação do Sistema Acadêmico

Esta pasta reúne a documentação da versão **0.1.0** do Sistema Acadêmico, conforme o código presente neste repositório.

## Estrutura

| Pasta | Conteúdo | Responsável indicado no README principal |
|---|---|---|
| `gerenciamento/` | Plano, riscos, cronograma, processo, backlog, mudanças e relatório | Integrante 2 |
| `requisitos/` | Levantamento, RF, RNF, rastreabilidade, testes e manual do usuário | Integrante 3 |
| `uml/` | Casos de uso, classes, sequência e atividades | Integrante 4 |
| `arquitetura/` | Arquitetura, padrões, modelo de dados e manual técnico | Integrante 4 |
| `manutencao/` | Registro de manutenção | Integrante 1 |

Os papéis acima reproduzem a divisão indicada no `README.md` do projeto. Os nomes dos integrantes ainda precisam ser preenchidos pela equipe.

## Base utilizada

A documentação foi elaborada a partir dos arquivos `src/sistema_academico/`, `database/schema.sql`, `tests/`, `scripts/`, `README.md` e `CHANGELOG.md` da versão 0.1.0.

## Situação e limites das evidências

- O código implementa uma aplicação de terminal, sem API REST e sem login.
- O banco é SQLite e contém sete tabelas.
- A suíte foi executada na cópia analisada: **66 testes passaram** com `unittest`.
- O arquivo ZIP não contém o histórico Git nem os Pull Requests. Portanto, esta documentação não afirma que todos os integrantes fizeram commits, que houve revisão de PR ou que releases de manutenção já foram publicadas.
- O `CHANGELOG.md` registra a versão 0.1.0. As versões 1.0 a 1.4 aparecem como planejamento, não como versões já entregues.
- O registro de manutenção ainda é um modelo sem ocorrências preenchidas. Não há evidência no pacote de que os quatro ciclos de manutenção tenham sido concluídos.

## Regra do trabalho

O README principal lista quatro papéis, enquanto o enunciado da atividade informado pelo professor estabelece máximo de três integrantes. A equipe deve confirmar a autorização para quatro integrantes com o professor e registrar a orientação recebida.
