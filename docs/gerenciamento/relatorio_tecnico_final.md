# Relatório técnico — Sistema Acadêmico 0.1.0

## 1. Identificação

- Projeto: Sistema Acadêmico.
- Disciplina: Projeto e Engenharia de Software.
- Professor: Christian Azonyetin (conforme README do projeto).
- Integrantes: preencher nomes completos.
- Repositório: inserir URL do GitHub.
- Commit/tag entregue: preencher com o identificador real.

## 2. Objetivo

Desenvolver uma aplicação de terminal para gerenciar cursos, disciplinas, alunos, professores, turmas, matrículas, notas e faltas, com consulta de boletim e relatório de turma.

## 3. Tecnologias

- Python 3.10 ou superior.
- SQLite por meio do módulo `sqlite3`.
- `unittest` para testes automatizados.
- Git e GitHub conforme o fluxo documentado no README.
- Mermaid para os diagramas desta documentação.

O `requirements.txt` não lista dependências externas obrigatórias.

## 4. Arquitetura

A aplicação está separada em apresentação (CLI), aplicação (services), domínio (entidades/regras) e persistência (conexão/repositórios). `main.py` inicializa a aplicação e `montagem.py` conecta os repositórios aos serviços.

## 5. Funcionalidades

A versão 0.1.0 contém os quinze requisitos funcionais descritos em `../requisitos/README.md`, abrangendo cadastros, turmas, matrículas, notas, faltas, boletim e relatórios.

## 6. Regras acadêmicas

A matrícula verifica compatibilidade entre curso do aluno e curso da disciplina, disponibilidade de vaga e duplicidade ativa. As notas variam de 0 a 10, as faltas são limitadas à carga horária, a frequência mínima padrão é 75%, a média de aprovação padrão é 7,0 e a faixa de recuperação começa em 4,0.

## 7. Testes

Foram executados os testes com `python -m unittest discover -s tests -t . -v`. 66 testes foram aprovados (`OK`). O resultado deve ser repetido no commit final que será entregue e acompanhado da saída/captura do terminal.

## 8. Gerenciamento e Git

O README descreve `main`, `develop`, `feature/*` e `fix/*`, além de commits com prefixos como `feat:`, `fix:`, `docs:`, `test:`, `refactor:` e `chore:`. O ZIP analisado não contém `.git`; anexar links ou capturas do repositório remoto para comprovar commits, PRs, revisões e tags efetivamente realizados.

## 9. Limitações

A versão 0.1.0 não possui API REST, login, controle de perfis, interface gráfica, integração externa, pagamentos ou notificações.

