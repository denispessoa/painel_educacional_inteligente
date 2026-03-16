
CREATE OR REPLACE VIEW vw_ima AS
SELECT
    it.id AS indicador_id,
    it.ano,
    it.trimestre,
    it.turma_id,
    t.nome AS turma_nome,
    e.id AS escola_id,
    e.nome AS escola_nome,
    m.id AS municipio_id,
    m.nome AS municipio_nome,
    m.estado AS municipio_estado,
    it.total_alunos,
    it.alfabetizados_leitura,
    it.alfabetizados_escrita,
    it.percentual_leitura,
    it.percentual_escrita,
    ROUND(((it.percentual_leitura + it.percentual_escrita) / 2.0)::numeric, 2) AS ima
FROM indicadores_trimestrais it
JOIN turmas t ON t.id = it.turma_id
JOIN escolas e ON e.id = t.escola_id
JOIN municipios m ON m.id = e.municipio_id;
