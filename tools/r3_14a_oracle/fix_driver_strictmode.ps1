[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Path = Join-Path $PSScriptRoot 'run_oracle.ps1'
$text = Get-Content -Raw -LiteralPath $Path

$replacements = @(
    [pscustomobject]@{
        Old = 'if ((Compare-Object $expectedOracleChanged $oracleChanged).Count -ne 0) {'
        New = 'if (@(Compare-Object $expectedOracleChanged $oracleChanged).Count -ne 0) {'
    },
    [pscustomobject]@{
        Old = 'if ((Compare-Object $expectedOracleChanged $oracleChangedAfter).Count -ne 0) { throw "oracle patch scope drifted after parse" }'
        New = 'if (@(Compare-Object $expectedOracleChanged $oracleChangedAfter).Count -ne 0) { throw "oracle patch scope drifted after parse" }'
    },
    [pscustomobject]@{
        Old = '$probe = Join-Path $boxcars ''target\debug\examples\r3_14a_probe.exe'''
        New = '$probeRelative = if ($IsWindows) { ''target\debug\examples\r3_14a_probe.exe'' } else { ''target/debug/examples/r3_14a_probe'' }`n$probe = Join-Path $boxcars $probeRelative'
    },
    [pscustomobject]@{
        Old = '    $lines = @(& $probe $resolved 2>&1 | ForEach-Object { $_.ToString() })'
        New = '    $lines = @(& $probe $resolved 2>&1 | ForEach-Object { $_.ToString() })`n    $lines = @($lines | ForEach-Object { $_.Replace(''\t'', "`t") })'
    },
    [pscustomobject]@{
        Old = '        throw "expected exactly one first-frame evidence row for $relative"'
        New = '        $lines | ForEach-Object { Write-Host "R3_14A_PROBE_OUTPUT $_" }`n        throw "expected exactly one first-frame evidence row for $relative; normalized matcher still failed"'
    }
)

foreach ($replacement in $replacements) {
    $old = $replacement.Old
    $new = $replacement.New.Replace('`n', [Environment]::NewLine)
    $count = ([regex]::Matches($text, [regex]::Escape($old))).Count
    if ($count -ne 1) {
        throw "Deterministic driver patch expected exactly one match, found $count for: $old"
    }
    $text = $text.Replace($old, $new)
}

Set-Content -LiteralPath $Path -Value $text -Encoding utf8NoBOM -NoNewline

$effectiveText = Get-Content -Raw -LiteralPath $Path
foreach ($replacement in $replacements) {
    $old = $replacement.Old
    $expectedNew = $replacement.New.Replace('`n', [Environment]::NewLine)
    if (-not $effectiveText.Contains($expectedNew)) {
        throw "Expected corrected driver expression missing after patch: $expectedNew"
    }
    if (-not $expectedNew.Contains($old) -and $effectiveText.Contains($old)) {
        throw "Unsafe or platform-specific driver expression remains after deterministic patch: $old"
    }
}

$effectiveSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
Set-Content -LiteralPath 'r3_14a_effective_driver_sha256.txt' -Encoding utf8NoBOM -Value "effective_driver_sha256=$effectiveSha"
Write-Host "R3_14A_EFFECTIVE_DRIVER_SHA256=$effectiveSha"
Write-Host 'R3_14A_DRIVER_CORRECTION=PASS'
