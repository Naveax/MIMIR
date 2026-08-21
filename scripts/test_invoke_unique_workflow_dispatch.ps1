$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Wrapper = Join-Path $PSScriptRoot 'invoke_unique_workflow_dispatch.ps1'
$ScratchRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('mimir-dispatch-contract-' + [guid]::NewGuid().ToString('N'))
$FakeBin = Join-Path $ScratchRoot 'bin'
$LogPath = Join-Path $ScratchRoot 'gh-workflow-run.log'
$OldPath = $env:PATH

$ExpectedSha = '0123456789abcdef0123456789abcdef01234567'
$OtherSha = '1111111111111111111111111111111111111111'
$Repository = 'Naveax/MIMIR'
$Workflow = 'Example Dispatch Workflow'
$Ref = 'aux/example-branch'

function Invoke-Wrapper {
    param(
        [switch]$DryRun,
        [Alias('Input')]
        [string[]]$WorkflowInput = @()
    )

    $Arguments = @(
        '-NoProfile',
        '-File', $Wrapper,
        '-Repository', $Repository,
        '-Workflow', $Workflow,
        '-Ref', $Ref,
        '-HeadBranch', $Ref,
        '-HeadSha', $ExpectedSha
    )
    if ($WorkflowInput.Count -gt 1) {
        throw 'Test harness accepts at most one CLI-style -Input value per child pwsh invocation.'
    }
    if ($WorkflowInput.Count -eq 1) {
        $Arguments += @('-Input', $WorkflowInput[0])
    }
    if ($DryRun) {
        $Arguments += '-DryRun'
    }

    $Output = @(& pwsh @Arguments 2>&1)
    return [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output = $Output -join "`n"
    }
}

try {
    New-Item -ItemType Directory -Path $FakeBin -Force | Out-Null

    $FakeGh = @'
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Arguments = @($args)
if ($Arguments.Count -lt 1) { exit 90 }

if ($Arguments[0] -eq 'api') {
    if ($Arguments.Count -lt 2) { exit 91 }
    $Endpoint = [string]$Arguments[1]

    if ($Endpoint -like 'repos/*/commits/*') {
        Write-Output $env:MIMIR_FAKE_RESOLVED_SHA
        exit 0
    }

    if ($Endpoint -like 'repos/*/actions/runs?*') {
        $Runs = @()
        if (
            $env:MIMIR_FAKE_ACTIVE_MODE -eq 'active' -and
            $Endpoint -like '*status=in_progress*'
        ) {
            $Runs = @(
                [ordered]@{
                    id = 424242
                    workflow_id = 777
                    name = $env:MIMIR_FAKE_WORKFLOW
                    path = '.github/workflows/example.yml'
                    status = 'in_progress'
                    event = 'workflow_dispatch'
                    head_branch = $env:MIMIR_FAKE_BRANCH
                    head_sha = $env:MIMIR_FAKE_EXPECTED_SHA
                    html_url = 'https://example.invalid/run/424242'
                    created_at = '2026-08-21T00:00:00Z'
                }
            )
        }

        [ordered]@{ workflow_runs = $Runs } | ConvertTo-Json -Depth 6
        exit 0
    }

    exit 92
}

if ($Arguments.Count -ge 2 -and $Arguments[0] -eq 'workflow' -and $Arguments[1] -eq 'run') {
    Add-Content -LiteralPath $env:MIMIR_FAKE_LOG -Value ($Arguments -join ' ')
    exit 0
}

exit 93
'@

    Set-Content -LiteralPath (Join-Path $FakeBin 'gh.ps1') -Value $FakeGh -Encoding utf8NoBOM
    $env:PATH = $FakeBin + [System.IO.Path]::PathSeparator + $OldPath
    $env:MIMIR_FAKE_LOG = $LogPath
    $env:MIMIR_FAKE_EXPECTED_SHA = $ExpectedSha
    $env:MIMIR_FAKE_RESOLVED_SHA = $ExpectedSha
    $env:MIMIR_FAKE_WORKFLOW = $Workflow
    $env:MIMIR_FAKE_BRANCH = $Ref
    $env:MIMIR_FAKE_ACTIVE_MODE = 'none'

    $Dry = Invoke-Wrapper -DryRun
    if ($Dry.ExitCode -ne 0 -or $Dry.Output -notlike '*"dispatch_ready": true*') {
        throw "Dry-run readiness failed. Exit=$($Dry.ExitCode) Output=$($Dry.Output)"
    }
    if (Test-Path -LiteralPath $LogPath) {
        throw 'Dry-run must not invoke gh workflow run.'
    }

    $Dispatch = Invoke-Wrapper -Input @('mode=test')
    if ($Dispatch.ExitCode -ne 0 -or $Dispatch.Output -notlike '*"dispatched": true*') {
        throw "Unique dispatch failed. Exit=$($Dispatch.ExitCode) Output=$($Dispatch.Output)"
    }
    $DispatchLines = @(Get-Content -LiteralPath $LogPath)
    if ($DispatchLines.Count -ne 1) {
        throw "Expected exactly one gh workflow run invocation, found $($DispatchLines.Count)."
    }
    if ($DispatchLines[0] -notlike '*-f mode=test*') {
        throw "Workflow input was not forwarded exactly: $($DispatchLines[0])"
    }

    Remove-Item -LiteralPath $LogPath -Force
    $env:MIMIR_FAKE_ACTIVE_MODE = 'active'
    $Blocked = Invoke-Wrapper
    if ($Blocked.ExitCode -ne 3 -or $Blocked.Output -notlike '*"equivalent_active_run": true*') {
        throw "Equivalent active run should block dispatch with exit 3. Exit=$($Blocked.ExitCode) Output=$($Blocked.Output)"
    }
    if (Test-Path -LiteralPath $LogPath) {
        throw 'Blocked duplicate must not invoke gh workflow run.'
    }

    $env:MIMIR_FAKE_ACTIVE_MODE = 'none'
    $env:MIMIR_FAKE_RESOLVED_SHA = $OtherSha
    $Drift = Invoke-Wrapper
    if ($Drift.ExitCode -eq 0 -or $Drift.Output -notlike '*Workflow dispatch ref drift*') {
        throw "Ref/SHA drift should fail closed. Exit=$($Drift.ExitCode) Output=$($Drift.Output)"
    }
    if (Test-Path -LiteralPath $LogPath) {
        throw 'Ref/SHA drift must fail before gh workflow run.'
    }

    $env:MIMIR_FAKE_RESOLVED_SHA = $ExpectedSha
    $BadInput = Invoke-Wrapper -Input @('missing-equals')
    if ($BadInput.ExitCode -eq 0 -or $BadInput.Output -notlike '*name=value*') {
        throw "Malformed workflow input should fail closed. Exit=$($BadInput.ExitCode) Output=$($BadInput.Output)"
    }
    if (Test-Path -LiteralPath $LogPath) {
        throw 'Malformed workflow input must fail before gh workflow run.'
    }

    Write-Host 'PASS: unique workflow dispatch wrapper contract tests.'
}
finally {
    $env:PATH = $OldPath
    Remove-Item Env:MIMIR_FAKE_LOG -ErrorAction SilentlyContinue
    Remove-Item Env:MIMIR_FAKE_EXPECTED_SHA -ErrorAction SilentlyContinue
    Remove-Item Env:MIMIR_FAKE_RESOLVED_SHA -ErrorAction SilentlyContinue
    Remove-Item Env:MIMIR_FAKE_WORKFLOW -ErrorAction SilentlyContinue
    Remove-Item Env:MIMIR_FAKE_BRANCH -ErrorAction SilentlyContinue
    Remove-Item Env:MIMIR_FAKE_ACTIVE_MODE -ErrorAction SilentlyContinue

    if (Test-Path -LiteralPath $ScratchRoot) {
        Remove-Item -LiteralPath $ScratchRoot -Recurse -Force
    }
}
