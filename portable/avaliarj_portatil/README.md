# AvaliaRJ Portatil

Pacote minimo para gerar analise em Excel, dashboard HTML e apresentacao PowerPoint sem depender do restante do repositorio.

## O que tem aqui

- `scripts/`: motores Python da analise
- `dados_auxiliares/`: legenda das habilidades do AlfabetizaRJ
- `docs/`: documentacao tecnica para manutencao da dashboard
- `entrada/`: pasta sugerida para colocar os arquivos `.xls`, `.xlsx` ou `.csv`
- `saida/`: pasta onde os arquivos gerados vao aparecer
- `instalar_ambiente.ps1`: prepara um ambiente Python local
- `gerar_excel.ps1`: gera o workbook analitico
- `gerar_dashboard.ps1`: gera dashboard HTML e PowerPoint

## Documentacao tecnica

Antes de alterar o HTML ou os scripts, consulte:

- `docs/GUIA_TECNICO_DASHBOARD.md`: arquitetura, fluxo de dados e pontos de alteracao.
- `docs/DECISOES_TECNICAS_E_BACKLOG.md`: o que ja foi decidido e o que ainda pode ser feito.
- `docs/CHECKLIST_PARA_DEVS_E_AGENTS.md`: checklist para devs e agents antes/depois de alterar.

## Requisitos

- Windows com PowerShell
- Python 3.11 ou superior
- Idealmente rodar `.\instalar_ambiente.ps1` antes de viajar, para deixar tudo pronto offline

## Preparacao

No PowerShell, dentro desta pasta:

```powershell
.\instalar_ambiente.ps1
```

Esse comando cria uma pasta `.venv` aqui dentro e instala as dependencias listadas em `requirements.txt`.

## Como usar

Coloque os dois arquivos da avaliacao em `entrada/` ou informe o caminho completo deles.

### Gerar dashboard HTML e PowerPoint

```powershell
.\gerar_dashboard.ps1 `
  -ArquivoEscola ".\entrada\DESEMPENHO POR ESCOLA.xls" `
  -ArquivoTurma ".\entrada\DESEMPENHO POR TURMA E ESCOLA.xls"
```

Saidas padrao:

- `saida\dashboard_avaliarj.html`
- `saida\apresentacao_avaliarj.pptx`

### Gerar analise em Excel

```powershell
.\gerar_excel.ps1 `
  -ArquivoEscola ".\entrada\DESEMPENHO POR ESCOLA.xls" `
  -ArquivoTurma ".\entrada\DESEMPENHO POR TURMA E ESCOLA.xls"
```

Saida padrao:

- `saida\analise_avaliarj.xlsx`

## Caminhos personalizados

Voce pode gravar a saida onde quiser:

```powershell
.\gerar_dashboard.ps1 `
  -ArquivoEscola "D:\dados\escola.xls" `
  -ArquivoTurma "D:\dados\turma.xls" `
  -SaidaHtml "D:\resultados\dashboard_mendes.html" `
  -SaidaPptx "D:\resultados\apresentacao_mendes.pptx"
```

```powershell
.\gerar_excel.ps1 `
  -ArquivoEscola "D:\dados\escola.xls" `
  -ArquivoTurma "D:\dados\turma.xls" `
  -Saida "D:\resultados\analise_mendes.xlsx"
```

## Uso totalmente offline

- Para apenas apresentar a dashboard, basta abrir o arquivo HTML gerado no navegador, sem internet.
- Para gerar novos arquivos offline, o ambiente Python precisa ja estar preparado nesta pasta com `.\instalar_ambiente.ps1`.

## Observacao

Este pacote trabalha com arquivos agregados por escola e por turma. Ele nao depende da base principal do projeto e nao grava microdados no repositorio.
