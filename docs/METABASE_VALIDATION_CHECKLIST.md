# Metabase - Checklist de Validacao e Paridade

Use este checklist para validar o dashboard principal no Metabase contra o SQL do banco.

## 1) Infraestrutura
- [ ] `docker compose ps` mostra `postgres` e `metabase` em `running`.
- [ ] `http://127.0.0.1:3000` abre sem erro.
- [ ] Banco `educacao` esta conectado no Metabase.
- [ ] View `vw_desempenho_componentes` esta visivel no Metabase.

## 2) Baseline SQL (fonte de verdade)
```powershell
docker compose exec -T postgres psql -U postgres -d educacao -c "SELECT COUNT(*) AS qtd_linhas, SUM(total_alunos) AS total_alunos, ROUND(AVG(percentual_leitura), 2) AS leitura_media, ROUND(AVG(percentual_escrita), 2) AS escrita_media, ROUND(AVG(percentual_matematica), 2) AS matematica_media FROM vw_desempenho_componentes;"
docker compose exec -T postgres psql -U postgres -d educacao -c "SELECT ano, trimestre, COUNT(*) AS qtd_linhas, SUM(total_alunos) AS total_alunos, ROUND(AVG(percentual_leitura), 2) AS leitura_media, ROUND(AVG(percentual_escrita), 2) AS escrita_media, ROUND(AVG(percentual_matematica), 2) AS matematica_media FROM vw_desempenho_componentes GROUP BY ano, trimestre ORDER BY ano, trimestre;"
docker compose exec -T postgres psql -U postgres -d educacao -c "SELECT fonte_avaliacao, MIN(ano_escolar) AS min_serie, MAX(ano_escolar) AS max_serie, COUNT(*) AS qtd_linhas FROM vw_desempenho_componentes GROUP BY fonte_avaliacao ORDER BY fonte_avaliacao;"
```

## 3) Paridade de KPIs
No dashboard `MVP - Desempenho por Componentes`, validar:
- [ ] `Qtd Linhas` bate com SQL.
- [ ] `Total Alunos` bate com SQL.
- [ ] `Percentual no Esperado - Leitura` bate com SQL.
- [ ] `Percentual no Esperado - Escrita` bate com SQL.
- [ ] `Percentual no Esperado - Matematica` bate com SQL.

## 4) Cenarios obrigatorios
- [ ] Sem filtros.
- [ ] `ano=2025`.
- [ ] `ano=2026`.
- [ ] `ano=2026, trimestre=4`.
- [ ] `fonte_avaliacao=cnca`.
- [ ] `fonte_avaliacao=mec_anos_finais_bncc`.
- [ ] `ano_escolar=1`.
- [ ] `ano_escolar=9`.
- [ ] `municipio_nome=Cidade BI`.

## 5) Filtros e interacao
- [ ] `ano` altera todos os cards.
- [ ] `trimestre` altera todos os cards.
- [ ] `ano_escolar` altera todos os cards.
- [ ] `fonte_avaliacao` altera todos os cards.
- [ ] `municipio_nome` altera todos os cards.
- [ ] limpar filtros retorna ao total global.

## 6) Legado
- [ ] `vw_ima` ainda esta disponivel para comparacao.
- [ ] o dashboard principal nao depende de `IMA` como metrica central.

## 7) Estabilidade
- [ ] fechar e reabrir Metabase sem perder configuracoes.
- [ ] reiniciar `metabase` sem erro de conexao.
- [ ] reexecutar dashboard sem falhas.
