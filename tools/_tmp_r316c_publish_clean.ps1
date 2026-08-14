$ErrorActionPreference = 'Stop'
$base = 'ebc0fa31ba90a8496c3d1719e436d2c17b605ff7'
$candidate = 'candidate/r3-16c-continuity-clean'
$allowed = @(
  'MIMIR_CONTINUE_HERE.md',
  'MIMIR_KNOWLEDGE_GRAPH.md',
  'docs/continuity/MIMIR_CONTINUITY_STATE.json',
  'docs/continuity/MIMIR_CURRENT_STATE.md',
  'docs/continuity/MIMIR_R3_16B_DECISION.md',
  'docs/continuity/MIMIR_R3_16C_EXECUTION_SPEC.md',
  'docs/continuity/MIMIR_R3_16C_DECISION.md',
  'docs/continuity/MIMIR_R3_17A_EXECUTION_SPEC.md'
) | Sort-Object

$changed = @(git status --porcelain | ForEach-Object { $_.Substring(3) } | Sort-Object)
if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
if (($changed -join "`n") -ne ($allowed -join "`n")) {
  Write-Host 'Expected:'; $allowed | ForEach-Object { Write-Host "  $_" }
  Write-Host 'Observed:'; $changed | ForEach-Object { Write-Host "  $_" }
  throw 'R3.16C post-validation scope drift'
}

git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R3.16C post-validation diff check failed' }

$stashRoot = Join-Path $env:RUNNER_TEMP 'r316c-clean'
Remove-Item -Recurse -Force $stashRoot -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $stashRoot | Out-Null
foreach ($rel in $allowed) {
  $src = Join-Path $PWD $rel
  if (-not (Test-Path -LiteralPath $src -PathType Leaf)) { throw "missing patched file: $rel" }
  $dst = Join-Path $stashRoot $rel
  New-Item -ItemType Directory -Force (Split-Path -Parent $dst) | Out-Null
  Copy-Item -LiteralPath $src -Destination $dst
}

git fetch origin main
if ($LASTEXITCODE -ne 0) { throw 'git fetch origin main failed' }
$freshMain = (git rev-parse origin/main).Trim()
if ($LASTEXITCODE -ne 0) { throw 'git rev-parse origin/main failed' }
if ($freshMain -ne $base) { throw "canonical main drifted: expected $base got $freshMain" }

git reset --hard $base
if ($LASTEXITCODE -ne 0) { throw 'git reset to canonical base failed' }
git clean -fd
if ($LASTEXITCODE -ne 0) { throw 'git clean failed' }
git switch -c $candidate $base
if ($LASTEXITCODE -ne 0) { throw 'candidate branch creation failed' }

foreach ($rel in $allowed) {
  $src = Join-Path $stashRoot $rel
  $dst = Join-Path $PWD $rel
  New-Item -ItemType Directory -Force (Split-Path -Parent $dst) | Out-Null
  Copy-Item -LiteralPath $src -Destination $dst
}

git add -- $allowed
if ($LASTEXITCODE -ne 0) { throw 'git add failed' }
$staged = @(git diff --cached --name-only | Sort-Object)
if ($LASTEXITCODE -ne 0) { throw 'staged path query failed' }
if (($staged -join "`n") -ne ($allowed -join "`n")) {
  Write-Host 'Expected staged:'; $allowed | ForEach-Object { Write-Host "  $_" }
  Write-Host 'Observed staged:'; $staged | ForEach-Object { Write-Host "  $_" }
  throw 'clean candidate staged scope mismatch'
}
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'clean candidate diff check failed' }

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git commit -m 'Close R3.16C continuity and open R3.17A'
if ($LASTEXITCODE -ne 0) { throw 'clean candidate commit failed' }
$candidateSha = (git rev-parse HEAD).Trim()
Write-Host "R3_16C_CANDIDATE_SHA=$candidateSha"

git push origin "HEAD:refs/heads/$candidate"
if ($LASTEXITCODE -ne 0) { throw 'clean candidate push failed' }
Write-Host 'R3_16C_CLEAN_PUBLISH=PASS'
