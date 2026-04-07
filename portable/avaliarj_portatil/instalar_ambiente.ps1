param()

$ErrorActionPreference = "Stop"

$BaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $BaseDir ".venv"
$RequirementsFile = Join-Path $BaseDir "requirements.txt"

function Get-PythonBootstrap {
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        return @{
            Executable = $pyLauncher.Source
            PrefixArgs = @("-3")
        }
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return @{
            Executable = $python.Source
            PrefixArgs = @()
        }
    }

    throw "Python nao encontrado. Instale Python 3.11+ antes de continuar."
}

$bootstrap = Get-PythonBootstrap

if (-not (Test-Path $VenvDir)) {
    & $bootstrap.Executable @($bootstrap.PrefixArgs + @("-m", "venv", $VenvDir))
}

$VenvPython = Join-Path $VenvDir "Scripts\\python.exe"

& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r $RequirementsFile

Write-Host ""
Write-Host "Ambiente preparado em: $VenvDir"
Write-Host "Agora voce pode usar:"
Write-Host "  .\\gerar_dashboard.ps1 -ArquivoEscola <arquivo> -ArquivoTurma <arquivo>"
Write-Host "  .\\gerar_excel.ps1 -ArquivoEscola <arquivo> -ArquivoTurma <arquivo>"
