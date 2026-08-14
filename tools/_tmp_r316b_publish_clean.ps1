$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$baseSha = "fc020729396ad9f62ee4b8fd8fe6808f5bdb5489"
$candidateBranch = "candidate/r3-16b-property-header-clean"
$patchSource = Join-Path $repoRoot "tools/_tmp_r316b_property_header.patch"
$testSource = Join-Path $repoRoot "crates/mimir-replay/tests/_tmp_r316b_property_header.rs"
$patchCopy = Join-Path $env:RUNNER_TEMP "r316b_property_header.patch"
$testCopy = Join-Path $env:RUNNER_TEMP "r316b_property_header.rs"

Copy-Item -LiteralPath $patchSource -Destination $patchCopy -Force
Copy-Item -LiteralPath $testSource -Destination $testCopy -Force

$existing = git ls-remote --heads origin "refs/heads/$candidateBranch"
if ($LASTEXITCODE -ne 0) { throw "failed to query candidate branch" }
if ($existing) { throw "candidate branch already exists: $candidateBranch" }

# Disposable verification runs intentionally mutate tracked test/source files via cargo fmt and the
# semantic production patch. Everything needed for clean reconstruction is already preserved in
# RUNNER_TEMP, so discard that disposable working-tree state before crossing to the canonical base.
git reset --hard HEAD
if ($LASTEXITCODE -ne 0) { throw "failed to reset disposable working tree" }
git clean -fd
if ($LASTEXITCODE -ne 0) { throw "failed to clean disposable working tree" }

git fetch --no-tags origin $baseSha
if ($LASTEXITCODE -ne 0) { throw "failed to fetch canonical R3.16B base $baseSha" }
git checkout --detach $baseSha
if ($LASTEXITCODE -ne 0) { throw "failed to detach at canonical base" }
git checkout -b $candidateBranch
if ($LASTEXITCODE -ne 0) { throw "failed to create clean candidate branch" }

$sourcePath = Join-Path $repoRoot "crates/mimir-replay/src/lib.rs"
$marker = 'fn network_lookup_plan_error(category: &str, detail: impl Into<String>) -> MimirError {'
$source = Get-Content -Raw $sourcePath
$first = $source.IndexOf($marker, [System.StringComparison]::Ordinal)
if ($first -lt 0) { throw "R3.16B clean insertion marker is missing" }
$second = $source.IndexOf($marker, $first + $marker.Length, [System.StringComparison]::Ordinal)
if ($second -ge 0) { throw "R3.16B clean insertion marker is not unique" }

$additionLines = Get-Content $patchCopy |
    Where-Object { ($_ -match '^\+') -and ($_ -notmatch '^\+\+\+') } |
    ForEach-Object { $_.Substring(1) }
if ($additionLines.Count -lt 100) { throw "R3.16B clean patch payload is unexpectedly small" }
$addition = ($additionLines -join "`n") + "`n`n"
$patched = $source.Substring(0, $first) + $addition + $source.Substring($first)
Set-Content -NoNewline -Encoding utf8 $sourcePath $patched

$permanentTest = Join-Path $repoRoot "crates/mimir-replay/tests/r3_16b_property_header.rs"
$permanentTestDir = Split-Path -Parent $permanentTest
New-Item -ItemType Directory -Force $permanentTestDir | Out-Null
Copy-Item -LiteralPath $testCopy -Destination $permanentTest -Force

cargo fmt --all
if ($LASTEXITCODE -ne 0) { throw "clean candidate rustfmt failed" }

# Stage exactly the intended production/test files before path accounting. The permanent test is a
# new file on the canonical base, so an unstaged `git diff` would deliberately omit it.
git add -- crates/mimir-replay/src/lib.rs crates/mimir-replay/tests/r3_16b_property_header.rs
if ($LASTEXITCODE -ne 0) { throw "clean candidate staging failed" }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "clean candidate staged diff check failed" }

$changed = @(git diff --cached --name-only $baseSha --)
$expected = @(
    "crates/mimir-replay/src/lib.rs",
    "crates/mimir-replay/tests/r3_16b_property_header.rs"
)
if ($changed.Count -ne $expected.Count) {
    throw "clean candidate changed unexpected path count: $($changed -join ', ')"
}
foreach ($path in $expected) {
    if ($changed -notcontains $path) { throw "clean candidate missing expected path: $path" }
}

$sourceHash = (Get-FileHash -Algorithm SHA256 $sourcePath).Hash.ToLowerInvariant()
if ($sourceHash -ne "186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28") {
    throw "clean candidate source hash drift: $sourceHash"
}

# Run the focused package gate before publishing the branch. The canonical branch workflows will
# still run independently after the push.
cargo test --locked -p mimir-replay --test r3_16b_property_header -- --nocapture
if ($LASTEXITCODE -ne 0) { throw "clean candidate focused tests failed" }

# Focused testing must not introduce additional tracked changes outside the staged two-file set.
$unstaged = @(git diff --name-only --)
if ($unstaged.Count -ne 0) {
    throw "clean candidate focused test introduced unstaged changes: $($unstaged -join ', ')"
}
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "clean candidate staged diff drifted after focused test" }

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git commit -m "Implement R3.16B existing-actor property header"
if ($LASTEXITCODE -ne 0) { throw "clean candidate commit failed" }
$candidateSha = (git rev-parse HEAD).Trim()

git push origin "HEAD:refs/heads/$candidateBranch"
if ($LASTEXITCODE -ne 0) { throw "clean candidate push failed" }

Write-Host "R3_16B_CLEAN_CANDIDATE_BRANCH=$candidateBranch"
Write-Host "R3_16B_CLEAN_CANDIDATE_SHA=$candidateSha"
Write-Host "R3_16B_CLEAN_SOURCE_SHA256=$sourceHash"
Write-Host "R3_16B_CLEAN_CANDIDATE=PASS"
