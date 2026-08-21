$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$RootPrefix = $Root.TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
) + [System.IO.Path]::DirectorySeparatorChar
$PathComparison = [System.StringComparison]::OrdinalIgnoreCase
$ManifestPath = Join-Path $Root "docs\chatgpt-archive\MANIFEST.json"
if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
    throw "Missing knowledge archive manifest: $ManifestPath"
}

$Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if ($Manifest.schema -ne "mimir-knowledge-archive-v1") {
    throw "Unexpected archive schema: $($Manifest.schema)"
}
if ($null -eq $Manifest.required_paths -or $Manifest.required_paths.Count -eq 0) {
    throw "Knowledge archive manifest required_paths must not be empty."
}

$SeenRequiredPaths = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
$missing = @()
foreach ($rel in $Manifest.required_paths) {
    $relText = [string]$rel
    if ([string]::IsNullOrWhiteSpace($relText)) {
        throw "Knowledge archive manifest contains a blank required path."
    }
    if ([System.IO.Path]::IsPathRooted($relText)) {
        throw "Knowledge archive manifest required path must be relative: $relText"
    }

    $segments = @($relText -split '[\\/]')
    $invalidSegments = @(
        $segments |
        Where-Object { $_ -eq '' -or $_ -eq '.' -or $_ -eq '..' }
    )
    if ($segments.Count -eq 0 -or $invalidSegments.Count -ne 0) {
        throw "Knowledge archive manifest required path must contain only normal path segments: $relText"
    }

    if (-not $SeenRequiredPaths.Add($relText)) {
        throw "Duplicate required path in knowledge archive manifest: $relText"
    }

    $p = [System.IO.Path]::GetFullPath((Join-Path $Root $relText))
    if (-not $p.StartsWith($RootPrefix, $PathComparison)) {
        throw "Knowledge archive manifest required path escapes repository root: $relText"
    }

    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) {
        $missing += $relText
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

Write-Host "PASS knowledge archive manifest paths: $($Manifest.required_paths.Count)"
Write-Host "PASS source registry markers"
Write-Host "PASS superbook cross-links and canonical markers"
Write-Host "PASS root knowledge graph cross-links"
Write-Host "PASS public-repo privacy exclusions"
Write-Host "PASS MIMIR knowledge archive verification"
