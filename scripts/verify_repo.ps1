$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

function Invoke-VerificationCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,

        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [string[]]$CommandArguments
    )

    Write-Host ""
    Write-Host "> $Executable $($CommandArguments -join ' ')"

    & $Executable @CommandArguments

    if ($LASTEXITCODE -ne 0) {
        throw "Verification command failed ($LASTEXITCODE): $Executable $($CommandArguments -join ' ')"
    }
}

$RequiredReplayFixtures = @(
    (Join-Path $RepoRoot "external_fixtures/sample_001.replay"),
    (Join-Path $RepoRoot "external_fixtures/sample_002.replay"),
    (Join-Path $RepoRoot "external_fixtures/sample_003.replay")
)

foreach ($FixturePath in $RequiredReplayFixtures) {
    if (-not (Test-Path -LiteralPath $FixturePath -PathType Leaf)) {
        throw "Required checked-in replay fixture is missing: $FixturePath"
    }

    $Fixture = Get-Item -LiteralPath $FixturePath
    if ($Fixture.Length -le 0) {
        throw "Required checked-in replay fixture is empty: $FixturePath"
    }
}

$env:MIMIR_REPLAY_FIXTURE_PATH = $RequiredReplayFixtures[0]

Write-Host ""
Write-Host "PASS: required checked-in replay fixtures are present."
Write-Host "MIMIR_REPLAY_FIXTURE_PATH=$env:MIMIR_REPLAY_FIXTURE_PATH"

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("fmt", "--all", "--", "--check")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("check", "--workspace", "--all-targets", "--all-features")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "-p", "mimir-replay", "--", "--nocapture")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "-p", "mimir-skill", "--", "--nocapture")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "--workspace", "--all-targets", "--all-features")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @(
        "clippy",
        "--workspace",
        "--all-targets",
        "--all-features",
        "--",
        "-D",
        "warnings"
    )

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "-p", "mimir-export", "--", "--list")

$CorpusVerifier = Join-Path $PSScriptRoot "verify_test_corpus.ps1"

Write-Host ""
Write-Host "> pwsh -NoProfile -File $CorpusVerifier"

& pwsh -NoProfile -File $CorpusVerifier

if ($LASTEXITCODE -ne 0) {
    throw "Replay corpus verification failed with exit code $LASTEXITCODE."
}

$MatrixOutput = Join-Path $RepoRoot "target/replay_compatibility_matrix.jsonl"
$MatrixSummary = Join-Path $RepoRoot "target/replay_compatibility_matrix.summary.json"

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @(
        "run",
        "-p",
        "mimir-cli",
        "--",
        "replay-compat-matrix",
        "--corpus-root",
        "test_corpus/largest_100",
        "--output",
        "target/replay_compatibility_matrix.jsonl"
    )

if (-not (Test-Path -LiteralPath $MatrixOutput -PathType Leaf)) {
    throw "Replay compatibility matrix output missing: $MatrixOutput"
}

if (-not (Test-Path -LiteralPath $MatrixSummary -PathType Leaf)) {
    throw "Replay compatibility matrix summary missing: $MatrixSummary"
}

$MatrixRows = @(
    Get-Content -LiteralPath $MatrixOutput |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
)

if ($MatrixRows.Count -ne 100) {
    throw "Expected 100 replay compatibility rows, found $($MatrixRows.Count)."
}

$Summary = Get-Content -LiteralPath $MatrixSummary -Raw | ConvertFrom-Json
if ([int]$Summary.scanned -ne 100) {
    throw "Replay compatibility summary scanned count drift: $($Summary.scanned)"
}

Write-Host ""
Write-Host "PASS: replay compatibility matrix scanned 100 checked-in replays."
Write-Host "supported=$($Summary.supported) unsupported=$($Summary.unsupported) malformed=$($Summary.malformed) mapping_error=$($Summary.mapping_error) other_error=$($Summary.other_error)"
Write-Host "unique_version_tuples=$($Summary.unique_version_tuples) unique_builds=$($Summary.unique_builds)"

Write-Host ""
Write-Host "PASS: MIMIR repository verification completed with real command arguments."