# Guia técnico da dashboard AvaliaRJ portátil

Este documento orienta devs e agents que precisem alterar a dashboard HTML do pacote portátil `avaliarj_portatil`.

## Objetivo do pacote

O pacote gera, de forma offline e desacoplada do restante do repositório:

- uma dashboard HTML estática;
- uma apresentação PowerPoint;
- um workbook Excel analítico.

O pacote trabalha com arquivos agregados do AvaliaRJ/AlfabetizaRJ por escola e por turma. Ele não depende de banco de dados, API, frontend principal ou microdados de estudantes.

## Regra principal de manutenção

Evite editar diretamente os arquivos em `saida/`.

O HTML é gerado por `scripts/gerar_dashboard_ppt_avaliarj.py`. Se a mudança precisa ser reaproveitável, altere o gerador e regenere a saída. Edição manual em `saida/*.html` só deve ser usada para ajuste emergencial de apresentação, sabendo que será perdida na próxima geração.

## Estrutura dos arquivos

- `gerar_dashboard.ps1`: wrapper PowerShell para gerar dashboard HTML e PowerPoint.
- `gerar_excel.ps1`: wrapper PowerShell para gerar workbook Excel.
- `instalar_ambiente.ps1`: cria `.venv` local e instala dependências.
- `requirements.txt`: dependências Python mínimas.
- `scripts/analisar_microdados_avaliarj_excel.py`: leitura, limpeza, normalização, indicadores e workbook Excel.
- `scripts/gerar_dashboard_ppt_avaliarj.py`: contexto analítico, HTML, CSS, JavaScript mínimo e PowerPoint.
- `dados_auxiliares/legenda_habilidades_alfabetizarj_2o_captura_2025.csv`: legenda/crosswalk de habilidades.
- `entrada/`: pasta sugerida para arquivos `.xls`, `.xlsx` ou `.csv`.
- `saida/`: artefatos gerados.

## Fluxo de dados

1. `read_input` lê `.xls`, `.xlsx` ou `.csv`.
2. `repair_text` corrige problemas comuns de codificação dos arquivos de origem.
3. `infer_component` identifica o componente curricular.
4. `load_legend` carrega a legenda de habilidades.
5. `prepare_base` normaliza percentuais, indicadores e colunas de habilidade.
6. `build_ranked_reports` calcula rankings por escola e turma.
7. `build_skill_summary` consolida habilidades da rede, das escolas e das turmas.
8. `build_context` cria o dicionário usado por HTML e PowerPoint.
9. `render_dashboard_html` gera o HTML completo, incluindo CSS e JS embutidos.
10. `generate_powerpoint` gera a apresentação `.pptx`.

## Entrada esperada

O pacote espera dois arquivos agregados:

- arquivo por escola;
- arquivo por turma e escola.

Colunas importantes:

- `Avaliação`
- `Rede`
- `Ano Escolar`
- `Componente Curricular`
- `Município`
- `Escola`
- `Turma`, no arquivo por turma
- `Previstos`
- `Avaliados`
- `Participação(%)`
- `Proficiência Média`
- `Abaixo do básico`
- `Básico`
- `Adequado`
- `Avançado`
- colunas no padrão `H 01 (%)`, `H 02 (%)`, etc.

Os percentuais podem vir como razão, por exemplo `0,85`, ou como percentual, por exemplo `85`. O script tenta normalizar automaticamente.

## Saída esperada

Com `gerar_dashboard.ps1`, as saídas padrão são:

- `saida/dashboard_avaliarj.html`
- `saida/apresentacao_avaliarj.pptx`

Com `gerar_excel.ps1`, a saída padrão é:

- `saida/analise_avaliarj.xlsx`

## Onde alterar cada tipo de coisa

- Significado dos descritores: altere `MATRIX_CODE_MEANINGS` em `gerar_dashboard_ppt_avaliarj.py`.
- Rótulo exibido das habilidades: altere `build_skill_display_label`.
- Texto do tooltip: altere `build_skill_meaning` ou os dados em `MATRIX_CODE_MEANINGS`.
- Padronização de nomes de escolas: altere `normalize_school_name`.
- Faixas interpretativas de aprendizado: altere `learning_band`.
- Cores dos heatmaps: altere `heat_color` e `heat_text_color`.
- Estrutura da dashboard: altere `render_dashboard_html`.
- Cards de turma: altere `school_turma_card_html`.
- Heatmap em cartões: altere `heat_tile_html` e `heatmap_card_html`.
- CSS visual: altere o bloco `<style>` dentro de `render_dashboard_html`.
- Interação das abas de escola: altere o bloco `<script>` dentro de `render_dashboard_html`.
- Apresentação PowerPoint: altere `generate_powerpoint` e funções auxiliares como `draw_school_learning_panel`.
- Workbook Excel: altere `analisar_microdados_avaliarj_excel.py`.

## Modelo visual atual

A dashboard HTML contém:

- cabeçalho executivo com indicadores da rede;
- navegação interna;
- panorama da rede;
- seção de escolas em abas;
- dentro de cada escola: perfil, distribuição, habilidades frágeis/fortes, análise das turmas da escola e heatmap das turmas;
- seção de habilidades da rede com heatmap geral municipal;
- encaminhamentos sugeridos.

As leituras por turma ficam no contexto da escola selecionada. A página principal não mostra heatmap por turma para evitar excesso de largura e perda de foco executivo.

## Interação atual

- Habilidades aparecem como `H xx (Dxx)`.
- O significado pedagógico do descritor aparece apenas no hover/foco do mouse.
- As escolas são separadas por abas.
- Os heatmaps são cartões responsivos, não tabelas largas.
- Os cards de turma usam cor de status e destacam `Melhor da escola` e `Maior atenção` quando a escola tem mais de uma turma.

## Como validar uma alteração

Dentro da pasta `avaliarj_portatil`, execute:

```powershell
.\gerar_dashboard.ps1 `
  -ArquivoEscola ".\entrada\DESEMPENHO POR ESCOLA.xls" `
  -ArquivoTurma ".\entrada\DESEMPENHO POR TURMA E ESCOLA.xls"
```

E, se a mudança também afetar o Excel:

```powershell
.\gerar_excel.ps1 `
  -ArquivoEscola ".\entrada\DESEMPENHO POR ESCOLA.xls" `
  -ArquivoTurma ".\entrada\DESEMPENHO POR TURMA E ESCOLA.xls"
```

Depois confira:

- se `saida/dashboard_avaliarj.html` abre no navegador;
- se as abas de escola alternam corretamente;
- se os tooltips aparecem nas habilidades;
- se não existe rolagem lateral indesejada no desktop;
- se a leitura no celular continua em cards;
- se a apresentação `.pptx` abre;
- se o Excel abre sem aviso de corrupção.

## Cuidados

- Não adicionar dependência de internet ao HTML, salvo decisão explícita.
- Não gravar microdados de estudantes.
- Não adicionar dependência do backend ou do banco do projeto principal.
- Manter textos pedagógicos e documentação em português.
- Ao incluir Matemática, não reutilizar automaticamente a matriz de Língua Portuguesa.
- Ao alterar o gerador HTML, verificar se o PowerPoint também precisa refletir a mesma mudança.
