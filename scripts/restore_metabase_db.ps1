param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile,
    [string]$MetabaseDbName = "metabase"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $InputFile)) {
    throw ("Arquivo de backup nao encontrado: {0}" -f $InputFile)
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location -LiteralPath $projectRoot

$inputQuoted = '"' + (Resolve-Path -LiteralPath $InputFile).Path + '"'
$cmd = "docker compose exec -T postgres psql -U postgres -d $MetabaseDbName < $inputQuoted"

cmd.exe /c $cmd
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao restaurar backup do metadata DB do Metabase."
}

Write-Output "Restore do Metabase concluido."
