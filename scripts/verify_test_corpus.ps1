param(
    [string]$CorpusRoot = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($CorpusRoot)) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
    $CorpusRoot = Join-Path $RepoRoot "test_corpus\largest_100"
}

$Manifest = Join-Path $CorpusRoot "manifest.jsonl"

if (-not (Test-Path -LiteralPath $Manifest -PathType Leaf)) {
    throw "Manifest not found: $Manifest"
}

$Rows = @(
    Get-Content -LiteralPath $Manifest |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
    ForEach-Object { $_ | ConvertFrom-Json }
)

if ($Rows.Count -ne 100) {
    throw "Expected 100 manifest rows, found $($Rows.Count)."
}

$ReplayFiles = @(
    Get-ChildItem `
        -LiteralPath $CorpusRoot `
        -File `
        -Filter "*.replay"
)

if ($ReplayFiles.Count -ne 100) {
    throw "Expected 100 replay files, found $($ReplayFiles.Count)."
}

$SeenHashes = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)

foreach ($Row in $Rows) {
    $Path = Join-Path $CorpusRoot $Row.filename

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing replay: $($Row.filename)"
    }

    $Item = Get-Item -LiteralPath $Path

    if ([int64]$Item.Length -ne [int64]$Row.bytes) {
        throw "Size mismatch: $($Row.filename)"
    }

    $Hash = (
        Get-FileHash `
            -LiteralPath $Path `
            -Algorithm SHA256
    ).Hash.ToUpperInvariant()

    if ($Hash -ne [string]$Row.sha256) {
        throw "Hash mismatch: $($Row.filename)"
    }

    if (-not $SeenHashes.Add($Hash)) {
        throw "Duplicate hash in checked-in corpus: $Hash"
    }
}

Write-Host "PASS: 100 replay fixtures match manifest size + SHA-256."