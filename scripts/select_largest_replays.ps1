param(
    [Parameter(Mandatory = $true)]
    [string]$ReplayRoot,

    [Parameter(Mandatory = $true)]
    [string]$OutputRoot,

    [int]$Count = 100
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($Count -le 0) {
    throw "Count must be greater than zero."
}

if (-not (Test-Path -LiteralPath $ReplayRoot -PathType Container)) {
    throw "Replay root not found: $ReplayRoot"
}

$ReplayRootFull = (Get-Item -LiteralPath $ReplayRoot -ErrorAction Stop).FullName.TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
)
$OutputRootFull = [System.IO.Path]::GetFullPath($OutputRoot).TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
)
$OutputFilesystemRoot = [System.IO.Path]::GetPathRoot($OutputRootFull).TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
)
$PathComparison = [System.StringComparison]::OrdinalIgnoreCase

if ($OutputRootFull.Equals($OutputFilesystemRoot, $PathComparison)) {
    throw "Output root must not be a filesystem root: $OutputRootFull"
}

if ($OutputRootFull.Equals($ReplayRootFull, $PathComparison)) {
    throw "Output root must not be the replay root: $OutputRootFull"
}

$OutputPrefix = $OutputRootFull + [System.IO.Path]::DirectorySeparatorChar
$ReplayPrefix = $ReplayRootFull + [System.IO.Path]::DirectorySeparatorChar
if ($ReplayPrefix.StartsWith($OutputPrefix, $PathComparison)) {
    throw "Output root must not contain the replay root: $OutputRootFull"
}

if (Test-Path -LiteralPath $OutputRootFull) {
    Remove-Item -LiteralPath $OutputRootFull -Recurse -Force
}
New-Item -ItemType Directory -Path $OutputRootFull -Force | Out-Null

$ManifestPath = Join-Path $OutputRootFull "manifest.jsonl"

$Files = @(
    Get-ChildItem `
        -LiteralPath $ReplayRootFull `
        -File `
        -Filter "*.replay" `
        -Recurse `
        -Force `
        -ErrorAction Stop |
    Sort-Object -Property `
        @{ Expression = "Length"; Descending = $true }, `
        @{ Expression = "FullName"; Descending = $false }
)

if ($Files.Count -lt $Count) {
    throw "Not enough replay files. Found $($Files.Count), need $Count."
}

$Seen = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)

$Selected = [System.Collections.Generic.List[object]]::new()

foreach ($File in $Files) {
    if ($Selected.Count -ge $Count) {
        break
    }

    $Hash = (
        Get-FileHash `
            -LiteralPath $File.FullName `
            -Algorithm SHA256
    ).Hash.ToUpperInvariant()

    if (-not $Seen.Add($Hash)) {
        continue
    }

    $Rank = $Selected.Count + 1
    $Name = "{0:D3}_{1}" -f $Rank, $File.Name
    $Dest = Join-Path $OutputRootFull $Name

    Copy-Item `
        -LiteralPath $File.FullName `
        -Destination $Dest `
        -Force

    $Record = [ordered]@{
        rank              = $Rank
        fixture_id        = "largest_{0:D3}" -f $Rank
        filename          = $Name
        original_filename = $File.Name
        bytes             = [int64]$File.Length
        sha256            = $Hash
        source            = "RLCS_REPLAYS_1V1"
        selection_policy  = "largest_sha256_unique_by_file_size_then_full_path"
    }

    $Json = $Record | ConvertTo-Json -Compress
    [System.IO.File]::AppendAllText(
        $ManifestPath,
        $Json + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )

    $Selected.Add([PSCustomObject]@{
        Rank   = $Rank
        Name   = $Name
        Bytes  = [int64]$File.Length
        SHA256 = $Hash
    })

    Write-Host ("[{0:D3}/{1}] {2}" -f $Rank, $Count, $File.Name)
}

if ($Selected.Count -ne $Count) {
    throw "Could select only $($Selected.Count) unique replay files."
}

$Total = ($Selected | Measure-Object Bytes -Sum).Sum
$Largest = ($Selected | Sort-Object Bytes -Descending | Select-Object -First 1).Bytes
$Smallest = ($Selected | Sort-Object Bytes | Select-Object -First 1).Bytes

Write-Host ""
Write-Host "Selected: $($Selected.Count)"
Write-Host ("Total bytes: {0:N0}" -f $Total)
Write-Host ("Largest: {0:N0}" -f $Largest)
Write-Host ("Smallest: {0:N0}" -f $Smallest)
Write-Host "Manifest: $ManifestPath"
