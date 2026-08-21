param(
    [string]$Root = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
else {
    $Root = (Resolve-Path -LiteralPath $Root).Path
}

$ManifestPath = Join-Path $Root "docs\chatgpt-archive\MANIFEST.json"
if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
    throw "Missing knowledge archive manifest: $ManifestPath"
}

$Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if ($Manifest.schema -ne "mimir-knowledge-archive-v1") {
    throw "Unexpected archive schema: $($Manifest.schema)"
}

$RequiredPaths = @($Manifest.required_paths)
if ($RequiredPaths.Count -eq 0) {
    throw "Knowledge archive manifest required_paths must not be empty."
}

$RootFull = [System.IO.Path]::GetFullPath($Root)
$RootPrefix = [System.IO.Path]::TrimEndingDirectorySeparator($RootFull) + [System.IO.Path]::DirectorySeparatorChar
$SeenRequiredPaths = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
$missing = @()

foreach ($relValue in $RequiredPaths) {
    $rel = [string]$relValue
    if ([string]::IsNullOrWhiteSpace($rel)) {
        throw "Knowledge archive manifest contains an empty required path."
    }
    if ([System.IO.Path]::IsPathRooted($rel)) {
        throw "Knowledge archive manifest required path must be relative: $rel"
    }

    $Segments = @($rel -split '[\\/]')
    if ($Segments.Count -eq 0 -or @($Segments | Where-Object { $_ -eq '' -or $_ -eq '.' -or $_ -eq '..' }).Count -ne 0) {
        throw "Knowledge archive manifest required path is not normalized: $rel"
    }

    $p = [System.IO.Path]::GetFullPath((Join-Path $RootFull $rel))
    if (-not $p.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Knowledge archive manifest required path escapes repository root: $rel"
    }
    if (-not $SeenRequiredPaths.Add($p)) {
        throw "Duplicate knowledge archive required path: $rel"
    }
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) {
        $missing += $rel
    }
}
if ($missing.Count -ne 0) {
    throw "Missing archive paths: $($missing -join ', ')"
}

$Registry = Get-Content -LiteralPath (Join-Path $Root "docs\chatgpt-archive\SOURCE_REGISTRY.md") -Raw
$Superbook = Get-Content -LiteralPath (Join-Path $Root "MIMIR_ALL_SOURCES_SUPERBOOK.md") -Raw
$Continue = Get-Content -LiteralPath (Join-Path $Root "MIMIR_CONTINUE_HERE.md") -Raw
$Graph = Get-Content -LiteralPath (Join-Path $Root "MIMIR_KNOWLEDGE_GRAPH.md") -Raw

$requiredRegistryMarkers = @(
    "RL_REPLAY_COACH_V0_2_README.md",
    "rl_replay_analyzer_v0_2.py",
    "MIMIR_MASTER_BLUEPRINT_2026-08-12.md",
    "conversations-011.json",
    "gabriel_sistem_tasarimi.md"
)
foreach ($marker in $requiredRegistryMarkers) {
    if (-not $Registry.Contains($marker)) {
        throw "SOURCE_REGISTRY missing marker: $marker"
    }
}

$requiredSuperbookMarkers = @(
    "SOURCE_REGISTRY.md",
    "VALIDATION_MATRIX.md",
    "HISTORICAL_TO_CURRENT_MAPPING.md",
    "R3.14A",
    "3,990,310",
    "RL REPLAY COACH V0.2",
    "SKILL FORGE",
    "212K"
)
foreach ($marker in $requiredSuperbookMarkers) {
    if (-not $Superbook.Contains($marker)) {
        throw "Superbook missing marker: $marker"
    }
}

$requiredGraphMarkers = @(
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_ALL_SOURCES_SUPERBOOK.md",
    "docs/chatgpt-archive/SOURCE_REGISTRY.md",
    "docs/chatgpt-archive/VALIDATION_MATRIX.md",
    "docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md",
    "scripts/verify_mimir_knowledge_archive.ps1"
)
foreach ($marker in $requiredGraphMarkers) {
    if (-not $Graph.Contains($marker)) {
        throw "MIMIR_KNOWLEDGE_GRAPH.md missing marker: $marker"
    }
}
if (-not $Superbook.Contains("MIMIR_KNOWLEDGE_GRAPH.md")) {
    throw "Superbook does not link the root knowledge graph."
}

# Public-repo privacy gate: mixed raw exports must not be mirrored wholesale.
$forbiddenPaths = @(
    "docs\chatgpt-archive\historical\conversations-011.json",
    "docs\chatgpt-archive\historical\Naveax_replay_extracted_settings.json"
)
foreach ($rel in $forbiddenPaths) {
    if (Test-Path -LiteralPath (Join-Path $Root $rel)) {
        throw "Forbidden raw private/mixed source mirrored into public archive: $rel"
    }
}

Write-Host "PASS knowledge archive manifest paths: $($RequiredPaths.Count)"
Write-Host "PASS source registry markers"
Write-Host "PASS superbook cross-links and canonical markers"
Write-Host "PASS root knowledge graph cross-links"
Write-Host "PASS public-repo privacy exclusions"
Write-Host "PASS MIMIR knowledge archive verification"
