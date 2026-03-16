param(
    [string]$MetabaseDbName = "metabase",
    [string]$MetabaseDbUser = "metabase",
    [string]$MetabaseDbPass = "metabase_local_change_me"
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location -LiteralPath $projectRoot

$sqlFile = Join-Path $projectRoot "database\sql\provision_metabase_metadata.sql"
if (-not (Test-Path -LiteralPath $sqlFile)) {
    throw "Arquivo SQL de provisionamento nao encontrado: $sqlFile"
}

Get-Content -LiteralPath $sqlFile -Raw | docker compose exec -T postgres psql -U postgres -d postgres `
    -v METABASE_DB_NAME="$MetabaseDbName" `
    -v METABASE_DB_USER="$MetabaseDbUser" `
    -v METABASE_DB_PASS="$MetabaseDbPass" `
    -f -

if ($LASTEXITCODE -ne 0) {
    throw "Falha ao provisionar banco de metadata do Metabase."
}

Write-Output "Provisionamento do metadata DB do Metabase concluido."
Write-Output "Database: $MetabaseDbName"
Write-Output "User: $MetabaseDbUser"
