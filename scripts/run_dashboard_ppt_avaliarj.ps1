param(
    [Parameter(Mandatory = $true)]
    [string]$ArquivoEscola,

    [Parameter(Mandatory = $true)]
    [string]$ArquivoTurma,

    [Parameter(Mandatory = $true)]
    [string]$SaidaHtml,

    [Parameter(Mandatory = $true)]
    [string]$SaidaPptx,

    [string]$ArquivoLegenda = ".\export\generated\legenda_habilidades_alfabetizarj_2o_captura_2025.csv"
)

$ErrorActionPreference = "Stop"

python .\scripts\gerar_dashboard_ppt_avaliarj.py `
  --arquivo-escola $ArquivoEscola `
  --arquivo-turma $ArquivoTurma `
  --saida-html $SaidaHtml `
  --saida-pptx $SaidaPptx `
  --arquivo-legenda $ArquivoLegenda
