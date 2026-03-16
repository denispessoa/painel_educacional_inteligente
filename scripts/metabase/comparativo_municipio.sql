SELECT
  municipio_nome,
  municipio_estado,
  ROUND(AVG(percentual_leitura), 2) AS media_leitura,
  ROUND(AVG(percentual_escrita), 2) AS media_escrita,
  ROUND(AVG(ima), 2) AS ima_medio,
  SUM(total_alunos) AS total_alunos,
  COUNT(*) AS qtd_registros
FROM vw_ima
WHERE 1=1
[[AND ano = {{ano}}]]
[[AND trimestre = {{trimestre}}]]
[[AND municipio_nome = {{municipio_nome}}]]
GROUP BY municipio_nome, municipio_estado
ORDER BY municipio_nome;
