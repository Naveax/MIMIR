# MIMIR R3.14A — First Frame + First Actor Envelope Differential Evidence

**Pass ID:** R3.14A  
**Pass type:** evidence-only / oracle instrumentation / no production implementation  
**Production base:** `ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa` unless fresh repo truth shows a newer production milestone  
**Target corpus:** the 47 currently supported replays  
**Oracle:** already-pinned Boxcars revision used by the current differential evidence lineage

---

# 1. Purpose

R3.14A exists to prove the **bit cursor and field order at the very beginning of native network decoding** before MIMIR consumes those bits in production.

The pass must answer only this question:

> For every currently supported replay, can the pinned oracle expose a deterministic first-frame timing preamble and first actor-envelope header that gives us exact expected values and exact bit positions for the future native reader?

It is intentionally small because a single wrong bounded-integer bit can desynchronize the entire remaining network stream.

---

# 2. Production code policy

R3.14A MUST NOT modify production Rust code.

Forbidden production modifications include:

```text
crates/mimir-replay/src/lib.rs
Cargo.toml
Cargo.lock
any other crates/* source
README capability claims
production scripts used by normal CI
```

Allowed temporary work:

```text
temporary GitHub Actions workflow on evidence branch
temporary oracle instrumentation patch
temporary evidence collection scripts
temporary structured outputs/artifacts on evidence branch
```

Nothing temporary is automatically eligible for `main`.

---

# 3. Preflight — mandatory repository audit

Before touching the oracle:

```text
1. fetch fresh origin/main
2. record origin/main SHA
3. compare it to continuity state
4. inspect commits after ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
5. determine whether they are continuity-doc-only or production-code commits
6. if production code advanced beyond R3.13, STOP and repair continuity first
7. ensure working/evidence branch starts from fresh main
8. inspect current crates/mimir-replay/src/lib.rs network plan symbols
9. inspect relevant corpus/support tests
10. record supported replay selection mechanism used for the 47 replay lane
```

Required preflight artifact should include:

```text
repository
base SHA
branch
working-tree status
last production code SHA
supported corpus count
oracle pin source
oracle exact SHA/tag/revision
```

---

# 4. Oracle pin recovery gate

The pass must locate the **existing pinned Boxcars revision** used by prior differential evidence.

Search order:

```text
1. current R3.10–R3.13 evidence scripts/workflows/artifacts
2. commit history associated with differential lookup-plan work
3. executor/evidence files that record external oracle revision
4. temporary branch history if retained
5. explicit repository documentation
```

Do NOT choose a new revision merely because the pin is inconvenient to find.

Accepted outcome:

```text
ORACLE_PIN_PROVEN
oracle_repo = ...
oracle_sha  = exact immutable SHA
```

Blocked outcome:

```text
ORACLE_PIN_NOT_PROVEN
```

If blocked:

- do not instrument latest Boxcars;
- do not implement native reader;
- create pin-recovery evidence and stop R3.14A.

---

# 5. Oracle cleanliness rule

The oracle is a reference, not a co-developed implementation.

Process:

```text
clone/fetch exact pinned revision
verify HEAD == expected oracle SHA
record clean working tree
apply tiny instrumentation patch
record instrumentation diff
run evidence
optionally reset oracle tree afterward
```

The instrumentation patch must not change decode decisions. It may only expose already-decoded intermediate values and cursor positions.

Any instrumentation that changes control flow, bounds, bit order, or parser policy invalidates the evidence.

---

# 6. Exact R3.14A decode stop boundary

For each supported replay, oracle instrumentation may observe:

```text
frame_start_bit
frame_time
frame_delta
bit_after_time_delta
actor_present_bit_offset
actor_present
```

If `actor_present == false`, stop the first-actor envelope record there.

If `actor_present == true`, additionally observe:

```text
actor_id_start_bit
actor_id
actor_id_end_bit
alive_bit_offset
alive
```

If `alive == false`, stop there.

If `alive == true`, additionally observe:

```text
new_bit_offset
new
first_actor_header_end_bit
```

Then STOP.

R3.14A must not consume or expose as admitted evidence:

```text
name_id
post-name_id one-bit field
object_id
spawn location
spawn rotation
any spawn trajectory payload
property_present
stream_id
attribute payload
second actor envelope
second frame
```

The oracle itself may internally continue decoding because that is how it validates the replay, but the R3.14A evidence record must stop at the stated boundary.

---

# 7. Exact expected field order

The evidence must confirm the following order, not infer it from expected values:

```text
network_start
→ f32 time
→ f32 delta
→ actor_present bit
→ bounded actor_id       [only if actor_present]
→ alive bit              [only if actor_present]
→ new bit                [only if actor_present && alive]
→ STOP
```

A record must include bit offsets so an accidentally correct value read from an incorrect position cannot pass.

---

# 8. Bounded integer evidence requirements

Actor ID is the first high-value validation of the Rocket League bounded-integer primitive.

For each replay where `actor_present == true`, record enough information to reproduce the decode:

```text
bound / max channel-derived actor bound used by oracle
starting bit offset
precomputed low-bit width if oracle exposes it
low-bit contribution
whether extra discriminator bit was consumed
extra discriminator value if consumed
final actor_id
ending bit offset
```

If the oracle internals do not cleanly expose all intermediate details without invasive changes, the minimum accepted record is:

```text
bound
start bit
decoded value
end bit
number of bits consumed
```

R3.14B can derive/lock the primitive contract from these records.

Do not reduce actor ID evidence to `actor_id = N` only.

---

# 9. Float timing evidence

For `time` and `delta`, record:

```text
raw little-endian bytes or raw u32 representation if convenient
f32 decoded value
finite/non-finite classification
bit/byte offset before and after
```

Required invariants:

- values must be finite for every admitted evidence row;
- the first frame must not be the zero-time/zero-delta terminal sentinel if current supported evidence already says it is not;
- the evidence collector must not rewrite float values through decimal formatting and then compare strings only.

Prefer raw bits plus decoded float.

---

# 10. Corpus identity requirements

R3.14A must use exactly the current supported 47-replay set, not “the first 47 files in a directory.”

Each evidence row must carry at minimum:

```text
corpus rank or stable fixture key
relative replay path
byte length
SHA-256
production support status
BuildVersion / exact admitted tuple identifier if available
network_start
network_size
```

The collector must prove:

```text
input_count = 47
unique_sha256_count = 47
oracle_success_count = 47
```

Any missing/duplicate replay is a failed evidence pass.

---

# 11. Suggested evidence schema

Preferred JSONL row shape:

```json
{
  "replay_id": "stable-corpus-key",
  "sha256": "...",
  "byte_length": 0,
  "build_version": "...",
  "network_start": 0,
  "network_size": 0,
  "frame_start_bit": 0,
  "time_raw_u32": 0,
  "time": 0.0,
  "delta_raw_u32": 0,
  "delta": 0.0,
  "actor_present_bit_offset": 64,
  "actor_present": true,
  "actor_id": {
    "bound": 0,
    "start_bit": 65,
    "end_bit": 0,
    "bits_consumed": 0,
    "value": 0
  },
  "alive_bit_offset": 0,
  "alive": true,
  "new_bit_offset": 0,
  "new": false,
  "stop_bit": 0,
  "oracle_sha": "..."
}
```

Fields that are not applicable due to branch conditions may be `null`.

Use integer bit offsets from `network_start` to avoid byte-rounding ambiguity.

---

# 12. Aggregate evidence report

The pass must generate a concise aggregate report containing at least:

```text
replays_total
replays_unique_sha
oracle_parse_success
first_frame_rows
actor_present_true
actor_present_false
alive_true
alive_false
new_true
new_false
bounded_actor_id_rows
min_actor_id
max_actor_id
min_actor_id_bits_consumed
max_actor_id_bits_consumed
extra_discriminator_consumed_count (if observable)
non_finite_time_count
non_finite_delta_count
zero_zero_terminal_first_frame_count
schema_errors
bit_offset_monotonicity_failures
```

Expected success gates:

```text
replays_total = 47
replays_unique_sha = 47
oracle_parse_success = 47
first_frame_rows = 47
non_finite_time_count = 0
non_finite_delta_count = 0
zero_zero_terminal_first_frame_count = 0
schema_errors = 0
bit_offset_monotonicity_failures = 0
```

Do not invent expected counts for branch distributions (`new_true`, `alive_false`, etc.) before measuring them.

---

# 13. Differential cross-check with existing MIMIR structural state

Although production must not decode actor bits yet, R3.14A should cross-check non-bit facts against MIMIR's admitted static plan:

```text
network_start matches ReplayContentScaffoldV1
network_size matches ReplayContentScaffoldV1
max channel/bound inputs are consistent with ReplayNetworkLookupPlanV1
supported replay identity matches production lane
```

This cross-check ensures the oracle and MIMIR are looking at the same network byte range.

Do NOT add a hidden MIMIR bit parser merely to make the differential easier.

---

# 14. GitHub Actions / scripting correctness

Mandatory fail-fast behavior:

PowerShell:

```powershell
& cargo ...
if ($LASTEXITCODE -ne 0) { throw "cargo failed: $LASTEXITCODE" }
```

Apply the same idea to:

```text
git
cargo
rustc
python
external oracle build/run commands
custom binaries
```

A step that printed an error but ended green is FAILED evidence.

Temporary workflow should explicitly assert:

```text
MIMIR repo SHA
oracle SHA
47-input count
artifact output presence
non-empty evidence rows
aggregate success gates
```

---

# 15. Artifact policy

Recommended temporary evidence outputs:

```text
artifacts/r3_14a/first_actor_envelope.jsonl
artifacts/r3_14a/summary.json
artifacts/r3_14a/oracle_instrumentation.patch
artifacts/r3_14a/replay_manifest.jsonl
artifacts/r3_14a/run_receipt.txt
```

Whether these artifacts are admitted into `main` is a separate audit decision.

At minimum the final R3.14A decision artifact must preserve:

```text
MIMIR base SHA
oracle exact SHA
instrumentation diff hash or patch identity
corpus manifest identity
summary counts
outcome
next-pass decision
```

---

# 16. R3.14A outcome model

## Outcome A — evidence sufficient

Requirements:

```text
oracle pin proven
47/47 corpus identity valid
47/47 oracle decode success
field order observed consistently
bit offsets valid
actor ID bounded decode evidence sufficient for contract planning
no unexplained format divergence
```

Next:

```text
R3.14B — evidence admission + native bit-cursor / bounded-int contract planning
```

Still NOT allowed immediately:

```text
full actor decoder
spawn decoder
property decoder
attribute decoder
frame iterator
```

## Outcome B — bounded evidence gap

Examples:

```text
some replay starts with a format branch not represented by current order
actor bound source differs by replay family
oracle cursor detail insufficient to reproduce bounded integer
one supported replay cannot be correlated to oracle network start
```

Next:

- isolate the evidence gap;
- instrument only the missing field;
- rerun affected/all 47 as appropriate;
- no production implementation.

## Outcome C — contradiction

Examples:

```text
pinned oracle and R3.14 format order disagree
supported corpus contains multiple incompatible envelope encodings
production lookup preconditions point to wrong network region
```

Next:

- reopen format policy;
- do not implement R3.14C/D;
- preserve contradictory evidence.

---

# 17. Final R3.14A report template

Every executor/chat that completes this pass should report:

```text
PASS: R3.14A
Base MIMIR SHA:
Oracle SHA:
Corpus: 47 / 47
Evidence rows:
Time/delta finite:
actor_present true/false:
alive true/false:
new true/false:
Actor-ID bounded rows:
Actor-ID bit-consumption range:
Extra discriminator observations:
Schema/offset failures:
Production Rust files changed: 0
Outcome: A/B/C
Next exact pass:
```

---

# 18. Non-goals, repeated because future enthusiasm is dangerous

R3.14A is NOT:

- native actor decoder implementation;
- frame iterator implementation;
- actor lifecycle implementation;
- new actor spawn decode;
- property loop decode;
- attribute decode;
- raw-state extraction;
- event extraction;
- replay-to-skill work.

The entire value of this pass is proving the first few bits so the next implementation has a trustworthy bit cursor.

---

# 19. Definition of done

R3.14A is done only when all of the following are true:

- [ ] fresh MIMIR base audited;
- [ ] pinned oracle SHA proven;
- [ ] instrumentation patch is observation-only;
- [ ] exact supported 47 replay manifest locked;
- [ ] 47/47 oracle runs succeeded;
- [ ] first frame `time/delta` recorded with offsets/raw representation;
- [ ] first actor `actor_present` recorded;
- [ ] conditional `actor_id/alive/new` recorded;
- [ ] actor ID bit consumption is sufficiently characterized for planning;
- [ ] all artifacts carry oracle/MIMIR/corpus identity;
- [ ] production source unchanged;
- [ ] aggregate report has no unexplained anomaly;
- [ ] outcome explicitly chosen;
- [ ] continuity state updated only after the pass is admitted.
