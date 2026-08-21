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
    throw "Count must be greater than zero. Actual: $Count"
}

if (-not (Test-Path -LiteralPath $ReplayRoot -PathType Container)) {
    throw "Replay root not found: $ReplayRoot"
}

$ReplayRootFull = [System.IO.Path]::GetFullPath(
    (Resolve-Path -LiteralPath $ReplayRoot -ErrorAction Stop).Path
)
$OutputRootFull = if (Test-Path -LiteralPath $OutputRoot) {
    [System.IO.Path]::GetFullPath(
        (Resolve-Path -LiteralPath $OutputRoot -ErrorAction Stop).Path
    )
} else {
    [System.IO.Path]::GetFullPath($OutputRoot)
}

$PathComparison = if ($IsWindows) {
    [System.StringComparison]::OrdinalIgnoreCase
} else {
    [System.StringComparison]::Ordinal
}
$Separator = [System.IO.Path]::DirectorySeparatorChar
$ReplayPrefix = $ReplayRootFull.TrimEnd([char[]]@('/', '\')) + $Separator
$OutputPrefix = $OutputRootFull.TrimEnd([char[]]@('/', '\')) + $Separator

$SameRoot = [string]::Equals($ReplayRootFull, $OutputRootFull, $PathComparison)
$OutputInsideReplay = $OutputPrefix.StartsWith($ReplayPrefix, $PathComparison)
$ReplayInsideOutput = $ReplayPrefix.StartsWith($OutputPrefix, $PathComparison)

if ($SameRoot -or $OutputInsideReplay -or $ReplayInsideOutput) {
    throw "ReplayRoot and OutputRoot must not overlap. replay=$ReplayRootFull output=$OutputRootFull"
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
    Sort-Object `
        @{ Expression = { [int64]$_.Length }; Descending = $true }, `
        @{ Expression = { [string]$_.FullName }; Descending = $false }
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
        selection_policy  = "largest_sha256_unique_by_file_size"
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
