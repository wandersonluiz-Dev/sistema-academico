# Arquitetura do Sistema

## 1. Visão geral

O Sistema Acadêmico 0.1.0 é uma aplicação executada no terminal, escrita em Python 3.10 ou superior, com persistência em SQLite. Não possui API REST, interface web ou autenticação/login.

A arquitetura separa a interface, os serviços de aplicação, as entidades/regras do domínio e o acesso ao banco. Essa separação pode ser observada nos pacotes `apresentacao`, `aplicacao`, `dominio` e `persistencia`.

## 2. Camadas e responsabilidades

| Camada | Localização | Responsabilidade observada no código |
|---|---|---|
| Apresentação | `src/sistema_academico/apresentacao/cli.py` | Exibe menus numerados, lê entradas, chama serviços e apresenta mensagens. |
| Aplicação | `src/sistema_academico/aplicacao/` | Coordena os casos de uso de cursos, pessoas, turmas, matrículas, notas, faltas e consultas. |
| Domínio | `src/sistema_academico/dominio/` | Define entidades, validações e regras acadêmicas. |
| Persistência | `src/sistema_academico/persistencia/` | Abre a conexão, executa SQL e mapeia linhas do SQLite para objetos do domínio. |
| Banco | `database/schema.sql` | Define tabelas, chaves estrangeiras, unicidade e restrições de valores. |

O arquivo `montagem.py` cria os repositórios e injeta esses objetos nos serviços. `main.py` abre a conexão, inicializa o esquema e inicia a CLI.

## 3. Organização real do projeto

```text
sistema-academico/
├── config/
│   └── settings.py
├── database/
│   └── schema.sql
├── docs/
├── scripts/
│   ├── executar_testes.sh
│   ├── popular_dados.py
│   └── setup_git.sh
├── src/sistema_academico/
│   ├── apresentacao/cli.py
│   ├── aplicacao/
│   │   ├── curso_service.py
│   │   ├── pessoa_service.py
│   │   ├── turma_service.py
│   │   └── matricula_service.py
│   ├── dominio/
│   │   ├── pessoa.py
│   │   ├── curso.py
│   │   ├── turma.py
│   │   ├── matricula.py
│   │   ├── avaliacao.py
│   │   └── excecoes.py
│   ├── persistencia/
│   │   ├── conexao.py
│   │   ├── base.py
│   │   ├── pessoa_repository.py
│   │   ├── curso_repository.py
│   │   ├── turma_repository.py
│   │   └── matricula_repository.py
│   └── montagem.py
├── tests/
├── main.py
├── requirements.txt
├── README.md
└── CHANGELOG.md
```

## 4. Orientação a objetos no código

- **Abstração:** `Pessoa` e `EstrategiaMedia` herdam de `ABC` e possuem métodos abstratos.
- **Herança:** `Aluno` e `Professor` herdam de `Pessoa`; `MediaAritmetica` e `MediaPonderada` herdam de `EstrategiaMedia`.
- **Polimorfismo:** `descricao()` possui implementação própria em `Aluno` e `Professor`; `calcular()` é implementado por cada estratégia de média.
- **Encapsulamento:** `Pessoa` usa atributos internos (`_nome`, `_email`, `_id`) com properties e validação; `Matricula.notas` devolve uma tupla, evitando alteração externa direta da lista interna.

## 5. Padrões de projeto identificados

### 5.1 Strategy — `dominio/avaliacao.py`

`EstrategiaMedia` define o contrato `calcular(notas)`. `MediaAritmetica` calcula a média simples e `MediaPonderada` considera o peso de cada nota. `obter_estrategia()` seleciona a implementação pelo texto `aritmetica` ou `ponderada`, informado na disciplina.

**Problema tratado:** disciplinas podem utilizar fórmulas diferentes. As estratégias deixam cada fórmula em uma classe própria e intercambiável.

### 5.2 Repository — `persistencia/`

Os repositórios concentram o SQL e oferecem operações como `inserir`, `buscar_por_id`, `listar` e atualizações. `RepositorioBase` compartilha a execução de SQL e converte violações de integridade do SQLite em exceções do domínio.

**Problema tratado:** evitar SQL espalhado nos serviços e manter o acesso aos dados concentrado na camada de persistência.

## 6. Princípios de organização observáveis

- **Separação de responsabilidades:** menus, serviços, domínio e persistência estão em módulos distintos.
- **Coesão:** cada serviço reúne casos de uso de uma área (cursos, pessoas, turmas ou matrículas).
- **Baixo acoplamento em relação ao banco:** os serviços recebem repositórios e não executam SQL diretamente.
- **DRY:** operações comuns de persistência estão concentradas em `RepositorioBase`.
- **KISS:** a solução é uma aplicação única com SQLite; não foram introduzidos serviços distribuídos nem infraestrutura de API.

Essas são características identificadas no código; não significam que exista uma auditoria formal de conformidade integral com todos os princípios SOLID.

