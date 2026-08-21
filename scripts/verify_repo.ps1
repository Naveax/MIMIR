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
    [pscustomobject]@{
        Path = Join-Path $RepoRoot "external_fixtures/sample_001.replay"
        Bytes = [int64]3001021
        Sha256 = "F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB"
    },
    [pscustomobject]@{
        Path = Join-Path $RepoRoot "external_fixtures/sample_002.replay"
        Bytes = [int64]2632903
        Sha256 = "376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6"
    },
    [pscustomobject]@{
        Path = Join-Path $RepoRoot "external_fixtures/sample_003.replay"
        Bytes = [int64]1638538
        Sha256 = "20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC"
    }
)

foreach ($FixtureSpec in $RequiredReplayFixtures) {
    if (-not (Test-Path -LiteralPath $FixtureSpec.Path -PathType Leaf)) {
        throw "Required checked-in replay fixture is missing: $($FixtureSpec.Path)"
    }

    $Fixture = Get-Item -LiteralPath $FixtureSpec.Path
    if ([int64]$Fixture.Length -ne $FixtureSpec.Bytes) {
        throw "Required checked-in replay fixture size drift: $($FixtureSpec.Path) expected=$($FixtureSpec.Bytes) actual=$($Fixture.Length)"
    }

    $Hash = (Get-FileHash -LiteralPath $FixtureSpec.Path -Algorithm SHA256).Hash.ToUpperInvariant()
    if (-not [string]::Equals($Hash, $FixtureSpec.Sha256, [System.StringComparison]::Ordinal)) {
        throw "Required checked-in replay fixture SHA-256 drift: $($FixtureSpec.Path) expected=$($FixtureSpec.Sha256) actual=$Hash"
    }
}

$env:MIMIR_REPLAY_FIXTURE_PATH = $RequiredReplayFixtures[0].Path

Write-Host ""
Write-Host "PASS: required checked-in replay fixtures match admitted size + SHA-256 identities."
Write-Host "MIMIR_REPLAY_FIXTURE_PATH=$env:MIMIR_REPLAY_FIXTURE_PATH"

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("fmt", "--all", "--", "--check")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("check", "--locked", "--workspace", "--all-targets", "--all-features")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "--locked", "-p", "mimir-replay", "--", "--nocapture")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "--locked", "-p", "mimir-skill", "--", "--nocapture")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "--locked", "--workspace", "--all-targets", "--all-features")

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @(
        "clippy",
        "--locked",
        "--workspace",
        "--all-targets",
        "--all-features",
        "--",
        "-D",
        "warnings"
    )

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @("test", "--locked", "-p", "mimir-export", "--", "--list")

$CorpusVerifier = Join-Path $PSScriptRoot "verify_test_corpus.ps1"

Write-Host ""
Write-Host "> pwsh -NoProfile -File $CorpusVerifier"

& pwsh -NoProfile -File $CorpusVerifier

if ($LASTEXITCODE -ne 0) {
    throw "Replay corpus verification failed with exit code $LASTEXITCODE."
}

$MatrixOutput = Join-Path $RepoRoot "target/replay_compatibility_matrix.jsonl"
$MatrixSummary = Join-Path $RepoRoot "target/replay_compatibility_matrix.summary.json"
$RankingOutput = Join-Path $RepoRoot "target/replay_compatibility_ranking.json"

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @(
        "run",
        "--locked",
        "-p",
        "mimir-cli",
        "--bin",
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

Invoke-VerificationCommand `
    -Executable "cargo" `
    -CommandArguments @(
        "run",
        "--locked",
        "-p",
        "mimir-cli",
        "--bin",
        "replay_compat_rank",
        "--",
        "--matrix",
        "target/replay_compatibility_matrix.jsonl",
        "--output",
        "target/replay_compatibility_ranking.json"
    )

if (-not (Test-Path -LiteralPath $RankingOutput -PathType Leaf)) {
    throw "Replay compatibility ranking output missing: $RankingOutput"
}

$Ranking = Get-Content -LiteralPath $RankingOutput -Raw | ConvertFrom-Json
if ([int]$Ranking.scanned -ne 100) {
    throw "Replay tuple ranking scanned count drift: $($Ranking.scanned)"
}
if ([int]$Ranking.rankable_rows -ne 100) {
    throw "Replay tuple ranking must currently rank all 100 corpus rows, found $($Ranking.rankable_rows)."
}
if ([int]$Ranking.unrankable_rows -ne 0) {
    throw "Replay tuple ranking unexpectedly contains unrankable rows: $($Ranking.unrankable_rows)"
}
if ([int]$Ranking.rankable_coverage_basis_points -ne 10000) {
    throw "Replay tuple ranking coverage drift: $($Ranking.rankable_coverage_basis_points) basis points"
}
if ([int]$Ranking.unique_version_tuples -ne [int]$Summary.unique_version_tuples) {
    throw "Replay tuple ranking unique tuple count drift: ranking=$($Ranking.unique_version_tuples) matrix=$($Summary.unique_version_tuples)"
}

$RankingRows = @($Ranking.rankings)
if ($RankingRows.Count -ne [int]$Ranking.unique_version_tuples) {
    throw "Replay tuple ranking row count drift: rows=$($RankingRows.Count) unique=$($Ranking.unique_version_tuples)"
}

$CountSum = [int](($RankingRows | Measure-Object -Property count -Sum).Sum)
if ($CountSum -ne [int]$Ranking.rankable_rows) {
    throw "Replay tuple ranking frequency sum drift: sum=$CountSum rankable=$($Ranking.rankable_rows)"
}

$PreviousCount = [int]::MaxValue
$ExpectedCumulative = 0
for ($Index = 0; $Index -lt $RankingRows.Count; $Index++) {
    $Entry = $RankingRows[$Index]
    $ExpectedRank = $Index + 1
    $Count = [int]$Entry.count
    $ExpectedCumulative += $Count

    if ([int]$Entry.rank -ne $ExpectedRank) {
        throw "Replay tuple ranking rank drift at index ${Index}: expected=$ExpectedRank actual=$($Entry.rank)"
    }
    if ($Count -gt $PreviousCount) {
        throw "Replay tuple ranking is not frequency-descending at rank ${ExpectedRank}: previous=$PreviousCount current=$Count"
    }
    if ([int]$Entry.cumulative_count -ne $ExpectedCumulative) {
        throw "Replay tuple ranking cumulative count drift at rank ${ExpectedRank}: expected=$ExpectedCumulative actual=$($Entry.cumulative_count)"
    }

    $PreviousCount = $Count
}

$FinalRanking = $RankingRows[-1]
if ([int]$FinalRanking.cumulative_count -ne 100) {
    throw "Replay tuple ranking final cumulative count drift: $($FinalRanking.cumulative_count)"
}
if ([int]$FinalRanking.cumulative_coverage_basis_points -ne 10000) {
    throw "Replay tuple ranking final cumulative coverage drift: $($FinalRanking.cumulative_coverage_basis_points) basis points"
}

Write-Host ""
Write-Host "PASS: replay version tuples are frequency-ranked across all 100 matrix rows."
Write-Host "Top replay version tuples:"
foreach ($Entry in @($RankingRows | Select-Object -First 10)) {
    Write-Host "rank=$($Entry.rank) count=$($Entry.count) cumulative=$($Entry.cumulative_count) coverage_bps=$($Entry.coverage_basis_points) tuple=$($Entry.major_version)|$($Entry.minor_version)|$($Entry.net_version)|$($Entry.game_type)|$($Entry.replay_version)|$($Entry.build_version)"
}

Write-Host ""
Write-Host "PASS: MIMIR repository verification completed with real command arguments."