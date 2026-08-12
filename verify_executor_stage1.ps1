param(
    [string]$Repo = 'D:\RocketLeague bot\MIMIR'
)

Set-Location $Repo

$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$logDir = ".log_archive\executor_stage1_verify_$ts"
New-Item -ItemType Directory -Force $logDir | Out-Null

$steps = @(
    @{ Name = 'fmt';   Cmd = 'cargo fmt --all' },
    @{ Name = 'check'; Cmd = 'cargo check --workspace --all-targets --all-features' },
    @{ Name = 'test';  Cmd = 'cargo test --workspace --all-targets --all-features' },
    @{ Name = 'clippy';Cmd = 'cargo clippy --workspace --all-targets --all-features -- -D warnings' },
    @{ Name = 'mimir_export_tests'; Cmd = 'cargo test -p mimir-export -- --list' }
)

foreach ($step in $steps) {
    $log = Join-Path $logDir ($step.Name + '.log')
    cmd /c "$($step.Cmd) > `"$log`" 2>&1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $($step.Name)"
        Write-Host "Log: $log"
        exit $LASTEXITCODE
    }
}

Write-Host "OK"
Write-Host "Logs: $logDir"

Get-Content (Join-Path $logDir 'mimir_export_tests.log')