-- Esquema do banco de dados (SQLite) - Sistema Acadêmico

CREATE TABLE IF NOT EXISTS cursos (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo             TEXT    NOT NULL UNIQUE,
    nome               TEXT    NOT NULL,
    duracao_semestres  INTEGER NOT NULL CHECK (duracao_semestres > 0)
);

CREATE TABLE IF NOT EXISTS disciplinas (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo         TEXT    NOT NULL UNIQUE,
    nome           TEXT    NOT NULL,
    carga_horaria  INTEGER NOT NULL CHECK (carga_horaria > 0),
    tipo_media     TEXT    NOT NULL DEFAULT 'aritmetica'
                           CHECK (tipo_media IN ('aritmetica', 'ponderada')),
    curso_id       INTEGER NOT NULL REFERENCES cursos (id)
);

CREATE TABLE IF NOT EXISTS professores (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    titulacao  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alunos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ra        TEXT NOT NULL UNIQUE,
    nome      TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE,
    curso_id  INTEGER NOT NULL REFERENCES cursos (id)
);

CREATE TABLE IF NOT EXISTS turmas (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    disciplina_id  INTEGER NOT NULL REFERENCES disciplinas (id),
    professor_id   INTEGER NOT NULL REFERENCES professores (id),
    semestre       TEXT    NOT NULL,
    vagas          INTEGER NOT NULL CHECK (vagas > 0)
);

CREATE TABLE IF NOT EXISTS matriculas (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id  INTEGER NOT NULL REFERENCES alunos (id),
    turma_id  INTEGER NOT NULL REFERENCES turmas (id),
    faltas    INTEGER NOT NULL DEFAULT 0 CHECK (faltas >= 0),
    ativa     INTEGER NOT NULL DEFAULT 1 CHECK (ativa IN (0, 1)),
    UNIQUE (aluno_id, turma_id)
);

CREATE TABLE IF NOT EXISTS notas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula_id  INTEGER NOT NULL REFERENCES matriculas (id),
    descricao     TEXT    NOT NULL DEFAULT '',
    valor         REAL    NOT NULL CHECK (valor >= 0 AND valor <= 10),
    peso          REAL    NOT NULL DEFAULT 1 CHECK (peso > 0)
);
