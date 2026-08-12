$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

function Run([string]$Exe, [string[]]$Args) {
    Write-Host ""
    Write-Host "> $Exe $($Args -join ' ')"
    & $Exe @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Verification command failed: $Exe $($Args -join ' ')"
    }
}

Run "cargo" @("fmt", "--all", "--", "--check")
Run "cargo" @("check", "--workspace", "--all-targets", "--all-features")
Run "cargo" @("test", "-p", "mimir-replay", "--", "--nocapture")
Run "cargo" @("test", "-p", "mimir-skill", "--", "--nocapture")
Run "cargo" @("test", "--workspace", "--all-targets", "--all-features")
Run "cargo" @("clippy", "--workspace", "--all-targets", "--all-features", "--", "-D", "warnings")
Run "cargo" @("test", "-p", "mimir-export", "--", "--list")

& (Join-Path $PSScriptRoot "verify_test_corpus.ps1")

Write-Host ""
Write-Host "PASS: MIMIR repository verification completed."