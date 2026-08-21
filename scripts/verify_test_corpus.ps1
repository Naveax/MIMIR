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

$SeenFilenames = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
$SeenHashes = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)

foreach ($Row in $Rows) {
    $Filename = [string]$Row.filename

    if ([string]::IsNullOrWhiteSpace($Filename)) {
        throw "Manifest replay filename must not be blank."
    }

    if (
        [System.IO.Path]::IsPathRooted($Filename) -or
        [System.IO.Path]::GetFileName($Filename) -cne $Filename
    ) {
        throw "Manifest replay filename must be one leaf filename: $Filename"
    }

    if (-not $Filename.EndsWith(".replay", [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Manifest replay filename must end with .replay: $Filename"
    }

    if (-not $SeenFilenames.Add($Filename)) {
        throw "Duplicate filename in checked-in corpus manifest: $Filename"
    }

    $ExpectedBytes = [int64]$Row.bytes
    if ($ExpectedBytes -le 0) {
        throw "Manifest replay byte length must be positive: $Filename"
    }

    $ExpectedHash = [string]$Row.sha256
    if ($ExpectedHash -notmatch '^[0-9A-Fa-f]{64}$') {
        throw "Manifest replay SHA-256 must contain exactly 64 hexadecimal characters: $Filename"
    }

    $Path = Join-Path $CorpusRoot $Filename

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing replay: $Filename"
    }

    $Item = Get-Item -LiteralPath $Path

    if ([int64]$Item.Length -ne $ExpectedBytes) {
        throw "Size mismatch: $Filename"
    }

    $Hash = (
        Get-FileHash `
            -LiteralPath $Path `
            -Algorithm SHA256
    ).Hash.ToUpperInvariant()

    if ($Hash -ne $ExpectedHash.ToUpperInvariant()) {
        throw "Hash mismatch: $Filename"
    }

    if (-not $SeenHashes.Add($Hash)) {
        throw "Duplicate hash in checked-in corpus: $Hash"
    }
}

Write-Host "PASS: 100 replay fixtures match manifest size + SHA-256."
