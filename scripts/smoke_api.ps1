[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$normalizedBaseUrl = $BaseUrl.TrimEnd("/")

function Invoke-Check {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [scriptblock]$Validator
    )

    $uri = "$normalizedBaseUrl$Path"
    $response = Invoke-WebRequest -Uri $uri -TimeoutSec 15

    if ($response.StatusCode -ne 200) {
        throw ("Status inesperado em {0}: {1}" -f $Path, $response.StatusCode)
    }

    $payload = $null
    if ($response.Content) {
        $payload = $response.Content | ConvertFrom-Json
    }

    & $Validator $payload
    Write-Host ("[ok] {0}" -f $Path)
}

Invoke-Check -Path "/health" -Validator {
    param($payload)
    if ($payload.status -ne "ok") {
        throw "Payload invalido em /health"
    }
}

Invoke-Check -Path "/health/dependencies" -Validator {
    param($payload)
    if ($payload.status -ne "ok" -or $payload.dependencies.database -ne "ok") {
        throw "Payload invalido em /health/dependencies"
    }
}

Invoke-Check -Path "/metrics" -Validator {
    param($payload)
    if ($null -eq $payload.requests_total -or $null -eq $payload.avg_latency_ms) {
        throw "Payload invalido em /metrics"
    }
}

Invoke-Check -Path "/analytics/ima?group_by=municipio" -Validator {
    param($payload)
    if ($null -eq $payload.filtros -or $null -eq $payload.resumo -or $null -eq $payload.itens) {
        throw "Payload invalido em /analytics/ima"
    }
}

Invoke-Check -Path "/bi/v1/ima?group_by=municipio" -Validator {
    param($payload)
    if ($payload.group_by -ne "municipio") {
        throw "Payload invalido em /bi/v1/ima"
    }
}

Invoke-Check -Path "/bi/v1/hierarquia" -Validator {
    param($payload)
    if (-not ($payload -is [System.Array])) {
        throw "Payload invalido em /bi/v1/hierarquia"
    }
}

Write-Host "Smoke test da API concluido com sucesso."
