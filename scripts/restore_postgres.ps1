param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $InputFile)) {
    throw ("Arquivo de backup nao encontrado: {0}" -f $InputFile)
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location -LiteralPath $projectRoot

$inputQuoted = '"' + (Resolve-Path -LiteralPath $InputFile).Path + '"'
$cmd = "docker compose exec -T postgres psql -U postgres -d educacao < $inputQuoted"

cmd.exe /c $cmd
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao restaurar backup no banco."
}

Write-Output "Restore concluido."
