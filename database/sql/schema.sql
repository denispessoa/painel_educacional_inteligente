
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS municipios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(150) NOT NULL CHECK (char_length(trim(nome)) > 0),
    estado CHAR(2) NOT NULL CHECK (char_length(estado) = 2 AND estado = upper(estado))
);

CREATE TABLE IF NOT EXISTS escolas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    municipio_id UUID NOT NULL REFERENCES municipios(id) ON DELETE RESTRICT,
    nome VARCHAR(200) NOT NULL CHECK (char_length(trim(nome)) > 0)
);

CREATE TABLE IF NOT EXISTS turmas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    escola_id UUID NOT NULL REFERENCES escolas(id) ON DELETE RESTRICT,
    nome VARCHAR(50) NOT NULL CHECK (char_length(trim(nome)) > 0)
);

CREATE TABLE IF NOT EXISTS indicadores_trimestrais (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    turma_id UUID NOT NULL REFERENCES turmas(id) ON DELETE RESTRICT,
    ano SMALLINT NOT NULL CHECK (ano >= 2000 AND ano <= 2100),
    trimestre SMALLINT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    total_alunos INTEGER NOT NULL CHECK (total_alunos >= 0),
    alfabetizados_leitura INTEGER NOT NULL CHECK (
        alfabetizados_leitura >= 0 AND alfabetizados_leitura <= total_alunos
    ),
    alfabetizados_escrita INTEGER NOT NULL CHECK (
        alfabetizados_escrita >= 0 AND alfabetizados_escrita <= total_alunos
    ),
    percentual_leitura NUMERIC(5,2) NOT NULL CHECK (
        percentual_leitura >= 0 AND percentual_leitura <= 100
    ),
    percentual_escrita NUMERIC(5,2) NOT NULL CHECK (
        percentual_escrita >= 0 AND percentual_escrita <= 100
    ),
    UNIQUE (turma_id, ano, trimestre)
);

CREATE INDEX IF NOT EXISTS idx_escolas_municipio_id ON escolas(municipio_id);
CREATE INDEX IF NOT EXISTS idx_turmas_escola_id ON turmas(escola_id);
CREATE INDEX IF NOT EXISTS idx_indicadores_turma_id ON indicadores_trimestrais(turma_id);
CREATE INDEX IF NOT EXISTS idx_indicadores_ano_trimestre ON indicadores_trimestrais(ano, trimestre);
CREATE INDEX IF NOT EXISTS idx_indicadores_turma_ano_trimestre ON indicadores_trimestrais(turma_id, ano, trimestre);
