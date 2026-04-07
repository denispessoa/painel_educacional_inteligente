param(
    [Parameter(Mandatory = $true)]
    [string]$ArquivoEscola,

    [Parameter(Mandatory = $true)]
    [string]$ArquivoTurma,

    [Parameter(Mandatory = $true)]
    [string]$Saida,

    [string]$ArquivoLegenda = ".\export\generated\legenda_habilidades_alfabetizarj_2o_captura_2025.csv"
)

$ErrorActionPreference = "Stop"

python .\scripts\analisar_microdados_avaliarj_excel.py `
  --arquivo-escola $ArquivoEscola `
  --arquivo-turma $ArquivoTurma `
  --saida $Saida `
  --arquivo-legenda $ArquivoLegenda
