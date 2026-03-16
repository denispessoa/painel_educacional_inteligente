BEGIN;

DROP VIEW IF EXISTS vw_desempenho_componentes;
DROP VIEW IF EXISTS vw_ima;

ALTER TABLE indicadores_trimestrais
    ADD COLUMN IF NOT EXISTS ano_escolar SMALLINT,
    ADD COLUMN IF NOT EXISTS fonte_avaliacao VARCHAR(32),
    ADD COLUMN IF NOT EXISTS atingiu_esperado_leitura INTEGER,
    ADD COLUMN IF NOT EXISTS atingiu_esperado_escrita INTEGER,
    ADD COLUMN IF NOT EXISTS atingiu_esperado_matematica INTEGER,
    ADD COLUMN IF NOT EXISTS percentual_matematica NUMERIC(5,2);

UPDATE indicadores_trimestrais
SET
    ano_escolar = COALESCE(ano_escolar, 2),
    fonte_avaliacao = COALESCE(fonte_avaliacao, 'cnca'),
    atingiu_esperado_leitura = COALESCE(atingiu_esperado_leitura, alfabetizados_leitura),
    atingiu_esperado_escrita = COALESCE(atingiu_esperado_escrita, alfabetizados_escrita),
    atingiu_esperado_matematica = COALESCE(atingiu_esperado_matematica, 0),
    percentual_matematica = COALESCE(percentual_matematica, 0.00);

ALTER TABLE indicadores_trimestrais
    ALTER COLUMN ano_escolar SET NOT NULL,
    ALTER COLUMN fonte_avaliacao SET NOT NULL,
    ALTER COLUMN atingiu_esperado_leitura SET NOT NULL,
    ALTER COLUMN atingiu_esperado_escrita SET NOT NULL,
    ALTER COLUMN atingiu_esperado_matematica SET NOT NULL,
    ALTER COLUMN percentual_matematica SET NOT NULL;

ALTER TABLE indicadores_trimestrais
    DROP CONSTRAINT IF EXISTS indicadores_trimestrais_turma_id_ano_trimestre_key,
    DROP CONSTRAINT IF EXISTS uq_indicadores_turma_periodo_serie_fonte,
    DROP CONSTRAINT IF EXISTS ck_indicadores_fonte_por_ano,
    DROP CONSTRAINT IF EXISTS ck_indicadores_legado_leitura,
    DROP CONSTRAINT IF EXISTS ck_indicadores_legado_escrita;

ALTER TABLE indicadores_trimestrais
    ADD CONSTRAINT uq_indicadores_turma_periodo_serie_fonte UNIQUE (
        turma_id,
        ano,
        trimestre,
        ano_escolar,
        fonte_avaliacao
    ),
    ADD CONSTRAINT ck_indicadores_fonte_por_ano CHECK (
        (fonte_avaliacao = 'cnca' AND ano_escolar BETWEEN 1 AND 5)
        OR (fonte_avaliacao = 'mec_anos_finais_bncc' AND ano_escolar BETWEEN 6 AND 9)
    ),
    ADD CONSTRAINT ck_indicadores_legado_leitura CHECK (
        alfabetizados_leitura = atingiu_esperado_leitura
    ),
    ADD CONSTRAINT ck_indicadores_legado_escrita CHECK (
        alfabetizados_escrita = atingiu_esperado_escrita
    );

CREATE INDEX IF NOT EXISTS idx_indicadores_ano_escolar_fonte
    ON indicadores_trimestrais(ano_escolar, fonte_avaliacao);

COMMIT;
