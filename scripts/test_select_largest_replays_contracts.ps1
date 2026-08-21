$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Selector = Join-Path $PSScriptRoot "select_largest_replays.ps1"
if (-not (Test-Path -LiteralPath $Selector -PathType Leaf)) {
    throw "Selector script not found: $Selector"
}

$Root = Join-Path ([System.IO.Path]::GetTempPath()) ("mimir-select-replay-contracts-" + [guid]::NewGuid().ToString("N"))
$InputRoot = Join-Path $Root "input"
$OutputRoot = Join-Path $Root "output"
New-Item -ItemType Directory -Path $InputRoot -Force | Out-Null

function Write-TestReplay {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [byte[]]$Bytes
    )

    [System.IO.File]::WriteAllBytes($Path, $Bytes)
}

function Assert-Throws {
    param(
        [Parameter(Mandatory = $true)]
        [scriptblock]$Action,

        [Parameter(Mandatory = $true)]
        [string]$ExpectedMessagePart
    )

    $Threw = $false
    try {
        & $Action
    } catch {
        $Threw = $true
        if (-not $_.Exception.Message.Contains($ExpectedMessagePart)) {
            throw "Unexpected failure. Expected message containing '$ExpectedMessagePart', got '$($_.Exception.Message)'"
        }
    }

    if (-not $Threw) {
        throw "Expected action to fail with message containing '$ExpectedMessagePart'."
    }
}

try {
    Write-TestReplay -Path (Join-Path $InputRoot "c_large.replay") -Bytes ([byte[]](1, 2, 3, 4, 5))
    Write-TestReplay -Path (Join-Path $InputRoot "d_duplicate.replay") -Bytes ([byte[]](1, 2, 3, 4, 5))
    Write-TestReplay -Path (Join-Path $InputRoot "a_tie.replay") -Bytes ([byte[]](10, 11, 12))
    Write-TestReplay -Path (Join-Path $InputRoot "b_tie.replay") -Bytes ([byte[]](20, 21, 22))

    $Sentinel = Join-Path $InputRoot "source-sentinel.txt"
    [System.IO.File]::WriteAllText($Sentinel, "must-survive")

    Assert-Throws -ExpectedMessagePart "Count must be greater than zero" -Action {
        & $Selector -ReplayRoot $InputRoot -OutputRoot (Join-Path $Root "count-zero-output") -Count 0
    }

    Assert-Throws -ExpectedMessagePart "must not overlap" -Action {
        & $Selector -ReplayRoot $InputRoot -OutputRoot $InputRoot -Count 1
    }
    if (-not (Test-Path -LiteralPath $Sentinel -PathType Leaf)) {
        throw "Same-root rejection happened too late; source sentinel was deleted."
    }

    Assert-Throws -ExpectedMessagePart "must not overlap" -Action {
        & $Selector -ReplayRoot $InputRoot -OutputRoot $Root -Count 1
    }
    if (-not (Test-Path -LiteralPath $Sentinel -PathType Leaf)) {
        throw "Ancestor-output rejection happened too late; source sentinel was deleted."
    }

    Assert-Throws -ExpectedMessagePart "must not overlap" -Action {
        & $Selector -ReplayRoot $InputRoot -OutputRoot (Join-Path $InputRoot "nested-output") -Count 1
    }

    & $Selector -ReplayRoot $InputRoot -OutputRoot $OutputRoot -Count 3

    $Manifest = Join-Path $OutputRoot "manifest.jsonl"
    if (-not (Test-Path -LiteralPath $Manifest -PathType Leaf)) {
        throw "Valid selection did not create manifest.jsonl."
    }

    $Rows = @(
        Get-Content -LiteralPath $Manifest |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object { $_ | ConvertFrom-Json }
    )
    if ($Rows.Count -ne 3) {
        throw "Expected 3 manifest rows, found $($Rows.Count)."
    }

    $ExpectedOriginals = @("c_large.replay", "a_tie.replay", "b_tie.replay")
    for ($Index = 0; $Index -lt $ExpectedOriginals.Count; $Index++) {
        $ExpectedRank = $Index + 1
        $Row = $Rows[$Index]
        if ([int]$Row.rank -ne $ExpectedRank) {
            throw "Rank drift at index ${Index}: expected=$ExpectedRank actual=$($Row.rank)"
        }
        if ([string]$Row.original_filename -cne $ExpectedOriginals[$Index]) {
            throw "Deterministic selection drift at rank ${ExpectedRank}: expected=$($ExpectedOriginals[$Index]) actual=$($Row.original_filename)"
        }
        $SelectedPath = Join-Path $OutputRoot ([string]$Row.filename)
        if (-not (Test-Path -LiteralPath $SelectedPath -PathType Leaf)) {
            throw "Selected replay missing: $SelectedPath"
        }
        $Hash = (Get-FileHash -LiteralPath $SelectedPath -Algorithm SHA256).Hash.ToUpperInvariant()
        if ($Hash -cne [string]$Row.sha256) {
            throw "Selected replay hash drift: $($Row.filename)"
        }
    }

    $DuplicateRows = @(
        $Rows | Where-Object { [string]$_.original_filename -ceq "d_duplicate.replay" }
    )
    if ($DuplicateRows.Count -ne 0) {
        throw "Duplicate-content replay was selected more than once."
    }

    Write-Host "SELECT_LARGEST_REPLAYS_CONTRACTS=PASS"
} finally {
    if (Test-Path -LiteralPath $Root) {
        Remove-Item -LiteralPath $Root -Recurse -Force
    }
}
