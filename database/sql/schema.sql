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
    ano_escolar SMALLINT NOT NULL CHECK (ano_escolar BETWEEN 1 AND 9),
    fonte_avaliacao VARCHAR(32) NOT NULL CHECK (
        fonte_avaliacao IN ('cnca', 'mec_anos_finais_bncc')
    ),
    total_alunos INTEGER NOT NULL CHECK (total_alunos >= 0),
    alfabetizados_leitura INTEGER NOT NULL CHECK (
        alfabetizados_leitura >= 0 AND alfabetizados_leitura <= total_alunos
    ),
    alfabetizados_escrita INTEGER NOT NULL CHECK (
        alfabetizados_escrita >= 0 AND alfabetizados_escrita <= total_alunos
    ),
    atingiu_esperado_leitura INTEGER NOT NULL CHECK (
        atingiu_esperado_leitura >= 0 AND atingiu_esperado_leitura <= total_alunos
    ),
    atingiu_esperado_escrita INTEGER NOT NULL CHECK (
        atingiu_esperado_escrita >= 0 AND atingiu_esperado_escrita <= total_alunos
    ),
    atingiu_esperado_matematica INTEGER NOT NULL CHECK (
        atingiu_esperado_matematica >= 0 AND atingiu_esperado_matematica <= total_alunos
    ),
    percentual_leitura NUMERIC(5,2) NOT NULL CHECK (
        percentual_leitura >= 0 AND percentual_leitura <= 100
    ),
    percentual_escrita NUMERIC(5,2) NOT NULL CHECK (
        percentual_escrita >= 0 AND percentual_escrita <= 100
    ),
    percentual_matematica NUMERIC(5,2) NOT NULL CHECK (
        percentual_matematica >= 0 AND percentual_matematica <= 100
    ),
    CONSTRAINT ck_indicadores_fonte_por_ano CHECK (
        (fonte_avaliacao = 'cnca' AND ano_escolar BETWEEN 1 AND 5)
        OR (fonte_avaliacao = 'mec_anos_finais_bncc' AND ano_escolar BETWEEN 6 AND 9)
    ),
    CONSTRAINT ck_indicadores_legado_leitura CHECK (
        alfabetizados_leitura = atingiu_esperado_leitura
    ),
    CONSTRAINT ck_indicadores_legado_escrita CHECK (
        alfabetizados_escrita = atingiu_esperado_escrita
    ),
    CONSTRAINT uq_indicadores_turma_periodo_serie_fonte UNIQUE (
        turma_id,
        ano,
        trimestre,
        ano_escolar,
        fonte_avaliacao
    )
);

CREATE INDEX IF NOT EXISTS idx_escolas_municipio_id ON escolas(municipio_id);
CREATE INDEX IF NOT EXISTS idx_turmas_escola_id ON turmas(escola_id);
CREATE INDEX IF NOT EXISTS idx_indicadores_turma_id ON indicadores_trimestrais(turma_id);
CREATE INDEX IF NOT EXISTS idx_indicadores_ano_trimestre ON indicadores_trimestrais(ano, trimestre);
CREATE INDEX IF NOT EXISTS idx_indicadores_turma_ano_trimestre ON indicadores_trimestrais(turma_id, ano, trimestre);
CREATE INDEX IF NOT EXISTS idx_indicadores_ano_escolar_fonte ON indicadores_trimestrais(ano_escolar, fonte_avaliacao);
