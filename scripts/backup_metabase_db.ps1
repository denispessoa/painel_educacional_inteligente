param(
    [string]$OutputFile,
    [string]$MetabaseDbName = "metabase"
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location -LiteralPath $projectRoot

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
if ([string]::IsNullOrWhiteSpace($OutputFile)) {
    $OutputFile = Join-Path $projectRoot ("export\\metabase_backup_{0}.sql" -f $timestamp)
}

$outputDir = Split-Path -Parent $OutputFile
if (-not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$outputQuoted = '"' + $OutputFile + '"'
$cmd = "docker compose exec -T postgres pg_dump -U postgres -d $MetabaseDbName --no-owner --no-privileges > $outputQuoted"

cmd.exe /c $cmd
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao gerar backup do metadata DB do Metabase."
}

Write-Output ("Backup do Metabase concluido: {0}" -f $OutputFile)
