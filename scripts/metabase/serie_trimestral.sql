SELECT
  ano,
  trimestre,
  CONCAT(ano, ' T', trimestre) AS periodo,
  ROUND(AVG(percentual_leitura), 2) AS media_leitura,
  ROUND(AVG(percentual_escrita), 2) AS media_escrita,
  ROUND(AVG(ima), 2) AS ima_medio,
  SUM(total_alunos) AS total_alunos
FROM vw_ima
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND municipio_nome = {{municipio_nome}}]]
GROUP BY ano, trimestre
ORDER BY ano, trimestre;
