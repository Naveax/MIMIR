[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[^/]+/[^/]+$')]
    [string]$Repository,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-fA-F]{40}$')]
    [string]$HeadSha,

    [Parameter(Mandatory = $true)]
    [string]$Workflow,

    [string]$Event,

    [string]$HeadBranch,

    [long]$ExcludeRunId = 0,

    [switch]$JsonOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Exit codes:
#   0 = no equivalent active run exists
#   3 = an equivalent queued/waiting/in-progress run already exists
# Any other non-zero exit is an inspection failure and must not be treated as
# permission to dispatch a new workflow run.

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'GitHub CLI (gh) is required to inspect active workflow runs.'
}

$HeadSha = $HeadSha.ToLowerInvariant()
$ActiveStatuses = @('queued', 'in_progress', 'waiting', 'requested', 'pending')
$RunsById = @{}

foreach ($Status in $ActiveStatuses) {
    $Endpoint = "repos/$Repository/actions/runs?head_sha=$HeadSha&status=$Status&per_page=100"
    $Raw = & gh api $Endpoint
    if ($LASTEXITCODE -ne 0) {
        throw "gh api failed while inspecting active workflow runs for status '$Status'."
    }

    $Response = $Raw | ConvertFrom-Json
    foreach ($Run in @($Response.workflow_runs)) {
        if ($null -eq $Run.id) {
            continue
        }

        $RunsById[[string]$Run.id] = $Run
    }
}

$Candidates = @(
    foreach ($Run in $RunsById.Values) {
        $RunSha = [string]$Run.head_sha
        if ($RunSha.ToLowerInvariant() -cne $HeadSha) {
            continue
        }

        $WorkflowMatches =
            if ($Workflow -match '^\d+$') {
                [string]$Run.workflow_id -ceq $Workflow
            }
            else {
                ([string]$Run.name -ceq $Workflow) -or ([string]$Run.path -ceq $Workflow)
            }

        if (-not $WorkflowMatches) {
            continue
        }

        if (-not [string]::IsNullOrWhiteSpace($Event) -and [string]$Run.event -cne $Event) {
            continue
        }

        if (-not [string]::IsNullOrWhiteSpace($HeadBranch) -and [string]$Run.head_branch -cne $HeadBranch) {
            continue
        }

        if ($ExcludeRunId -gt 0 -and [long]$Run.id -eq $ExcludeRunId) {
            continue
        }

        $Run
    }
)

$EquivalentRun = @(
    $Candidates |
        Sort-Object -Property @{ Expression = { [datetimeoffset]$_.created_at }; Descending = $true }
) | Select-Object -First 1

if ($null -ne $EquivalentRun) {
    $Result = [ordered]@{
        equivalent_active_run = $true
        run_id = [long]$EquivalentRun.id
        workflow_id = [long]$EquivalentRun.workflow_id
        workflow_name = [string]$EquivalentRun.name
        status = [string]$EquivalentRun.status
        event = [string]$EquivalentRun.event
        head_branch = [string]$EquivalentRun.head_branch
        head_sha = ([string]$EquivalentRun.head_sha).ToLowerInvariant()
        html_url = [string]$EquivalentRun.html_url
    }

    if (-not $JsonOnly) {
        Write-Host (
            'MIMIR_EQUIVALENT_ACTIVE_RUN=FOUND ' +
            "run_id=$($Result.run_id) status=$($Result.status) " +
            "workflow=$($Result.workflow_name) event=$($Result.event)"
        )
    }

    $Result | ConvertTo-Json -Depth 4
    exit 3
}

$Result = [ordered]@{
    equivalent_active_run = $false
    run_id = $null
    workflow = $Workflow
    event = if ([string]::IsNullOrWhiteSpace($Event)) { $null } else { $Event }
    head_branch = if ([string]::IsNullOrWhiteSpace($HeadBranch)) { $null } else { $HeadBranch }
    head_sha = $HeadSha
}

if (-not $JsonOnly) {
    Write-Host 'MIMIR_EQUIVALENT_ACTIVE_RUN=NONE'
}

$Result | ConvertTo-Json -Depth 4
exit 0
