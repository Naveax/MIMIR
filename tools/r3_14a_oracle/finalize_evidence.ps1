[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$BoxcarsSha = 'c70e77df7af81b436cb545d070bb90c82f562d0b'
$ProductionCodeSha = 'ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa'
$SelectorManifestSha256 = '28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55'

foreach ($path in @(
    'r3_14a_supported.tsv',
    'r3_14a_oracle.log',
    'r3_14a_oracle_identity.txt',
    'r3_14a_effective_driver_sha256.txt'
)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "missing R3.14A finalizer input: $path" }
}

$identity = @{}
foreach ($line in Get-Content -LiteralPath 'r3_14a_oracle_identity.txt') {
    if ($line -match '^([^=]+)=(.*)$') { $identity[$Matches[1]] = $Matches[2] }
}
$driverIdentity = @{}
foreach ($line in Get-Content -LiteralPath 'r3_14a_effective_driver_sha256.txt') {
    if ($line -match '^([^=]+)=(.*)$') { $driverIdentity[$Matches[1]] = $Matches[2] }
}
if ($identity['boxcars_sha'] -ne $BoxcarsSha) { throw 'oracle identity file Boxcars SHA mismatch' }
if (-not $identity.ContainsKey('instrumentation_patch_sha256')) { throw 'missing instrumentation patch SHA-256' }
if (-not $driverIdentity.ContainsKey('effective_driver_sha256')) { throw 'missing effective driver SHA-256' }

$selectorRows = @(Get-Content -LiteralPath 'r3_14a_supported.tsv' | Where-Object { $_ -match '^SUPPORTED\t' })
if ($selectorRows.Count -ne 47) { throw "expected 47 selector rows, got $($selectorRows.Count)" }
$selectorByPath = @{}
foreach ($row in $selectorRows) {
    $p = $row -split "`t"
    if ($p.Count -ne 10) { throw "selector schema drift: $row" }
    $record = [ordered]@{
        corpus_index = [int]$p[1]
        relative_path = $p[2]
        byte_length = [int64]$p[3]
        sha256 = $p[4]
        build_version = $p[5]
        network_start = [int64]$p[6]
        network_size = [int64]$p[7]
        max_channels = [int]$p[8]
        channel_bits = [int]$p[9]
    }
    if ($selectorByPath.ContainsKey($record.relative_path)) { throw "duplicate selector path: $($record.relative_path)" }
    $selectorByPath[$record.relative_path] = $record
}
if (@($selectorByPath.Values.sha256 | Sort-Object -Unique).Count -ne 47) { throw 'selector SHA uniqueness drift' }

$evidenceLines = @(Get-Content -LiteralPath 'r3_14a_oracle.log' | Where-Object { $_ -match '^R3_14A_EVIDENCE\t' })
$parsePassCount = @(Get-Content -LiteralPath 'r3_14a_oracle.log' | Where-Object { $_ -eq 'R3_14A_ORACLE_PARSE=PASS' }).Count
if ($evidenceLines.Count -ne 47) { throw "expected 47 evidence rows, got $($evidenceLines.Count)" }
if ($parsePassCount -ne 47) { throw "expected 47 oracle parse PASS rows, got $parsePassCount" }

$actorIds = [System.Collections.Generic.List[int]]::new()
$actorBits = [System.Collections.Generic.List[int]]::new()
$actorPresentTrue = 0
$actorPresentFalse = 0
$aliveTrue = 0
$aliveFalse = 0
$newTrue = 0
$newFalse = 0
$extraDiscriminator = 0
$nonFiniteTime = 0
$nonFiniteDelta = 0
$zeroZeroTerminal = 0
$terminalRows = 0
$schemaErrors = 0
$monotonicityFailures = 0
$outputRows = [System.Collections.Generic.List[object]]::new()

foreach ($line in $evidenceLines) {
    $fields = @{}
    foreach ($part in (($line -split "`t") | Select-Object -Skip 1)) {
        $kv = $part -split '=', 2
        if ($kv.Count -ne 2 -or $fields.ContainsKey($kv[0])) { throw "evidence schema error: $line" }
        $fields[$kv[0]] = $kv[1]
    }
    if (-not $selectorByPath.ContainsKey($fields['label'])) { throw "evidence label not in supported selector: $($fields['label'])" }
    $selector = $selectorByPath[$fields['label']]

    $time = [single]::Parse($fields['time_f32'], [Globalization.CultureInfo]::InvariantCulture)
    $delta = [single]::Parse($fields['delta_f32'], [Globalization.CultureInfo]::InvariantCulture)
    if ([single]::IsNaN($time) -or [single]::IsInfinity($time)) { $nonFiniteTime++ }
    if ([single]::IsNaN($delta) -or [single]::IsInfinity($delta)) { $nonFiniteDelta++ }
    if ($time -eq 0.0 -and $delta -eq 0.0) { $zeroZeroTerminal++ }
    if ($fields['terminal'] -eq 'true') { $terminalRows++ }

    $frameStart = [int64]$fields['frame_start_bit']
    $afterTiming = [int64]$fields['bit_after_time_delta']
    $stopBit = [int64]$fields['first_actor_header_end_bit']
    if ($frameStart -lt 0 -or $afterTiming -ne ($frameStart + 64) -or $stopBit -lt $afterTiming) { $monotonicityFailures++ }

    $actorIdObject = $null
    $aliveValue = $null
    $newValue = $null
    $actorPresent = $fields['actor_present'] -eq 'true'
    if ($actorPresent) {
        $actorPresentTrue++
        $actorId = [int]$fields['actor_id_value']
        $actorIdStart = [int64]$fields['actor_id_start_bit']
        $actorIdEnd = [int64]$fields['actor_id_end_bit']
        $actorIdBits = [int]$fields['actor_id_bits_consumed']
        $actorIds.Add($actorId)
        $actorBits.Add($actorIdBits)
        if ($actorId -lt 0 -or $actorId -ge $selector.max_channels) { $schemaErrors++ }
        if ($actorIdBits -ne $selector.channel_bits -and $actorIdBits -ne ($selector.channel_bits + 1)) { $schemaErrors++ }
        $discriminator = $null
        if ($fields['actor_id_discriminator'] -ne 'null') {
            $discriminator = [int]$fields['actor_id_discriminator']
            $extraDiscriminator++
            if ($discriminator -ne 0 -and $discriminator -ne 1) { $schemaErrors++ }
        }
        $actorIdObject = [ordered]@{
            bound = [int]$selector.max_channels
            low_bit_width = [int]$selector.channel_bits
            start_bit = $actorIdStart
            end_bit = $actorIdEnd
            bits_consumed = $actorIdBits
            extra_discriminator_consumed = $fields['actor_id_discriminator'] -ne 'null'
            extra_discriminator_value = $discriminator
            value = $actorId
        }

        if ($fields['alive'] -eq 'true') {
            $aliveTrue++
            $aliveValue = $true
            if ($fields['new'] -eq 'true') { $newTrue++; $newValue = $true }
            elseif ($fields['new'] -eq 'false') { $newFalse++; $newValue = $false }
            else { $schemaErrors++ }
        }
        elseif ($fields['alive'] -eq 'false') {
            $aliveFalse++
            $aliveValue = $false
            if ($fields['new'] -ne 'null') { $schemaErrors++ }
        }
        else { $schemaErrors++ }
    }
    elseif ($fields['actor_present'] -eq 'false') {
        $actorPresentFalse++
    }
    else { $schemaErrors++ }

    $outputRows.Add([ordered]@{
        schema = 'mimir.r3_14a.first_actor_envelope.v1'
        mimir_evidence_head = $env:GITHUB_SHA
        production_code_sha = $ProductionCodeSha
        oracle_repo = 'nickbabcock/boxcars'
        oracle_sha = $BoxcarsSha
        instrumentation_patch_sha256 = $identity['instrumentation_patch_sha256']
        effective_driver_sha256 = $driverIdentity['effective_driver_sha256']
        selector_manifest_sha256 = $SelectorManifestSha256
        corpus_index = $selector.corpus_index
        relative_path = $selector.relative_path
        byte_length = $selector.byte_length
        sha256 = $selector.sha256
        production_support_status = $true
        build_version = $selector.build_version
        network_start = $selector.network_start
        network_size = $selector.network_size
        max_channels = $selector.max_channels
        channel_bits = $selector.channel_bits
        frame_start_bit = $frameStart
        time_raw_u32 = [uint32]$fields['time_raw_u32']
        time = $time
        delta_raw_u32 = [uint32]$fields['delta_raw_u32']
        delta = $delta
        bit_after_time_delta = $afterTiming
        actor_present_bit_offset = if ($fields['actor_present_bit_offset'] -eq 'null') { $null } else { [int64]$fields['actor_present_bit_offset'] }
        actor_present = $actorPresent
        actor_id = $actorIdObject
        alive_bit_offset = if ($fields['alive_bit_offset'] -eq 'null') { $null } else { [int64]$fields['alive_bit_offset'] }
        alive = $aliveValue
        new_bit_offset = if ($fields['new_bit_offset'] -eq 'null') { $null } else { [int64]$fields['new_bit_offset'] }
        new = $newValue
        stop_bit = $stopBit
        terminal = $fields['terminal'] -eq 'true'
    })
}

if (@($outputRows.relative_path | Sort-Object -Unique).Count -ne 47) { throw 'final evidence path uniqueness drift' }
if (@($outputRows.sha256 | Sort-Object -Unique).Count -ne 47) { throw 'final evidence SHA uniqueness drift' }
if ($schemaErrors -ne 0 -or $monotonicityFailures -ne 0 -or $nonFiniteTime -ne 0 -or $nonFiniteDelta -ne 0 -or $zeroZeroTerminal -ne 0 -or $terminalRows -ne 0) {
    throw "spec aggregate gate failed: schema=$schemaErrors monotonicity=$monotonicityFailures nonfinite_time=$nonFiniteTime nonfinite_delta=$nonFiniteDelta zerozero=$zeroZeroTerminal terminal=$terminalRows"
}

$outputRows | ForEach-Object { $_ | ConvertTo-Json -Depth 8 -Compress } | Set-Content -LiteralPath 'r3_14a_first_actor_envelope.jsonl' -Encoding utf8NoBOM

$summary = [ordered]@{
    schema = 'mimir.r3_14a.summary.v1'
    mimir_evidence_head = $env:GITHUB_SHA
    production_code_sha = $ProductionCodeSha
    oracle_repo = 'nickbabcock/boxcars'
    oracle_sha = $BoxcarsSha
    instrumentation_patch_sha256 = $identity['instrumentation_patch_sha256']
    effective_driver_sha256 = $driverIdentity['effective_driver_sha256']
    selector_manifest_sha256 = $SelectorManifestSha256
    replays_total = 47
    replays_unique_sha = 47
    oracle_parse_success = $parsePassCount
    first_frame_rows = $evidenceLines.Count
    actor_present_true = $actorPresentTrue
    actor_present_false = $actorPresentFalse
    alive_true = $aliveTrue
    alive_false = $aliveFalse
    new_true = $newTrue
    new_false = $newFalse
    bounded_actor_id_rows = $actorIds.Count
    min_actor_id = if ($actorIds.Count) { ($actorIds | Measure-Object -Minimum).Minimum } else { $null }
    max_actor_id = if ($actorIds.Count) { ($actorIds | Measure-Object -Maximum).Maximum } else { $null }
    min_actor_id_bits_consumed = if ($actorBits.Count) { ($actorBits | Measure-Object -Minimum).Minimum } else { $null }
    max_actor_id_bits_consumed = if ($actorBits.Count) { ($actorBits | Measure-Object -Maximum).Maximum } else { $null }
    extra_discriminator_consumed_count = $extraDiscriminator
    non_finite_time_count = $nonFiniteTime
    non_finite_delta_count = $nonFiniteDelta
    zero_zero_terminal_first_frame_count = $zeroZeroTerminal
    terminal_first_frame_rows = $terminalRows
    schema_errors = $schemaErrors
    bit_offset_monotonicity_failures = $monotonicityFailures
    production_source_mutation = 0
    hard_stop = 'after actor_present; conditional actor_id/alive/new; before name_id/object_id/spawn/property payload'
    outcome_candidate = 'A'
    next_pass_candidate = 'R3.14B'
}
$summary | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath 'r3_14a_summary.json' -Encoding utf8NoBOM

@(
    'R3.14A spec-complete aggregate',
    "mimir_evidence_head=$($summary.mimir_evidence_head)",
    "production_code_sha=$ProductionCodeSha",
    "oracle_sha=$BoxcarsSha",
    "selector_manifest_sha256=$SelectorManifestSha256",
    "instrumentation_patch_sha256=$($summary.instrumentation_patch_sha256)",
    "effective_driver_sha256=$($summary.effective_driver_sha256)",
    'replays_total=47',
    'replays_unique_sha=47',
    "oracle_parse_success=$($summary.oracle_parse_success)",
    "first_frame_rows=$($summary.first_frame_rows)",
    "actor_present_true=$actorPresentTrue",
    "actor_present_false=$actorPresentFalse",
    "alive_true=$aliveTrue",
    "alive_false=$aliveFalse",
    "new_true=$newTrue",
    "new_false=$newFalse",
    "bounded_actor_id_rows=$($summary.bounded_actor_id_rows)",
    "min_actor_id=$($summary.min_actor_id)",
    "max_actor_id=$($summary.max_actor_id)",
    "min_actor_id_bits_consumed=$($summary.min_actor_id_bits_consumed)",
    "max_actor_id_bits_consumed=$($summary.max_actor_id_bits_consumed)",
    "extra_discriminator_consumed_count=$extraDiscriminator",
    'non_finite_time_count=0',
    'non_finite_delta_count=0',
    'zero_zero_terminal_first_frame_count=0',
    'terminal_first_frame_rows=0',
    'schema_errors=0',
    'bit_offset_monotonicity_failures=0',
    'production_source_mutation=0',
    'outcome_candidate=A',
    'next_pass_candidate=R3.14B',
    'R3_14A_SPEC_EVIDENCE=PASS'
) | Set-Content -LiteralPath 'r3_14a_spec_aggregate.txt' -Encoding utf8NoBOM

Get-Content -LiteralPath 'r3_14a_spec_aggregate.txt' | ForEach-Object { Write-Host $_ }
