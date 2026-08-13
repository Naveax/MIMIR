[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProductionCodeSha = 'ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa'
$BoxcarsSha = 'c70e77df7af81b436cb545d070bb90c82f562d0b'
$BoxcarsFrameDecoderBlob = '6f2ff153d3a27cdacccc65e3f23851489077a7d8'
$BoxcarsBitsBlob = 'd3ca061580e5e78038b2af383ff53971001c91c9'
$SelectorManifestSha256 = '28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55'

function Invoke-NativeChecked {
    param(
        [Parameter(Mandatory)] [scriptblock] $Command,
        [Parameter(Mandatory)] [string] $Label
    )
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with native exit code $LASTEXITCODE"
    }
}

function Get-NativeLines {
    param(
        [Parameter(Mandatory)] [scriptblock] $Command,
        [Parameter(Mandatory)] [string] $Label
    )
    $lines = @(& $Command 2>&1 | ForEach-Object { $_.ToString() })
    $native = $LASTEXITCODE
    if ($native -ne 0) {
        $lines | ForEach-Object { Write-Host $_ }
        throw "$Label failed with native exit code $native"
    }
    return $lines
}

$head = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw "git rev-parse HEAD failed: $LASTEXITCODE" }
if ($env:GITHUB_SHA -and $head -ne $env:GITHUB_SHA) {
    throw "checkout SHA mismatch: head=$head github=$env:GITHUB_SHA"
}
Write-Host "R3_14A_MIMIR_EVIDENCE_HEAD=$head"

Invoke-NativeChecked -Label 'fetch exact production baseline' -Command {
    & git fetch origin $ProductionCodeSha --depth=1
}
$productionDrift = @(& git diff --name-only $ProductionCodeSha HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus)
if ($LASTEXITCODE -ne 0) { throw "production tree diff failed: $LASTEXITCODE" }
if ($productionDrift.Count -ne 0) {
    $productionDrift | ForEach-Object { Write-Host "PRODUCTION_DRIFT $_" }
    throw "R3.14A evidence branch mutated admitted production/corpus tree"
}
Write-Host "R3_14A_PRODUCTION_TREE_IMMUTABLE=PASS"

$selector = Get-NativeLines -Label 'R3.14A selector' -Command {
    & cargo run --manifest-path tools/r3_14a_selector/Cargo.toml --quiet
}
$selector | Set-Content -Encoding utf8 r3_14a_selector_for_oracle.log
$supported = @($selector | Where-Object { $_ -match '^SUPPORTED\t' })
if ($supported.Count -ne 47) { throw "expected 47 supported selector rows, got $($supported.Count)" }
$selectorText = $selector -join "`n"
foreach ($marker in @(
    'SUMMARY total_replays=103',
    'SUMMARY supported_replays=47',
    'SUMMARY unsupported_replays=56',
    'SUMMARY unique_supported_sha256=47',
    "SUMMARY manifest_sha256=$SelectorManifestSha256",
    'R3_14A_SELECTOR=PASS'
)) {
    if (-not $selectorText.Contains($marker)) { throw "missing selector marker: $marker" }
}
$supported | Set-Content -Encoding utf8 r3_14a_supported.tsv
Write-Host "R3_14A_SELECTOR_IDENTITY=PASS"

$boxcars = Join-Path $env:RUNNER_TEMP 'boxcars-r3-14a-v2'
Invoke-NativeChecked -Label 'Boxcars clone' -Command {
    & git clone --quiet https://github.com/nickbabcock/boxcars.git $boxcars
}
Invoke-NativeChecked -Label 'Boxcars exact checkout' -Command {
    & git -C $boxcars checkout --quiet --detach $BoxcarsSha
}
$oracleHead = (& git -C $boxcars rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $oracleHead -ne $BoxcarsSha) { throw "Boxcars pin mismatch: $oracleHead" }
$oracleDirty = @(& git -C $boxcars status --porcelain)
if ($LASTEXITCODE -ne 0 -or $oracleDirty.Count -ne 0) { throw "Boxcars tree not clean before instrumentation" }
$frameBlob = (& git -C $boxcars hash-object src/network/frame_decoder.rs).Trim()
$bitsBlob = (& git -C $boxcars hash-object src/bits.rs).Trim()
if ($frameBlob -ne $BoxcarsFrameDecoderBlob) { throw "frame_decoder blob mismatch: $frameBlob" }
if ($bitsBlob -ne $BoxcarsBitsBlob) { throw "bits blob mismatch: $bitsBlob" }
@(
    "boxcars_sha=$oracleHead",
    "frame_decoder_blob=$frameBlob",
    "bits_blob=$bitsBlob",
    'prepatch_tree_clean=true'
) | Set-Content -Encoding utf8 r3_14a_oracle_identity.txt
Write-Host "R3_14A_ORACLE_PIN=PASS"

Invoke-NativeChecked -Label 'Boxcars observation patch' -Command {
    & python tools/r3_14a_oracle/patch_boxcars.py $boxcars
}
Invoke-NativeChecked -Label 'Boxcars probe intent-to-add' -Command {
    & git -C $boxcars add -N examples/r3_14a_probe.rs
}
Invoke-NativeChecked -Label 'Boxcars instrumentation format' -Command {
    & cargo fmt --manifest-path (Join-Path $boxcars 'Cargo.toml') --all
}
Invoke-NativeChecked -Label 'Boxcars instrumentation diff-check' -Command {
    & git -C $boxcars diff --check
}
$oracleChanged = @(& git -C $boxcars diff --name-only)
if ($LASTEXITCODE -ne 0) { throw "Boxcars changed-path query failed: $LASTEXITCODE" }
$expectedOracleChanged = @('examples/r3_14a_probe.rs', 'src/network/frame_decoder.rs')
if ((Compare-Object $expectedOracleChanged $oracleChanged).Count -ne 0) {
    $oracleChanged | ForEach-Object { Write-Host "ORACLE_CHANGED $_" }
    throw "instrumentation changed unexpected Boxcars paths"
}

$patchLines = @(& git -C $boxcars diff --binary -- examples/r3_14a_probe.rs src/network/frame_decoder.rs)
if ($LASTEXITCODE -ne 0) { throw "Boxcars instrumentation patch capture failed: $LASTEXITCODE" }
$patchLines | Set-Content -Encoding utf8 r3_14a_boxcars_instrumentation.patch
$patchSha = (Get-FileHash -Algorithm SHA256 r3_14a_boxcars_instrumentation.patch).Hash.ToLowerInvariant()
"instrumentation_patch_sha256=$patchSha" | Add-Content -Encoding utf8 r3_14a_oracle_identity.txt
$oracleChanged | ForEach-Object { "instrumented_path=$_" } | Add-Content -Encoding utf8 r3_14a_oracle_identity.txt
Write-Host "R3_14A_ORACLE_PATCH_SHA256=$patchSha"

Invoke-NativeChecked -Label 'instrumented Boxcars example check' -Command {
    & cargo check --manifest-path (Join-Path $boxcars 'Cargo.toml') --example r3_14a_probe
}
Invoke-NativeChecked -Label 'instrumented Boxcars library tests' -Command {
    & cargo test --manifest-path (Join-Path $boxcars 'Cargo.toml') --lib --quiet
}
Invoke-NativeChecked -Label 'instrumented Boxcars probe build' -Command {
    & cargo build --manifest-path (Join-Path $boxcars 'Cargo.toml') --example r3_14a_probe --quiet
}
Write-Host "R3_14A_ORACLE_INSTRUMENTATION_BUILD=PASS"

$probe = Join-Path $boxcars 'target\debug\examples\r3_14a_probe.exe'
if (-not (Test-Path -LiteralPath $probe)) { throw "missing oracle probe executable: $probe" }
Remove-Item r3_14a_oracle.log -ErrorAction SilentlyContinue
foreach ($row in $supported) {
    $parts = $row -split "`t"
    if ($parts.Count -ne 10) { throw "selector row schema drift: $row" }
    $relative = $parts[2]
    $resolved = (Resolve-Path -LiteralPath $relative).Path
    $env:MIMIR_R3_14A_OBSERVE = '1'
    $env:MIMIR_R3_14A_LABEL = $relative
    $lines = @(& $probe $resolved 2>&1 | ForEach-Object { $_.ToString() })
    $native = $LASTEXITCODE
    "INPUT`t$relative" | Add-Content -Encoding utf8 r3_14a_oracle.log
    $lines | Add-Content -Encoding utf8 r3_14a_oracle.log
    if ($native -ne 0) {
        $lines | ForEach-Object { Write-Host $_ }
        throw "pinned Boxcars parse failed for $relative with exit $native"
    }
    if (@($lines | Where-Object { $_ -match '^R3_14A_EVIDENCE\t' }).Count -ne 1) {
        throw "expected exactly one first-frame evidence row for $relative"
    }
    if (@($lines | Where-Object { $_ -eq 'R3_14A_ORACLE_PARSE=PASS' }).Count -ne 1) {
        throw "missing oracle parse PASS for $relative"
    }
}
Remove-Item Env:MIMIR_R3_14A_OBSERVE -ErrorAction SilentlyContinue
Remove-Item Env:MIMIR_R3_14A_LABEL -ErrorAction SilentlyContinue
Write-Host "R3_14A_ORACLE_PARSE_LOOP=PASS"

$evidence = @(Get-Content r3_14a_oracle.log | Where-Object { $_ -match '^R3_14A_EVIDENCE\t' })
$parsePass = @(Get-Content r3_14a_oracle.log | Where-Object { $_ -eq 'R3_14A_ORACLE_PARSE=PASS' })
if ($evidence.Count -ne 47) { throw "expected 47 evidence rows, got $($evidence.Count)" }
if ($parsePass.Count -ne 47) { throw "expected 47 oracle parse PASS rows, got $($parsePass.Count)" }

$selectorByPath = @{}
foreach ($row in $supported) {
    $p = $row -split "`t"
    $selectorByPath[$p[2]] = [pscustomobject]@{
        Sha256 = $p[4]
        MaxChannels = [int]$p[8]
        ChannelBits = [int]$p[9]
    }
}

$records = @()
foreach ($line in $evidence) {
    $fields = @{}
    foreach ($part in (($line -split "`t") | Select-Object -Skip 1)) {
        $kv = $part -split '=', 2
        if ($kv.Count -ne 2 -or $fields.ContainsKey($kv[0])) { throw "evidence schema error: $line" }
        $fields[$kv[0]] = $kv[1]
    }
    $records += [pscustomobject]$fields
}

$required = @(
    'label','frame_start_bit','time_raw_u32','time_f32','delta_raw_u32','delta_f32',
    'bit_after_time_delta','actor_present_bit_offset','actor_present','actor_id_bound',
    'actor_id_start_bit','actor_id_value','actor_id_end_bit','actor_id_bits_consumed',
    'actor_id_discriminator','alive_bit_offset','alive','new_bit_offset','new',
    'first_actor_header_end_bit','terminal'
)
$schemaErrors = 0
$monotonicityFailures = 0
$nonFinite = 0
$zeroZero = 0
$terminalRows = 0
$actorPresentTrue = 0
$actorPresentFalse = 0
$aliveTrue = 0
$aliveFalse = 0
$newTrue = 0
$newFalse = 0
$discriminatorConsumed = 0

foreach ($r in $records) {
    foreach ($name in $required) {
        if ($null -eq $r.PSObject.Properties[$name]) { $schemaErrors++ }
    }
    if (-not $selectorByPath.ContainsKey($r.label)) { $schemaErrors++; continue }

    $frameStart = [int64]$r.frame_start_bit
    $afterTD = [int64]$r.bit_after_time_delta
    $headerEnd = [int64]$r.first_actor_header_end_bit
    if ($frameStart -lt 0 -or $afterTD -ne ($frameStart + 64) -or $headerEnd -lt $afterTD) { $monotonicityFailures++ }

    $time = [double]::Parse($r.time_f32, [Globalization.CultureInfo]::InvariantCulture)
    $delta = [double]::Parse($r.delta_f32, [Globalization.CultureInfo]::InvariantCulture)
    if ([double]::IsNaN($time) -or [double]::IsInfinity($time) -or [double]::IsNaN($delta) -or [double]::IsInfinity($delta)) { $nonFinite++ }
    if ($time -eq 0.0 -and $delta -eq 0.0) { $zeroZero++ }
    if ($r.terminal -eq 'true') { $terminalRows++ }

    if ($r.actor_present -eq 'true') {
        $actorPresentTrue++
        $selectorRecord = $selectorByPath[$r.label]
        if ([int]$r.actor_id_bound -ne $selectorRecord.MaxChannels) { $schemaErrors++ }
        $presentOffset = [int64]$r.actor_present_bit_offset
        $idStart = [int64]$r.actor_id_start_bit
        $idEnd = [int64]$r.actor_id_end_bit
        $aliveOffset = [int64]$r.alive_bit_offset
        $consumed = [int]$r.actor_id_bits_consumed
        $actorId = [int]$r.actor_id_value
        if ($presentOffset -ne $afterTD -or $idStart -ne ($presentOffset + 1) -or $idEnd -le $idStart -or $aliveOffset -ne $idEnd) { $monotonicityFailures++ }
        if ($actorId -lt 0 -or $actorId -ge $selectorRecord.MaxChannels) { $schemaErrors++ }
        if ($consumed -ne $selectorRecord.ChannelBits -and $consumed -ne ($selectorRecord.ChannelBits + 1)) { $schemaErrors++ }
        if ($consumed -eq ($selectorRecord.ChannelBits + 1)) {
            $discriminatorConsumed++
            if ($r.actor_id_discriminator -ne '0' -and $r.actor_id_discriminator -ne '1') { $schemaErrors++ }
        }
        elseif ($r.actor_id_discriminator -ne 'null') {
            $schemaErrors++
        }

        if ($r.alive -eq 'true') {
            $aliveTrue++
            $newOffset = [int64]$r.new_bit_offset
            if ($newOffset -ne ($aliveOffset + 1) -or $headerEnd -ne ($newOffset + 1)) { $monotonicityFailures++ }
            if ($r.new -eq 'true') { $newTrue++ }
            elseif ($r.new -eq 'false') { $newFalse++ }
            else { $schemaErrors++ }
        }
        elseif ($r.alive -eq 'false') {
            $aliveFalse++
            if ($r.new_bit_offset -ne 'null' -or $r.new -ne 'null' -or $headerEnd -ne ($aliveOffset + 1)) { $schemaErrors++ }
        }
        else {
            $schemaErrors++
        }
    }
    elseif ($r.actor_present -eq 'false') {
        $actorPresentFalse++
        $presentOffset = [int64]$r.actor_present_bit_offset
        if ($presentOffset -ne $afterTD -or $headerEnd -ne ($presentOffset + 1)) { $monotonicityFailures++ }
        foreach ($name in @('actor_id_bound','actor_id_start_bit','actor_id_value','actor_id_end_bit','actor_id_bits_consumed','actor_id_discriminator','alive_bit_offset','alive','new_bit_offset','new')) {
            if ($r.$name -ne 'null') { $schemaErrors++ }
        }
    }
    else {
        $schemaErrors++
    }
}

$uniqueLabels = @($records.label | Sort-Object -Unique).Count
if ($uniqueLabels -ne 47) { throw "expected 47 unique evidence labels, got $uniqueLabels" }
if ($nonFinite -ne 0 -or $zeroZero -ne 0 -or $terminalRows -ne 0 -or $schemaErrors -ne 0 -or $monotonicityFailures -ne 0) {
    throw "R3.14A aggregate failure: nonfinite=$nonFinite zerozero=$zeroZero terminal=$terminalRows schema=$schemaErrors monotonicity=$monotonicityFailures"
}

@(
    'R3.14A pinned oracle aggregate',
    "mimir_evidence_head=$head",
    "production_code_sha=$ProductionCodeSha",
    "boxcars_sha=$BoxcarsSha",
    "selector_manifest_sha256=$SelectorManifestSha256",
    'supported_replays=47',
    'unique_replay_sha256=47',
    'oracle_parse_success=47',
    'first_frame_rows=47',
    "actor_present_true=$actorPresentTrue",
    "actor_present_false=$actorPresentFalse",
    "alive_true=$aliveTrue",
    "alive_false=$aliveFalse",
    "new_true=$newTrue",
    "new_false=$newFalse",
    "actor_id_discriminator_consumed=$discriminatorConsumed",
    'nonfinite_time_delta=0',
    'zero_zero_first_frame=0',
    'terminal_first_frame_rows=0',
    'schema_errors=0',
    'bit_monotonicity_failures=0',
    'production_source_mutation=0',
    'R3_14A_ORACLE_EVIDENCE=PASS'
) | Set-Content -Encoding utf8 r3_14a_aggregate.txt
Get-Content r3_14a_aggregate.txt | ForEach-Object { Write-Host $_ }

$oracleHeadAfter = (& git -C $boxcars rev-parse HEAD).Trim()
if ($oracleHeadAfter -ne $BoxcarsSha) { throw "oracle HEAD drifted after parse: $oracleHeadAfter" }
$oracleChangedAfter = @(& git -C $boxcars diff --name-only)
if ((Compare-Object $expectedOracleChanged $oracleChangedAfter).Count -ne 0) { throw "oracle patch scope drifted after parse" }
$productionDriftAfter = @(& git diff --name-only $ProductionCodeSha HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus)
if ($LASTEXITCODE -ne 0 -or $productionDriftAfter.Count -ne 0) { throw "MIMIR production/corpus tree drifted during oracle pass" }
Write-Host "R3_14A_FINAL_SCOPE=PASS"
