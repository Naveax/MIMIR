$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Verifier = Join-Path $PSScriptRoot "verify_mimir_knowledge_archive.ps1"
$ScratchRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("mimir-archive-path-contract-" + [guid]::NewGuid().ToString("N"))

function Write-TextFile {
    param([string]$Root, [string]$RelativePath, [string]$Content)
    $Path = Join-Path $Root $RelativePath
    $Parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    Set-Content -LiteralPath $Path -Value $Content -Encoding utf8NoBOM
}

function New-SyntheticArchive {
    param([string]$Name)

    $Root = Join-Path $ScratchRoot $Name
    New-Item -ItemType Directory -Path $Root -Force | Out-Null

    $Registry = @(
        "RL_REPLAY_COACH_V0_2_README.md",
        "rl_replay_analyzer_v0_2.py",
        "MIMIR_MASTER_BLUEPRINT_2026-08-12.md",
        "conversations-011.json",
        "gabriel_sistem_tasarimi.md"
    ) -join "`n"
    $Superbook = @(
        "SOURCE_REGISTRY.md",
        "VALIDATION_MATRIX.md",
        "HISTORICAL_TO_CURRENT_MAPPING.md",
        "R3.14A",
        "3,990,310",
        "RL REPLAY COACH V0.2",
        "SKILL FORGE",
        "212K",
        "MIMIR_KNOWLEDGE_GRAPH.md"
    ) -join "`n"
    $Graph = @(
        "MIMIR_CONTINUE_HERE.md",
        "MIMIR_ALL_SOURCES_SUPERBOOK.md",
        "docs/chatgpt-archive/SOURCE_REGISTRY.md",
        "docs/chatgpt-archive/VALIDATION_MATRIX.md",
        "docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md",
        "scripts/verify_mimir_knowledge_archive.ps1"
    ) -join "`n"

    Write-TextFile $Root "MIMIR_CONTINUE_HERE.md" "synthetic continue"
    Write-TextFile $Root "MIMIR_ALL_SOURCES_SUPERBOOK.md" $Superbook
    Write-TextFile $Root "MIMIR_KNOWLEDGE_GRAPH.md" $Graph
    Write-TextFile $Root "docs/chatgpt-archive/SOURCE_REGISTRY.md" $Registry
    Write-TextFile $Root "docs/chatgpt-archive/VALIDATION_MATRIX.md" "synthetic validation"
    Write-TextFile $Root "docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md" "synthetic mapping"

    $RequiredPaths = @(
        "MIMIR_CONTINUE_HERE.md",
        "MIMIR_ALL_SOURCES_SUPERBOOK.md",
        "MIMIR_KNOWLEDGE_GRAPH.md",
        "docs/chatgpt-archive/SOURCE_REGISTRY.md",
        "docs/chatgpt-archive/VALIDATION_MATRIX.md",
        "docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md"
    )
    $Manifest = [ordered]@{
        schema = "mimir-knowledge-archive-v1"
        required_paths = $RequiredPaths
    }
    Write-TextFile $Root "docs/chatgpt-archive/MANIFEST.json" ($Manifest | ConvertTo-Json -Depth 5)

    return $Root
}

function Set-RequiredPaths {
    param([string]$Root, [object[]]$RequiredPaths)
    $Path = Join-Path $Root "docs/chatgpt-archive/MANIFEST.json"
    $Manifest = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    $Manifest.required_paths = $RequiredPaths
    Set-Content -LiteralPath $Path -Value ($Manifest | ConvertTo-Json -Depth 5) -Encoding utf8NoBOM
}

function Assert-Rejected {
    param([string]$Root, [string]$ExpectedFragment)
    $Output = @(& pwsh -NoProfile -File $Verifier -Root $Root 2>&1)
    if ($LASTEXITCODE -eq 0) {
        throw "Expected archive verifier rejection containing '$ExpectedFragment'."
    }
    $Text = $Output -join "`n"
    if ($Text -notlike "*$ExpectedFragment*") {
        throw "Archive verifier failed for wrong reason. Expected '$ExpectedFragment'. Output: $Text"
    }
}

try {
    New-Item -ItemType Directory -Path $ScratchRoot -Force | Out-Null

    $Valid = New-SyntheticArchive "valid"
    & pwsh -NoProfile -File $Verifier -Root $Valid
    if ($LASTEXITCODE -ne 0) {
        throw "Valid synthetic archive should pass."
    }

    $Empty = New-SyntheticArchive "empty"
    Set-RequiredPaths $Empty @()
    Assert-Rejected $Empty "required_paths must not be empty"

    $Traversal = New-SyntheticArchive "traversal"
    Set-RequiredPaths $Traversal @("MIMIR_CONTINUE_HERE.md", "../outside.md")
    Assert-Rejected $Traversal "not normalized"

    $Dot = New-SyntheticArchive "dot"
    Set-RequiredPaths $Dot @("./MIMIR_CONTINUE_HERE.md")
    Assert-Rejected $Dot "not normalized"

    $Duplicate = New-SyntheticArchive "duplicate"
    Set-RequiredPaths $Duplicate @("MIMIR_CONTINUE_HERE.md", "MIMIR_CONTINUE_HERE.md")
    Assert-Rejected $Duplicate "Duplicate knowledge archive required path"

    $Absolute = New-SyntheticArchive "absolute"
    $AbsoluteTarget = Join-Path $Absolute "MIMIR_CONTINUE_HERE.md"
    Set-RequiredPaths $Absolute @($AbsoluteTarget)
    Assert-Rejected $Absolute "must be relative"

    Write-Host "PASS: knowledge archive required-path fail-closed contract tests."
}
finally {
    if (Test-Path -LiteralPath $ScratchRoot) {
        Remove-Item -LiteralPath $ScratchRoot -Recurse -Force
    }
}
