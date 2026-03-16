INSERT INTO municipios (id, nome, estado)
VALUES
    ('d973590a-b783-490c-825b-a455012462e0', 'Cidade BI', 'RJ'),
    ('cc981cc5-55f9-4712-8e02-a32e5ad5e36b', 'Cidade 1ddc51bb', 'RJ'),
    ('9dd05474-8aa1-46a8-b1e1-c1b24cc26b20', 'Cidade fc31a02c', 'RJ')
ON CONFLICT (id) DO UPDATE
SET
    nome = EXCLUDED.nome,
    estado = EXCLUDED.estado;

INSERT INTO escolas (id, municipio_id, nome)
VALUES
    ('dadb2bcf-84c5-4bdd-8212-17b2c2198d46', 'd973590a-b783-490c-825b-a455012462e0', 'Escola BI'),
    ('b84a2102-e21c-4bd9-8ada-15277bdc64bc', 'cc981cc5-55f9-4712-8e02-a32e5ad5e36b', 'Escola 1ddc51bb'),
    ('88402fc3-0f64-448e-a723-3999a67fd0a7', '9dd05474-8aa1-46a8-b1e1-c1b24cc26b20', 'Escola fc31a02c')
ON CONFLICT (id) DO UPDATE
SET
    municipio_id = EXCLUDED.municipio_id,
    nome = EXCLUDED.nome;

WITH seed_turmas (id, escola_id, nome, ano_escolar, fonte_avaliacao, total_base, leitura_base, escrita_base, matematica_base) AS (
    VALUES
        ('afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 'dadb2bcf-84c5-4bdd-8212-17b2c2198d46'::uuid, '1o Ano - CNCA', 1, 'cnca', 18, 7, 6, 5),
        ('f0a3b0a1-c9c4-4a18-b9c1-111111111111'::uuid, 'dadb2bcf-84c5-4bdd-8212-17b2c2198d46'::uuid, '2o Ano - CNCA', 2, 'cnca', 19, 8, 7, 6),
        ('f0a3b0a1-c9c4-4a18-b9c1-222222222222'::uuid, 'dadb2bcf-84c5-4bdd-8212-17b2c2198d46'::uuid, '3o Ano - CNCA', 3, 'cnca', 20, 9, 8, 7),
        ('8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 'b84a2102-e21c-4bd9-8ada-15277bdc64bc'::uuid, '4o Ano - CNCA', 4, 'cnca', 21, 10, 9, 8),
        ('f0a3b0a1-c9c4-4a18-b9c1-333333333333'::uuid, 'b84a2102-e21c-4bd9-8ada-15277bdc64bc'::uuid, '5o Ano - CNCA', 5, 'cnca', 22, 11, 10, 9),
        ('f0a3b0a1-c9c4-4a18-b9c1-444444444444'::uuid, 'b84a2102-e21c-4bd9-8ada-15277bdc64bc'::uuid, '6o Ano - MEC AF', 6, 'mec_anos_finais_bncc', 23, 12, 11, 10),
        ('a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, '88402fc3-0f64-448e-a723-3999a67fd0a7'::uuid, '7o Ano - MEC AF', 7, 'mec_anos_finais_bncc', 24, 13, 12, 11),
        ('f0a3b0a1-c9c4-4a18-b9c1-555555555555'::uuid, '88402fc3-0f64-448e-a723-3999a67fd0a7'::uuid, '8o Ano - MEC AF', 8, 'mec_anos_finais_bncc', 25, 14, 13, 12),
        ('f0a3b0a1-c9c4-4a18-b9c1-666666666666'::uuid, '88402fc3-0f64-448e-a723-3999a67fd0a7'::uuid, '9o Ano - MEC AF', 9, 'mec_anos_finais_bncc', 26, 15, 14, 13)
)
INSERT INTO turmas (id, escola_id, nome)
SELECT id, escola_id, nome
FROM seed_turmas
ON CONFLICT (id) DO UPDATE
SET
    escola_id = EXCLUDED.escola_id,
    nome = EXCLUDED.nome;

WITH seed_turmas (id, ano_escolar, fonte_avaliacao) AS (
    VALUES
        ('afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 1, 'cnca'),
        ('f0a3b0a1-c9c4-4a18-b9c1-111111111111'::uuid, 2, 'cnca'),
        ('f0a3b0a1-c9c4-4a18-b9c1-222222222222'::uuid, 3, 'cnca'),
        ('8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 4, 'cnca'),
        ('f0a3b0a1-c9c4-4a18-b9c1-333333333333'::uuid, 5, 'cnca'),
        ('f0a3b0a1-c9c4-4a18-b9c1-444444444444'::uuid, 6, 'mec_anos_finais_bncc'),
        ('a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, 7, 'mec_anos_finais_bncc'),
        ('f0a3b0a1-c9c4-4a18-b9c1-555555555555'::uuid, 8, 'mec_anos_finais_bncc'),
        ('f0a3b0a1-c9c4-4a18-b9c1-666666666666'::uuid, 9, 'mec_anos_finais_bncc')
)
DELETE FROM indicadores_trimestrais
WHERE turma_id IN (SELECT id FROM seed_turmas);

WITH seed_turmas (id, ano_escolar, fonte_avaliacao, total_base, leitura_base, escrita_base, matematica_base) AS (
    VALUES
        ('afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 1, 'cnca', 18, 7, 6, 5),
        ('f0a3b0a1-c9c4-4a18-b9c1-111111111111'::uuid, 2, 'cnca', 19, 8, 7, 6),
        ('f0a3b0a1-c9c4-4a18-b9c1-222222222222'::uuid, 3, 'cnca', 20, 9, 8, 7),
        ('8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 4, 'cnca', 21, 10, 9, 8),
        ('f0a3b0a1-c9c4-4a18-b9c1-333333333333'::uuid, 5, 'cnca', 22, 11, 10, 9),
        ('f0a3b0a1-c9c4-4a18-b9c1-444444444444'::uuid, 6, 'mec_anos_finais_bncc', 23, 12, 11, 10),
        ('a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, 7, 'mec_anos_finais_bncc', 24, 13, 12, 11),
        ('f0a3b0a1-c9c4-4a18-b9c1-555555555555'::uuid, 8, 'mec_anos_finais_bncc', 25, 14, 13, 12),
        ('f0a3b0a1-c9c4-4a18-b9c1-666666666666'::uuid, 9, 'mec_anos_finais_bncc', 26, 15, 14, 13)
),
periodos (ano, trimestre, delta) AS (
    VALUES
        (2025, 1, 0),
        (2025, 2, 1),
        (2025, 3, 2),
        (2025, 4, 3),
        (2026, 1, 4),
        (2026, 2, 5),
        (2026, 3, 6),
        (2026, 4, 7)
)
INSERT INTO indicadores_trimestrais (
    id,
    turma_id,
    ano,
    trimestre,
    ano_escolar,
    fonte_avaliacao,
    total_alunos,
    alfabetizados_leitura,
    alfabetizados_escrita,
    atingiu_esperado_leitura,
    atingiu_esperado_escrita,
    atingiu_esperado_matematica,
    percentual_leitura,
    percentual_escrita,
    percentual_matematica
)
SELECT
    uuid_generate_v5(
        '6ba7b811-9dad-11d1-80b4-00c04fd430c8'::uuid,
        CONCAT(st.id::text, '-', p.ano, '-', p.trimestre)
    ) AS id,
    st.id AS turma_id,
    p.ano,
    p.trimestre,
    st.ano_escolar,
    st.fonte_avaliacao,
    st.total_base AS total_alunos,
    LEAST(st.total_base, st.leitura_base + p.delta) AS alfabetizados_leitura,
    LEAST(st.total_base, st.escrita_base + p.delta) AS alfabetizados_escrita,
    LEAST(st.total_base, st.leitura_base + p.delta) AS atingiu_esperado_leitura,
    LEAST(st.total_base, st.escrita_base + p.delta) AS atingiu_esperado_escrita,
    LEAST(st.total_base, st.matematica_base + p.delta) AS atingiu_esperado_matematica,
    ROUND((LEAST(st.total_base, st.leitura_base + p.delta)::numeric / st.total_base::numeric) * 100, 2) AS percentual_leitura,
    ROUND((LEAST(st.total_base, st.escrita_base + p.delta)::numeric / st.total_base::numeric) * 100, 2) AS percentual_escrita,
    ROUND((LEAST(st.total_base, st.matematica_base + p.delta)::numeric / st.total_base::numeric) * 100, 2) AS percentual_matematica
FROM seed_turmas st
CROSS JOIN periodos p
ON CONFLICT (turma_id, ano, trimestre, ano_escolar, fonte_avaliacao) DO UPDATE
SET
    total_alunos = EXCLUDED.total_alunos,
    alfabetizados_leitura = EXCLUDED.alfabetizados_leitura,
    alfabetizados_escrita = EXCLUDED.alfabetizados_escrita,
    atingiu_esperado_leitura = EXCLUDED.atingiu_esperado_leitura,
    atingiu_esperado_escrita = EXCLUDED.atingiu_esperado_escrita,
    atingiu_esperado_matematica = EXCLUDED.atingiu_esperado_matematica,
    percentual_leitura = EXCLUDED.percentual_leitura,
    percentual_escrita = EXCLUDED.percentual_escrita,
    percentual_matematica = EXCLUDED.percentual_matematica;
