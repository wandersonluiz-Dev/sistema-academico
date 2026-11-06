# Diagrama de classes do domínio

Diagrama baseado nas classes presentes em `src/sistema_academico/dominio/`. Os serviços e repositórios não foram incluídos para manter o foco nas entidades e estratégias do domínio.

```mermaid
classDiagram
  class Pessoa {
    <<abstract>>
    -_id: int
    -_nome: str
    -_email: str
    +id: int
    +nome: str
    +email: str
    +tipo: str
    +descricao()* str
  }
  class Aluno {
    -_ra: str
    -_curso_id: int
    +ra: str
    +curso_id: int
    +descricao() str
  }
  class Professor {
    -_titulacao: str
    +titulacao: str
    +descricao() str
  }
  Pessoa <|-- Aluno
  Pessoa <|-- Professor

  class Curso {
    +id: int
    +codigo: str
    +nome: str
    +duracao_semestres: int
  }
  class Disciplina {
    +id: int
    +codigo: str
    +nome: str
    +carga_horaria: int
    +curso_id: int
    +tipo_media: str
  }
  Curso "1" --> "0..*" Disciplina
  Curso "1" --> "0..*" Aluno

  class Turma {
    +id: int
    +disciplina_id: int
    +professor_id: int
    +semestre: str
    +vagas: int
    +tem_vaga(ocupadas) bool
  }
  Disciplina "1" --> "0..*" Turma
  Professor "1" --> "0..*" Turma

  class Matricula {
    +id: int
    +aluno_id: int
    +turma_id: int
    -_notas: list[Nota]
    -_faltas: int
    +notas: tuple[Nota]
    +faltas: int
    +lancar_nota(valor, peso, descricao) Nota
    +registrar_faltas(quantidade, carga_horaria) None
    +media(estrategia) float
    +frequencia(carga_horaria) float
    +cancelar() None
    +reativar() None
  }
  Aluno "1" --> "0..*" Matricula
  Turma "1" --> "0..*" Matricula

  class Nota {
    +valor: float
    +peso: float
    +descricao: str
  }
  Matricula "1" *-- "0..*" Nota

  class EstrategiaMedia {
    <<abstract>>
    +calcular(notas) float
  }
  class MediaAritmetica {
    +calcular(notas) float
  }
  class MediaPonderada {
    +calcular(notas) float
  }
  EstrategiaMedia <|-- MediaAritmetica
  EstrategiaMedia <|-- MediaPonderada
  class CriterioAprovacao {
    +media_aprovacao: float = 7.0
    +media_recuperacao: float = 4.0
    +frequencia_minima: float = 0.75
  }
```

`Nota` e `CriterioAprovacao` são dataclasses congeladas. `Pessoa` e `EstrategiaMedia` são classes abstratas. A relação de `Curso` com `Aluno` ocorre por `Aluno.curso_id`.
