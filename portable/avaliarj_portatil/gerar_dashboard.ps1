param(
    [Parameter(Mandatory = $true)]
    [string]$ArquivoEscola,

    [Parameter(Mandatory = $true)]
    [string]$ArquivoTurma,

    [string]$SaidaHtml = ".\\saida\\dashboard_avaliarj.html",

    [string]$SaidaPptx = ".\\saida\\apresentacao_avaliarj.pptx",

    [string]$ArquivoLegenda = ".\\dados_auxiliares\\legenda_habilidades_alfabetizarj_2o_captura_2025.csv"
)

$ErrorActionPreference = "Stop"

$BaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Resolve-PortablePath {
    param([string]$PathValue)

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $BaseDir $PathValue))
}

function Get-PortablePython {
    $venvPython = Join-Path $BaseDir ".venv\\Scripts\\python.exe"
    if (Test-Path $venvPython) {
        return @{
            Executable = $venvPython
            PrefixArgs = @()
        }
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return @{
            Executable = $python.Source
            PrefixArgs = @()
        }
    }

    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        return @{
            Executable = $pyLauncher.Source
            PrefixArgs = @("-3")
        }
    }

    throw "Python nao encontrado. Execute .\\instalar_ambiente.ps1 ou instale Python 3.11+."
}

$PythonCommand = Get-PortablePython
$ScriptPath = Join-Path $BaseDir "scripts\\gerar_dashboard_ppt_avaliarj.py"
$ResolvedEscola = Resolve-PortablePath $ArquivoEscola
$ResolvedTurma = Resolve-PortablePath $ArquivoTurma
$ResolvedHtml = Resolve-PortablePath $SaidaHtml
$ResolvedPptx = Resolve-PortablePath $SaidaPptx
$ResolvedLegenda = Resolve-PortablePath $ArquivoLegenda

New-Item -ItemType Directory -Force (Split-Path -Parent $ResolvedHtml) | Out-Null
New-Item -ItemType Directory -Force (Split-Path -Parent $ResolvedPptx) | Out-Null

& $PythonCommand.Executable @(
    $PythonCommand.PrefixArgs +
    @(
        $ScriptPath,
        "--arquivo-escola", $ResolvedEscola,
        "--arquivo-turma", $ResolvedTurma,
        "--saida-html", $ResolvedHtml,
        "--saida-pptx", $ResolvedPptx,
        "--arquivo-legenda", $ResolvedLegenda
    )
)

Write-Host ""
Write-Host "Dashboard gerada em: $ResolvedHtml"
Write-Host "Apresentacao gerada em: $ResolvedPptx"
