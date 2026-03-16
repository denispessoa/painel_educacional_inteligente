-- Qtd Linhas
SELECT COUNT(*) AS qtd_linhas
FROM vw_desempenho_componentes
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND ano_escolar = {{ano_escolar}}]]
[[AND fonte_avaliacao = {{fonte_avaliacao}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- Total Alunos
SELECT SUM(total_alunos) AS total_alunos
FROM vw_desempenho_componentes
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND ano_escolar = {{ano_escolar}}]]
[[AND fonte_avaliacao = {{fonte_avaliacao}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- Percentual no Esperado - Leitura
SELECT ROUND(AVG(percentual_leitura), 2) AS percentual_leitura_no_esperado
FROM vw_desempenho_componentes
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND ano_escolar = {{ano_escolar}}]]
[[AND fonte_avaliacao = {{fonte_avaliacao}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- Percentual no Esperado - Escrita
SELECT ROUND(AVG(percentual_escrita), 2) AS percentual_escrita_no_esperado
FROM vw_desempenho_componentes
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND ano_escolar = {{ano_escolar}}]]
[[AND fonte_avaliacao = {{fonte_avaliacao}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- Percentual no Esperado - Matematica
SELECT ROUND(AVG(percentual_matematica), 2) AS percentual_matematica_no_esperado
FROM vw_desempenho_componentes
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND ano_escolar = {{ano_escolar}}]]
[[AND fonte_avaliacao = {{fonte_avaliacao}}]]
[[AND municipio_nome = {{municipio_nome}}]];
