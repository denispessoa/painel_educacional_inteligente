# Metabase - Checklist de Validacao e Paridade

Use este checklist para validar a migracao em paralelo (Metabase x SQL do banco).

## 1) Infraestrutura
- [ ] `docker compose ps` mostra `postgres` e `metabase` em `running`.
- [ ] `http://127.0.0.1:3000` abre sem erro.
- [ ] Banco `educacao` esta conectado no Metabase.
- [ ] Tabela/view `vw_ima` esta visivel no Metabase.

## 2) Baseline SQL (fonte de verdade)
Executar no terminal e guardar resultados de referencia:

```powershell
@'
SELECT
  COUNT(*) AS qtd_linhas,
  SUM(total_alunos) AS total_alunos,
  ROUND(AVG(percentual_leitura), 2) AS media_leitura,
  ROUND(AVG(percentual_escrita), 2) AS media_escrita,
  ROUND(AVG(ima), 2) AS ima_medio
FROM vw_ima;

SELECT
  ano,
  trimestre,
  COUNT(*) AS qtd_linhas,
  SUM(total_alunos) AS total_alunos,
  ROUND(AVG(percentual_leitura), 2) AS media_leitura,
  ROUND(AVG(percentual_escrita), 2) AS media_escrita,
  ROUND(AVG(ima), 2) AS ima_medio
FROM vw_ima
GROUP BY ano, trimestre
ORDER BY ano, trimestre;

SELECT
  municipio_nome,
  COUNT(*) AS qtd_linhas,
  SUM(total_alunos) AS total_alunos,
  ROUND(AVG(percentual_leitura), 2) AS media_leitura,
  ROUND(AVG(percentual_escrita), 2) AS media_escrita,
  ROUND(AVG(ima), 2) AS ima_medio
FROM vw_ima
GROUP BY municipio_nome
ORDER BY municipio_nome;
'@ | docker compose exec -T postgres psql -U postgres -d educacao
```

## 3) Paridade de KPIs no Metabase
No dashboard `MVP - Alfabetizacao e IMA`, validar:
- [ ] `Qtd Linhas` bate com SQL.
- [ ] `Total Alunos` bate com SQL.
- [ ] `Media Leitura` bate com SQL.
- [ ] `Media Escrita` bate com SQL.
- [ ] `IMA Medio` bate com SQL.

## 4) Cenarios obrigatorios
- [ ] Sem filtros (visao global).
- [ ] Filtro `ano=2026, trimestre=1`.
- [ ] Filtro `ano=2026, trimestre=2` (se houver dados no banco).
- [ ] Filtro por municipio especifico (ex.: `Cidade BI`, se existir).

## 5) Filtros e interacao
- [ ] Filtro `ano` altera todos os cards/graficos corretamente.
- [ ] Filtro `trimestre` altera todos os cards/graficos corretamente.
- [ ] Filtro `municipio_nome` altera todos os cards/graficos corretamente.
- [ ] Limpar filtros retorna os totais globais.

## 6) Estabilidade
- [ ] Fechar e reabrir Metabase sem perder configuracoes.
- [ ] Reexecutar dashboard sem erro de conexao.
- [ ] Reboot do container `metabase` mantem funcionamento.

## 7) Gate para cutover
- [ ] Checklist 100% concluido.
- [ ] Operacao paralela validada por pelo menos 1 ciclo de uso.
- [ ] Rollback para Power BI documentado e testado.
