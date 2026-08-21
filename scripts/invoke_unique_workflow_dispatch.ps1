[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[^/]+/[^/]+$')]
    [string]$Repository,

    [Parameter(Mandatory = $true)]
    [string]$Workflow,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Ref,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$HeadBranch,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-fA-F]{40}$')]
    [string]$HeadSha,

    [string[]]$Input = @(),

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'GitHub CLI (gh) is required to dispatch workflows.'
}

$HeadSha = $HeadSha.ToLowerInvariant()

foreach ($Entry in $Input) {
    if ($Entry -notmatch '^[^=\s]+=.+' ) {
        throw "Workflow input must use non-empty name=value form: $Entry"
    }
}

$ResolvedRaw = & gh api "repos/$Repository/commits/$Ref" --jq '.sha'
if ($LASTEXITCODE -ne 0) {
    throw "Failed to resolve workflow dispatch ref '$Ref' in $Repository."
}

$ResolvedSha = (($ResolvedRaw | Out-String).Trim()).ToLowerInvariant()
if ($ResolvedSha -notmatch '^[0-9a-f]{40}$') {
    throw "Resolved ref '$Ref' returned an invalid commit SHA: $ResolvedSha"
}
if ($ResolvedSha -cne $HeadSha) {
    throw "Workflow dispatch ref drift: ref=$Ref expected=$HeadSha resolved=$ResolvedSha"
}

$Guard = Join-Path $PSScriptRoot 'find_equivalent_active_action_run.ps1'
if (-not (Test-Path -LiteralPath $Guard -PathType Leaf)) {
    throw "Equivalent-run guard not found: $Guard"
}

$GuardArguments = @(
    '-NoProfile',
    '-File', $Guard,
    '-Repository', $Repository,
    '-HeadSha', $HeadSha,
    '-Workflow', $Workflow,
    '-Event', 'workflow_dispatch',
    '-HeadBranch', $HeadBranch,
    '-JsonOnly'
)

$GuardOutput = @(& pwsh @GuardArguments 2>&1)
$GuardExitCode = $LASTEXITCODE

if ($GuardExitCode -eq 3) {
    $GuardOutput | ForEach-Object { Write-Output $_ }
    exit 3
}
if ($GuardExitCode -ne 0) {
    $Text = $GuardOutput -join "`n"
    throw "Equivalent-run inspection failed with exit code $GuardExitCode. Output: $Text"
}

if ($DryRun) {
    [ordered]@{
        dispatch_ready = $true
        dry_run = $true
        repository = $Repository
        workflow = $Workflow
        ref = $Ref
        head_branch = $HeadBranch
        head_sha = $HeadSha
    } | ConvertTo-Json -Depth 4
    exit 0
}

$DispatchArguments = @(
    'workflow', 'run', $Workflow,
    '--repo', $Repository,
    '--ref', $Ref
)
foreach ($Entry in $Input) {
    $DispatchArguments += @('-f', $Entry)
}

& gh @DispatchArguments
if ($LASTEXITCODE -ne 0) {
    throw "Workflow dispatch failed for '$Workflow' at ref '$Ref'."
}

[ordered]@{
    dispatched = $true
    repository = $Repository
    workflow = $Workflow
    ref = $Ref
    head_branch = $HeadBranch
    head_sha = $HeadSha
    input_count = $Input.Count
} | ConvertTo-Json -Depth 4
