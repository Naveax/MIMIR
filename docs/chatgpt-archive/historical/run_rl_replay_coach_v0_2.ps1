param(
  [Parameter(Mandatory=$true)] [string]$ReplayPath,
  [string]$Player = "Naveax",
  [string]$OutPrefix = ""
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $ReplayPath)) {
  throw "Replay not found: $ReplayPath"
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Analyzer = Join-Path $ScriptDir "rl_replay_analyzer_v0_2.py"
if (!(Test-Path $Analyzer)) {
  throw "Analyzer not found next to this PS1: $Analyzer"
}

if ([string]::IsNullOrWhiteSpace($OutPrefix)) {
  $base = [System.IO.Path]::GetFileNameWithoutExtension($ReplayPath)
  $dir = Split-Path -Parent $ReplayPath
  $OutPrefix = Join-Path $dir ($base + "_v0_2")
}

$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) {
  & py $Analyzer $ReplayPath --player $Player --out-prefix $OutPrefix --zip
} else {
  & python $Analyzer $ReplayPath --player $Player --out-prefix $OutPrefix --zip
}

Write-Host "`nDone. Outputs prefix: $OutPrefix" -ForegroundColor Green
