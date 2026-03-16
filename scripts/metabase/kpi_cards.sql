-- Qtd Linhas
SELECT COUNT(*) AS qtd_linhas
FROM vw_ima
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- Total Alunos
SELECT SUM(total_alunos) AS total_alunos
FROM vw_ima
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- Media Leitura
SELECT ROUND(AVG(percentual_leitura), 2) AS media_leitura
FROM vw_ima
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- Media Escrita
SELECT ROUND(AVG(percentual_escrita), 2) AS media_escrita
FROM vw_ima
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND municipio_nome = {{municipio_nome}}]];

-- IMA Medio
SELECT ROUND(AVG(ima), 2) AS ima_medio
FROM vw_ima
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND municipio_nome = {{municipio_nome}}]];
