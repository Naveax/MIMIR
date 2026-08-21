$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Selector = Join-Path $PSScriptRoot "select_largest_replays.ps1"
$ScratchRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("mimir-selector-contract-" + [guid]::NewGuid().ToString("N"))

function Write-Replay {
    param(
        [Parameter(Mandatory = $true)] [string]$Path,
        [Parameter(Mandatory = $true)] [string]$Text
    )

    $Parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    [System.IO.File]::WriteAllBytes($Path, [System.Text.Encoding]::UTF8.GetBytes($Text))
}

function Invoke-ExpectFailure {
    param(
        [Parameter(Mandatory = $true)] [string]$ReplayRoot,
        [Parameter(Mandatory = $true)] [string]$OutputRoot,
        [Parameter(Mandatory = $true)] [int]$Count,
        [Parameter(Mandatory = $true)] [string]$ExpectedFragment
    )

    $Output = @(
        & pwsh -NoProfile -File $Selector -ReplayRoot $ReplayRoot -OutputRoot $OutputRoot -Count $Count 2>&1
    )
    if ($LASTEXITCODE -eq 0) {
        throw "Expected selector failure containing '$ExpectedFragment'."
    }

    $Text = $Output -join "`n"
    if ($Text -notlike "*$ExpectedFragment*") {
        throw "Selector failed for the wrong reason. Expected '$ExpectedFragment'. Output: $Text"
    }
}

try {
    New-Item -ItemType Directory -Path $ScratchRoot -Force | Out-Null

    $Input = Join-Path $ScratchRoot "input"
    $Output = Join-Path $ScratchRoot "output"
    Write-Replay -Path (Join-Path $Input "z.replay") -Text "333333"
    Write-Replay -Path (Join-Path $Input "b.replay") -Text "2222"
    Write-Replay -Path (Join-Path $Input "a.replay") -Text "1111"
    Write-Replay -Path (Join-Path $Input "small.replay") -Text "x"

    & pwsh -NoProfile -File $Selector -ReplayRoot $Input -OutputRoot $Output -Count 3
    if ($LASTEXITCODE -ne 0) {
        throw "Valid replay selection should succeed."
    }

    $Rows = @(
        Get-Content -LiteralPath (Join-Path $Output "manifest.jsonl") |
        ForEach-Object { $_ | ConvertFrom-Json }
    )
    if ($Rows.Count -ne 3) {
        throw "Expected 3 manifest rows, found $($Rows.Count)."
    }
    if ($Rows[0].original_filename -cne "z.replay") {
        throw "Largest replay should rank first."
    }
    if ($Rows[1].original_filename -cne "a.replay" -or $Rows[2].original_filename -cne "b.replay") {
        throw "Equal-size replay tie must be deterministically FullName-ascending."
    }

    $SameRoot = Join-Path $ScratchRoot "same-root"
    Write-Replay -Path (Join-Path $SameRoot "keep.replay") -Text "keep-me"
    Invoke-ExpectFailure -ReplayRoot $SameRoot -OutputRoot $SameRoot -Count 1 -ExpectedFragment "must not overlap"
    if (-not (Test-Path -LiteralPath (Join-Path $SameRoot "keep.replay") -PathType Leaf)) {
        throw "Same-root guard failed to preserve replay input."
    }

    $ParentRoot = Join-Path $ScratchRoot "parent-root"
    $NestedInput = Join-Path $ParentRoot "nested-input"
    Write-Replay -Path (Join-Path $NestedInput "keep.replay") -Text "keep-me-too"
    Invoke-ExpectFailure -ReplayRoot $NestedInput -OutputRoot $ParentRoot -Count 1 -ExpectedFragment "must not overlap"
    if (-not (Test-Path -LiteralPath (Join-Path $NestedInput "keep.replay") -PathType Leaf)) {
        throw "Parent-output guard failed to preserve nested replay input."
    }

    $NestedOutputInput = Join-Path $ScratchRoot "nested-output-input"
    Write-Replay -Path (Join-Path $NestedOutputInput "keep.replay") -Text "still-keep-me"
    $NestedOutput = Join-Path $NestedOutputInput "generated"
    Invoke-ExpectFailure -ReplayRoot $NestedOutputInput -OutputRoot $NestedOutput -Count 1 -ExpectedFragment "must not overlap"
    if (-not (Test-Path -LiteralPath (Join-Path $NestedOutputInput "keep.replay") -PathType Leaf)) {
        throw "Nested-output guard failed to preserve replay input."
    }

    $CountInput = Join-Path $ScratchRoot "count-input"
    Write-Replay -Path (Join-Path $CountInput "keep.replay") -Text "count-guard"
    $CountOutput = Join-Path $ScratchRoot "count-output"
    New-Item -ItemType Directory -Path $CountOutput -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $CountOutput "sentinel.txt") -Value "do-not-delete"
    Invoke-ExpectFailure -ReplayRoot $CountInput -OutputRoot $CountOutput -Count 0 -ExpectedFragment "Count must be greater than zero"
    if (-not (Test-Path -LiteralPath (Join-Path $CountOutput "sentinel.txt") -PathType Leaf)) {
        throw "Count guard must run before output deletion."
    }

    Write-Host "PASS: replay selector destructive-path and determinism contract tests."
}
finally {
    if (Test-Path -LiteralPath $ScratchRoot) {
        Remove-Item -LiteralPath $ScratchRoot -Recurse -Force
    }
}
