# Manual técnico

## Ambiente necessário

- Python 3.10 ou superior.
- Git para clonar e versionar o repositório.
- SQLite por meio do módulo `sqlite3` da biblioteca padrão.
- Não há dependência externa obrigatória no `requirements.txt`. O projeto utiliza também `unittest` para testes.

## Instalação

```bash
git clone <https://github.com/wandersonluiz-Dev/sistema-academico>
cd sistema-academico
```

## Configuração do banco

Por padrão, `config/settings.py` define `database/academico.db` como arquivo de banco. A variável de ambiente `SISTEMA_ACADEMICO_DB` pode indicar outro caminho.

PowerShell:

```powershell
$env:SISTEMA_ACADEMICO_DB="C:\caminho\outro.db"
python main.py
```

Linux/macOS:

```bash
export SISTEMA_ACADEMICO_DB=/caminho/outro.db
python main.py
```

`abrir_conexao()` cria a pasta pai do arquivo, configura `sqlite3.Row` e ativa as chaves estrangeiras.

## Executar a aplicação

Na raiz do projeto:

```bash
python main.py
```

O `main.py` abre a conexão, inicializa o esquema e executa a CLI.

## Dados de demonstração

```bash
python scripts/popular_dados.py
```

O script cadastra um curso ADS, duas disciplinas, um professor, dois alunos, duas turmas, matrículas e algumas notas/faltas. Ele utiliza o mesmo banco configurado pelo sistema. **Execute em banco novo ou faça backup antes:** o script cadastra novamente os registros e pode encontrar duplicidades se for executado repetidamente no mesmo banco.

## Executar testes

```bash
python -m unittest discover -s tests -t . -v
```

Ou, em ambiente com Bash:

```bash
bash scripts/executar_testes.sh
```

Na cópia do projeto examinada para esta documentação, o comando executou 66 testes e terminou com `OK`.

## Componentes principais

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada. |
| `config/settings.py` | Caminho do banco. |
| `database/schema.sql` | Definição das tabelas e restrições. |
| `dominio/` | Entidades, estratégias de média, critérios e exceções. |
| `aplicacao/` | Serviços que coordenam operações. |
| `persistencia/` | Conexão, SQL e repositórios. |
| `apresentacao/cli.py` | Menus e entrada/saída de terminal. |
| `montagem.py` | Criação e injeção dos repositórios nos serviços. |

