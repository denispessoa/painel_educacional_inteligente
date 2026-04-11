# Checklist para devs e agents

Use este checklist antes de alterar a dashboard HTML do pacote portátil.

## Antes de mexer

- Confirme que está trabalhando dentro de `portable/avaliarj_portatil`.
- Leia `docs/GUIA_TECNICO_DASHBOARD.md`.
- Leia `docs/DECISOES_TECNICAS_E_BACKLOG.md`.
- Não edite `saida/*.html` como fonte permanente da mudança.
- Não introduza microdados de estudantes.
- Não acople o pacote ao backend, banco de dados ou frontend principal.
- Se a alteração for pedagógica, mantenha textos em português.
- Se a alteração for de Matemática, não reaproveite descritores de Língua Portuguesa.

## Setup local

Execute uma vez:

```powershell
.\instalar_ambiente.ps1
```

Depois use:

```powershell
.\gerar_dashboard.ps1 `
  -ArquivoEscola ".\entrada\DESEMPENHO POR ESCOLA.xls" `
  -ArquivoTurma ".\entrada\DESEMPENHO POR TURMA E ESCOLA.xls"
```

Para Excel:

```powershell
.\gerar_excel.ps1 `
  -ArquivoEscola ".\entrada\DESEMPENHO POR ESCOLA.xls" `
  -ArquivoTurma ".\entrada\DESEMPENHO POR TURMA E ESCOLA.xls"
```

## Mapa rápido de alterações

- Mudar cores, cards, espaçamentos ou responsividade: edite o CSS embutido em `render_dashboard_html`.
- Mudar seções da dashboard: edite `render_dashboard_html`.
- Mudar abas de escola: edite o HTML e o script de abas em `render_dashboard_html`.
- Mudar cards de turma: edite `school_turma_card_html`.
- Mudar heatmaps: edite `heat_tile_html` e `heatmap_card_html`.
- Mudar significado dos descritores: edite `MATRIX_CODE_MEANINGS`.
- Mudar rótulo `H xx (Dxx)`: edite `build_skill_display_label`.
- Mudar nomes oficiais de escolas: edite `normalize_school_name`.
- Mudar faixas de aprendizado: edite `learning_band`.
- Mudar recomendações automáticas: procure `recommendations` em `build_context`.
- Mudar PowerPoint: edite `generate_powerpoint`.
- Mudar Excel: edite `analisar_microdados_avaliarj_excel.py`.

## Validação mínima após qualquer mudança no HTML

- Gere novamente a dashboard.
- Abra `saida/dashboard_avaliarj.html` no navegador.
- Teste as abas de escola.
- Passe o mouse ou use foco de teclado nas habilidades para verificar tooltips.
- Reduza a largura da janela para simular celular.
- Verifique se não há rolagem lateral nas seções de turmas e heatmaps.
- Confirme se o heatmap por turma aparece apenas dentro da escola.
- Confirme se o heatmap geral da rede aparece na seção de habilidades.
- Confirme se os rótulos continuam no padrão `H xx (Dxx)`.

## Validação mínima do PowerPoint

- Gere novamente a apresentação.
- Abra `saida/apresentacao_avaliarj.pptx`.
- Confirme se os slides abrem sem aviso de corrupção.
- Confirme se os números principais batem com a dashboard.

## Validação mínima do Excel

- Gere novamente o workbook.
- Abra `saida/analise_avaliarj.xlsx`.
- Confirme se as abas principais existem.
- Confirme se não há aviso de corrupção.

## Quando atualizar a documentação

Atualize os docs se a mudança:

- alterar o escopo pedagógico;
- adicionar Matemática;
- adicionar novo tipo de arquivo de entrada;
- mudar o padrão visual principal;
- mudar o fluxo de geração;
- adicionar dependência externa;
- mudar como publicar online;
- mudar regras de ranking ou interpretação.

## O que evitar

- CDN, fontes externas ou scripts externos sem necessidade explícita.
- Dados individualizados de estudantes.
- Caminhos absolutos fixos no código.
- Mudar os arquivos gerados sem mudar o gerador.
- Misturar melhorias do pacote portátil com alterações da plataforma principal.
- Apagar artefatos ou docs não relacionados.
