[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Message,

    [string]$RemoteName = "origin",

    [string]$RemoteUrl,

    [string]$Branch,

    [switch]$SkipPush,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-GitCapture {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args,

        [switch]$AllowFailure
    )

    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = "git"
    $processInfo.UseShellExecute = $false
    $processInfo.RedirectStandardOutput = $true
    $processInfo.RedirectStandardError = $true
    $processInfo.Arguments = (($Args | ForEach-Object {
        if ($_ -match '[\s"]') {
            '"' + ($_ -replace '"', '\"') + '"'
        }
        else {
            $_
        }
    }) -join " ")

    $process = [System.Diagnostics.Process]::Start($processInfo)
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    $exitCode = $process.ExitCode
    $output = @($stdout, $stderr) | Where-Object { $_ -and $_.Trim() }

    if ($exitCode -ne 0 -and -not $AllowFailure) {
        throw ("Falha ao executar: git {0}`n{1}" -f ($Args -join " "), ($output -join [Environment]::NewLine))
    }

    if ($exitCode -ne 0 -and $AllowFailure) {
        return ""
    }

    return ($output -join [Environment]::NewLine).Trim()
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    if ($DryRun) {
        Write-Host ("[dry-run] git {0}" -f ($Args -join " "))
        return
    }

    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw ("Falha ao executar: git {0}" -f ($Args -join " "))
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Invoke-GitCapture -Args @("-C", $scriptDir, "rev-parse", "--show-toplevel")

if (-not $repoRoot) {
    throw "Nao foi possivel localizar a raiz do repositorio Git."
}

$statusBefore = Invoke-GitCapture -Args @("-C", $repoRoot, "status", "--porcelain")
if (-not $statusBefore) {
    Write-Host "Nenhuma alteracao local para commit."
    exit 0
}

$branchToUse = $Branch
if (-not $branchToUse) {
    $branchToUse = Invoke-GitCapture -Args @("-C", $repoRoot, "branch", "--show-current")
}

if (-not $branchToUse) {
    throw "Nao foi possivel identificar a branch atual."
}

$currentRemoteUrl = Invoke-GitCapture -Args @("-C", $repoRoot, "remote", "get-url", $RemoteName) -AllowFailure

if ($DryRun) {
    Write-Host ("[dry-run] git -C {0} add ." -f $repoRoot)
    Write-Host ("[dry-run] git -C {0} commit -m ""{1}""" -f $repoRoot, $Message)

    if (-not $currentRemoteUrl -and $RemoteUrl) {
        Write-Host ("[dry-run] git -C {0} remote add {1} {2}" -f $repoRoot, $RemoteName, $RemoteUrl)
        $currentRemoteUrl = $RemoteUrl
    }

    if ($SkipPush) {
        Write-Host "[dry-run] push ignorado por parametro."
        exit 0
    }

    if (-not $currentRemoteUrl) {
        Write-Host "[dry-run] nenhum remoto configurado; o push nao seria executado."
        exit 0
    }

    $upstreamPreview = Invoke-GitCapture -Args @("-C", $repoRoot, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}") -AllowFailure
    if ($upstreamPreview) {
        Write-Host ("[dry-run] git -C {0} push {1} {2}" -f $repoRoot, $RemoteName, $branchToUse)
    }
    else {
        Write-Host ("[dry-run] git -C {0} push -u {1} {2}" -f $repoRoot, $RemoteName, $branchToUse)
    }

    exit 0
}

Invoke-Git -Args @("-C", $repoRoot, "add", ".")

$stagedFiles = Invoke-GitCapture -Args @("-C", $repoRoot, "diff", "--cached", "--name-only")
if (-not $stagedFiles) {
    Write-Host "Nenhuma alteracao entrou no stage."
    exit 0
}

Invoke-Git -Args @("-C", $repoRoot, "commit", "-m", $Message)

if (-not $currentRemoteUrl -and $RemoteUrl) {
    Invoke-Git -Args @("-C", $repoRoot, "remote", "add", $RemoteName, $RemoteUrl)
    $currentRemoteUrl = $RemoteUrl
    Write-Host ("Remoto '{0}' configurado: {1}" -f $RemoteName, $RemoteUrl)
}
elseif ($currentRemoteUrl -and $RemoteUrl -and $currentRemoteUrl -ne $RemoteUrl) {
    throw ("O remoto '{0}' ja aponta para '{1}'. Nao foi alterado para '{2}'." -f $RemoteName, $currentRemoteUrl, $RemoteUrl)
}

if ($SkipPush) {
    Write-Host "Commit criado localmente. Push ignorado por parametro."
    exit 0
}

if (-not $currentRemoteUrl) {
    Write-Host "Commit criado localmente, mas nenhum remoto foi configurado."
    Write-Host ("Conecte o GitHub com: git remote add {0} <URL-DO-REPOSITORIO>" -f $RemoteName)
    Write-Host ("Depois envie com: git push -u {0} {1}" -f $RemoteName, $branchToUse)
    exit 0
}

$upstream = Invoke-GitCapture -Args @("-C", $repoRoot, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}") -AllowFailure
if ($upstream) {
    Invoke-Git -Args @("-C", $repoRoot, "push", $RemoteName, $branchToUse)
}
else {
    Invoke-Git -Args @("-C", $repoRoot, "push", "-u", $RemoteName, $branchToUse)
}

Write-Host ("Commit e push concluidos para {0}/{1}." -f $RemoteName, $branchToUse)
