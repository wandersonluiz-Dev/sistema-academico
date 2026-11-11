# Gerenciamento do projeto

## 1. Identificação

- Projeto: Sistema Acadêmico.
- Disciplina: Projeto e Engenharia de Software.
- Professor indicado no README: Christian Azonyetin.
- Versão do código documentada: 0.1.0.
- Repositório: inserir URL efetiva do GitHub.
- Integrantes: preencher os nomes reais.

O README principal apresenta quatro papéis: código/Git/manutenção; gerenciamento/processo; requisitos/qualidade; UML/arquitetura. O enunciado da atividade fornecido para análise indica limite de três integrantes. A equipe deve confirmar com o professor se houve autorização para quatro participantes.

## 2. Objetivo

Desenvolver e documentar uma aplicação de terminal para organizar dados acadêmicos de cursos, disciplinas, alunos, professores, turmas, matrículas, notas e faltas, utilizando Python, SQLite, orientação a objetos, arquitetura em camadas, testes e Git.

## 3. Escopo da versão 0.1.0

**Incluído:** cadastros e listagens de cursos, disciplinas, alunos e professores; edição de dados do aluno; criação/listagem de turmas; matrícula e cancelamento; lançamento de notas; registro de faltas; boletim; listagem de alunos por turma; relatório da turma.

**Não incluído:** API REST, login/autenticação, perfis de acesso, interface gráfica, integração externa, pagamentos ou notificações.

## 4. Partes interessadas

- Professor da disciplina: define o trabalho e avalia os artefatos.
- Integrantes: planejam, desenvolvem, testam e documentam.
- Operador simulado: utiliza os menus do sistema.
- Alunos e professores cadastrados: são representados como registros acadêmicos no sistema; não há interface própria para eles.

## 5. Processo de desenvolvimento

O `README.md` e os scripts indicam um fluxo de desenvolvimento com branches `main`, `develop` e branches de trabalho `feature/*` e `fix/*`. O `scripts/setup_git.sh` inicializa `main`, cria o commit inicial e cria a branch `develop`. O README recomenda abrir Pull Requests das branches de trabalho para `develop`, com revisão por outro integrante.

O pacote ZIP não contém a pasta `.git`; por isso, não é possível comprovar por este arquivo quais branches, commits, PRs ou revisões foram efetivamente realizados. Essas evidências devem ser obtidas no repositório remoto.

## 6. Comparação e escolha do processo

O código e o README mostram divisão por componentes e orientação para integrar mudanças por branches. A documentação descreve a abordagem como desenvolvimento incremental por módulos. Não há evidência no pacote de execução formal do Scrum (sprints, Product Owner, Scrum Master, Planning, Review e Retrospective); portanto, não declarar adoção formal do Scrum sem comprovação.

A comparação está em `comparacao_processos.md`.

## 7. Responsabilidades indicadas no README

| Papel | Responsabilidade indicada | Integrante |
|---|---|---|
| Integrante 1 | Código, Git e manutenção | Preencher nome |
| Integrante 2 | Gerenciamento do projeto e processo | Preencher nome |
| Integrante 3 | Requisitos e qualidade (testes) | Preencher nome |
| Integrante 4 | UML e arquitetura | Preencher nome |

A equipe deve preencher os nomes e confirmar a composição com o professor.

## 8. Critérios de conclusão

- Funcionalidades da versão 0.1.0 disponíveis no menu.
- Dados armazenados em SQLite.
- Testes automatizados executados.
- Documentação e diagramas coerentes com o código entregue.
- Repositório atualizado e evidências de Git disponíveis.
- Integrantes preparados para explicar a arquitetura, regras e funcionamento.

## 9. Documentos complementares

- `backlog.md`
- `comparacao_processos.md`
- `relatorio_tecnico_final.md`

Datas, atas, horas trabalhadas, decisões e responsáveis devem ser preenchidos com informações reais do grupo.
