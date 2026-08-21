$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Verifier = Join-Path $PSScriptRoot "verify_test_corpus.ps1"
$ScratchRoot = Join-Path (
    [System.IO.Path]::GetTempPath()
) ("mimir-corpus-contract-" + [guid]::NewGuid().ToString("N"))

function Write-ManifestRows {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CorpusRoot,

        [Parameter(Mandatory = $true)]
        [object[]]$Rows
    )

    @(
        $Rows | ForEach-Object { $_ | ConvertTo-Json -Compress }
    ) | Set-Content -LiteralPath (Join-Path $CorpusRoot "manifest.jsonl") -Encoding utf8NoBOM
}

function New-ValidSyntheticCorpus {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $CorpusRoot = Join-Path $ScratchRoot $Name
    New-Item -ItemType Directory -Path $CorpusRoot -Force | Out-Null

    $Rows = @()
    for ($Index = 0; $Index -lt 100; $Index++) {
        $Filename = "fixture_{0:D3}.replay" -f $Index
        $Path = Join-Path $CorpusRoot $Filename
        $Bytes = [System.Text.Encoding]::UTF8.GetBytes(
            "mimir-synthetic-corpus-$Index-" + ("x" * (($Index % 17) + 1))
        )
        [System.IO.File]::WriteAllBytes($Path, $Bytes)
        $Hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()

        $Rows += [pscustomobject]@{
            filename = $Filename
            bytes = [int64]$Bytes.Length
            sha256 = $Hash
        }
    }

    Write-ManifestRows -CorpusRoot $CorpusRoot -Rows $Rows
    return $CorpusRoot
}

function Read-ManifestRows {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CorpusRoot
    )

    return @(
        Get-Content -LiteralPath (Join-Path $CorpusRoot "manifest.jsonl") |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object { $_ | ConvertFrom-Json }
    )
}

function Assert-VerifierRejects {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CorpusRoot,

        [Parameter(Mandatory = $true)]
        [string]$ExpectedFragment
    )

    $Output = @(
        & pwsh -NoProfile -File $Verifier -CorpusRoot $CorpusRoot 2>&1
    )
    $ExitCode = $LASTEXITCODE

    if ($ExitCode -eq 0) {
        throw "Expected corpus verifier failure containing '$ExpectedFragment'."
    }

    $Text = $Output -join "`n"
    if ($Text -notlike "*$ExpectedFragment*") {
        throw "Corpus verifier failed for the wrong reason. Expected '$ExpectedFragment'. Output: $Text"
    }
}

try {
    New-Item -ItemType Directory -Path $ScratchRoot -Force | Out-Null

    $Valid = New-ValidSyntheticCorpus -Name "valid"
    & pwsh -NoProfile -File $Verifier -CorpusRoot $Valid
    if ($LASTEXITCODE -ne 0) {
        throw "Valid synthetic corpus should pass verification."
    }

    $Traversal = New-ValidSyntheticCorpus -Name "path-traversal"
    $Rows = Read-ManifestRows -CorpusRoot $Traversal
    $Rows[0].filename = "../escape.replay"
    Write-ManifestRows -CorpusRoot $Traversal -Rows $Rows
    Assert-VerifierRejects -CorpusRoot $Traversal -ExpectedFragment "Unsafe manifest replay filename"

    $Duplicate = New-ValidSyntheticCorpus -Name "duplicate-filename"
    $Rows = Read-ManifestRows -CorpusRoot $Duplicate
    $Rows[1].filename = $Rows[0].filename
    Write-ManifestRows -CorpusRoot $Duplicate -Rows $Rows
    Assert-VerifierRejects -CorpusRoot $Duplicate -ExpectedFragment "Duplicate filename"

    $BadHash = New-ValidSyntheticCorpus -Name "invalid-sha"
    $Rows = Read-ManifestRows -CorpusRoot $BadHash
    $Rows[0].sha256 = "not-a-sha256"
    Write-ManifestRows -CorpusRoot $BadHash -Rows $Rows
    Assert-VerifierRejects -CorpusRoot $BadHash -ExpectedFragment "Invalid SHA-256"

    $WrongExtension = New-ValidSyntheticCorpus -Name "wrong-extension"
    $Rows = Read-ManifestRows -CorpusRoot $WrongExtension
    $Rows[0].filename = "fixture_000.txt"
    Write-ManifestRows -CorpusRoot $WrongExtension -Rows $Rows
    Assert-VerifierRejects -CorpusRoot $WrongExtension -ExpectedFragment "must use .replay extension"

    $ZeroLength = New-ValidSyntheticCorpus -Name "zero-length"
    $Rows = Read-ManifestRows -CorpusRoot $ZeroLength
    $Rows[0].bytes = 0
    Write-ManifestRows -CorpusRoot $ZeroLength -Rows $Rows
    Assert-VerifierRejects -CorpusRoot $ZeroLength -ExpectedFragment "byte length must be positive"

    Write-Host "PASS: replay corpus verifier fail-closed contract tests."
}
finally {
    if (Test-Path -LiteralPath $ScratchRoot) {
        Remove-Item -LiteralPath $ScratchRoot -Recurse -Force
    }
}
