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

INSERT INTO turmas (id, escola_id, nome)
VALUES
    ('afcf2bc0-93cf-441a-9bc9-bfdbda1832e3', 'dadb2bcf-84c5-4bdd-8212-17b2c2198d46', 'Turma BI'),
    ('8c491a07-b85c-4ef7-b36d-0206e72c804b', 'b84a2102-e21c-4bd9-8ada-15277bdc64bc', 'Turma 1ddc51bb'),
    ('a05d7ca5-ed97-487b-83e9-d221584099fc', '88402fc3-0f64-448e-a723-3999a67fd0a7', 'Turma fc31a02c')
ON CONFLICT (id) DO UPDATE
SET
    escola_id = EXCLUDED.escola_id,
    nome = EXCLUDED.nome;

WITH seed_indicadores (
    id,
    turma_id,
    ano,
    trimestre,
    total_alunos,
    alfabetizados_leitura,
    alfabetizados_escrita
) AS (
    VALUES
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1101'::uuid, '8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 2025, 1, 12, 5, 6),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1102'::uuid, '8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 2025, 2, 12, 6, 7),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1103'::uuid, '8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 2025, 3, 12, 7, 8),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1104'::uuid, '8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 2025, 4, 12, 8, 9),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1201'::uuid, 'afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 2025, 1, 20, 10, 9),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1202'::uuid, 'afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 2025, 2, 20, 11, 10),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1203'::uuid, 'afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 2025, 3, 20, 12, 11),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1204'::uuid, 'afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 2025, 4, 20, 13, 12),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1301'::uuid, 'a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, 2025, 1, 18, 7, 8),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1302'::uuid, 'a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, 2025, 2, 18, 8, 8),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1303'::uuid, 'a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, 2025, 3, 18, 8, 9),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f1304'::uuid, 'a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, 2025, 4, 18, 9, 9),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f2101'::uuid, '8c491a07-b85c-4ef7-b36d-0206e72c804b'::uuid, 2026, 1, 10, 6, 8),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f2201'::uuid, 'afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 2026, 1, 20, 12, 10),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f2202'::uuid, 'afcf2bc0-93cf-441a-9bc9-bfdbda1832e3'::uuid, 2026, 2, 20, 14, 12),
        ('5a0a7f8d-35f8-4baf-a9ea-1f6ca07f2301'::uuid, 'a05d7ca5-ed97-487b-83e9-d221584099fc'::uuid, 2026, 1, 20, 8, 10)
)
INSERT INTO indicadores_trimestrais (
    id,
    turma_id,
    ano,
    trimestre,
    total_alunos,
    alfabetizados_leitura,
    alfabetizados_escrita,
    percentual_leitura,
    percentual_escrita
)
SELECT
    id,
    turma_id,
    ano,
    trimestre,
    total_alunos,
    alfabetizados_leitura,
    alfabetizados_escrita,
    ROUND(
        CASE
            WHEN total_alunos = 0 THEN 0
            ELSE (alfabetizados_leitura::numeric / total_alunos::numeric) * 100
        END,
        2
    ) AS percentual_leitura,
    ROUND(
        CASE
            WHEN total_alunos = 0 THEN 0
            ELSE (alfabetizados_escrita::numeric / total_alunos::numeric) * 100
        END,
        2
    ) AS percentual_escrita
FROM seed_indicadores
ON CONFLICT (turma_id, ano, trimestre) DO UPDATE
SET
    total_alunos = EXCLUDED.total_alunos,
    alfabetizados_leitura = EXCLUDED.alfabetizados_leitura,
    alfabetizados_escrita = EXCLUDED.alfabetizados_escrita,
    percentual_leitura = EXCLUDED.percentual_leitura,
    percentual_escrita = EXCLUDED.percentual_escrita;
