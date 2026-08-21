param(
    [string]$CorpusRoot = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($CorpusRoot)) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
    $CorpusRoot = Join-Path $RepoRoot "test_corpus\largest_100"
}

$CorpusRoot = [System.IO.Path]::GetFullPath($CorpusRoot)
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
$SeenFilenames = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)

foreach ($Row in $Rows) {
    $Filename = [string]$Row.filename

    if (
        [string]::IsNullOrWhiteSpace($Filename) -or
        [System.IO.Path]::IsPathRooted($Filename) -or
        $Filename -match '[\\/]' -or
        $Filename -eq '.' -or
        $Filename -eq '..' -or
        [System.IO.Path]::GetExtension($Filename) -ine '.replay'
    ) {
        throw "Manifest filename must be a leaf .replay filename: $Filename"
    }

    if (-not $SeenFilenames.Add($Filename)) {
        throw "Duplicate filename in checked-in corpus manifest: $Filename"
    }

    $ExpectedHash = [string]$Row.sha256
    if ($ExpectedHash -notmatch '^[0-9A-Fa-f]{64}$') {
        throw "Invalid SHA-256 in checked-in corpus manifest: $Filename"
    }

    try {
        $ExpectedBytes = [int64]$Row.bytes
    }
    catch {
        throw "Invalid byte length in checked-in corpus manifest: $Filename"
    }

    if ($ExpectedBytes -lt 0) {
        throw "Invalid byte length in checked-in corpus manifest: $Filename"
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

foreach ($ReplayFile in $ReplayFiles) {
    if (-not $SeenFilenames.Contains($ReplayFile.Name)) {
        throw "Replay file is not represented exactly once in manifest: $($ReplayFile.Name)"
    }
}

Write-Host "PASS: 100 replay fixtures match exact manifest filenames + size + SHA-256."
