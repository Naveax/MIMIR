# MIMIR — R3.14A Evidence Admission Decision

**Decision date:** 2026-08-13  
**Pass:** `R3.14A — first frame + first actor envelope differential evidence`  
**Pass kind:** evidence-only / pinned-oracle instrumentation  
**Outcome:** **A — EVIDENCE SUFFICIENT**  
**Next exact pass:** `R3.14B — evidence admission + native bit-cursor / bounded-int contract planning`

---

## 1. Authority and production boundary

R3.14A did **not** change MIMIR production replay code.

Production code baseline remains:

```text
ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
```

Production milestone remains:

```text
R3.13 — static replay network lookup plan
```

The successful evidence head was:

```text
f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
```

Evidence tooling lived on the disposable branch:

```text
agent/r3-14a-first-actor-envelope-evidence
```

The evidence branch was independently checked against the admitted production baseline. No change was present in:

```text
crates/**
Cargo.toml
Cargo.lock
external_fixtures/**
test_corpus/**
```

Therefore this decision admits **format evidence and planning facts only**. It does not admit a native production bit reader.

---

## 2. Exact oracle identity

Pinned oracle:

```text
repository: nickbabcock/boxcars
commit: c70e77df7af81b436cb545d070bb90c82f562d0b
```

Pinned source blobs verified before instrumentation:

```text
src/network/frame_decoder.rs = 6f2ff153d3a27cdacccc65e3f23851489077a7d8
src/bits.rs                  = d3ca061580e5e78038b2af383ff53971001c91c9
prepatch_tree_clean          = true
```

Observation-only instrumentation changed exactly:

```text
examples/r3_14a_probe.rs
src/network/frame_decoder.rs
```

Final instrumentation patch SHA-256:

```text
0fed1f4812b07efe660ee1eb07d8f1876287ad34632563d94783c77740991408
```

Effective evidence-driver SHA-256:

```text
8b3b20a7e5770614112131da1f84b6e238b3a5c5bce36cd54f236189aaf1476d
```

The instrumented oracle passed:

```text
cargo check example      = PASS
Boxcars library tests    = 43 / 43 PASS
probe build              = PASS
```

---

## 3. Exact corpus identity

The production-supported selector was rerun over exactly:

```text
3 historical fixtures + test_corpus/largest_100 = 103 replay files
```

Selector result:

```text
total_replays             = 103
supported_replays         = 47
unsupported_replays       = 56
unique_supported_sha256   = 47
```

Stable supported-lane manifest SHA-256:

```text
28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
```

Each supported replay identity carried:

```text
stable corpus index
relative path
byte length
SHA-256
BuildVersion
network_start
network_size
MaxChannels
channel_bits
```

The final oracle JSONL contained exactly 47 rows, 47 unique paths and 47 unique replay SHA-256 values, with zero selector/JSONL identity mismatch.

---

## 4. Workflow and artifact identity

Successful GitHub Actions run:

```text
workflow: Temporary R3.14A Pinned Oracle Evidence V2
run_id:   31690714121
job_id:   94417135424
head_sha: f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
result:   SUCCESS
```

Evidence artifact:

```text
artifact_id: 9177314099
artifact_name: r3-14a-pinned-oracle-evidence-v2-f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
artifact_zip_sha256: d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
```

The downloaded artifact digest was independently recomputed and matched GitHub's reported artifact digest exactly.

Bundle contents included:

```text
r3_14a_effective_driver_sha256.txt
r3_14a_selector_for_oracle.log
r3_14a_supported.tsv
r3_14a_oracle_identity.txt
r3_14a_boxcars_instrumentation.patch
r3_14a_oracle.log
r3_14a_aggregate.txt
r3_14a_first_actor_envelope.jsonl
r3_14a_summary.json
r3_14a_spec_aggregate.txt
```

---

## 5. Aggregate evidence

Successful final aggregate:

```text
replays_total                         = 47
replays_unique_sha                    = 47
oracle_parse_success                  = 47
first_frame_rows                      = 47
actor_present_true                    = 47
actor_present_false                   = 0
alive_true                            = 47
alive_false                           = 0
new_true                              = 47
new_false                             = 0
bounded_actor_id_rows                 = 47
min_actor_id                          = 0
max_actor_id                          = 0
min_actor_id_bits_consumed            = 11
max_actor_id_bits_consumed            = 11
extra_discriminator_consumed_count    = 47
non_finite_time_count                 = 0
non_finite_delta_count                = 0
zero_zero_terminal_first_frame_count  = 0
terminal_first_frame_rows             = 0
schema_errors                         = 0
bit_offset_monotonicity_failures      = 0
production_source_mutation            = 0
```

Measured values were not pre-assumed. The uniform first-envelope distribution is an observed fact of the current 47-replay supported corpus.

---

## 6. Exact first-envelope order proven by the 47-replay lane

Every admitted evidence row followed this cursor sequence relative to `network_start`:

```text
frame_start_bit          = 0
read f32 time            -> bit 32
read f32 delta           -> bit 64
actor_present bit        = bit 64
actor_id start           = bit 65
bounded actor_id end     = bit 76
alive bit                = bit 76
new bit                  = bit 77
R3.14A hard stop         = bit 78
```

For all 47 rows:

```text
actor_present = true
actor_id       = 0
alive          = true
new            = true
```

`time` was finite in all 47 rows and had 47 distinct observed values. `delta` was finite and observed as `0.0` in all 47 first frames. No first frame was the zero-time/zero-delta terminal sentinel.

---

## 7. Bounded actor-ID evidence admitted

All 47 supported rows carried:

```text
MaxChannels / bound       = 2047
precomputed channel_bits  = 10
actor_id low width        = 10
actor_id bits consumed    = 11
extra discriminator       = consumed
extra discriminator value = 0
actor_id value            = 0
```

This is direct corpus evidence that `channel_bits = 10` is **not** permission to consume only 10 bits.

The native contract must preserve Rocket League's value-dependent bounded-integer rule:

1. consume the low-width candidate bits;
2. compute the upper candidate using the low-width range;
3. consume the discriminator only when the bound/value relation requires it;
4. return the low or upper candidate according to that discriminator;
5. advance the cursor by exactly the bits actually consumed.

R3.14A therefore provides sufficient evidence to plan the native bounded-int primitive. It does **not** yet admit its production implementation.

---

## 8. Differential consistency with MIMIR static state

For every final evidence row:

```text
relative replay identity     = selector identity
SHA-256                      = selector identity
byte length                  = selector identity
BuildVersion                 = selector identity
network_start                = production lookup-plan selector value
network_size                 = production lookup-plan selector value
MaxChannels                  = production lookup-plan selector value
channel_bits                 = production lookup-plan selector value
```

Independent readback found zero selector/JSONL mismatch.

This proves the oracle instrumentation and MIMIR static lookup plan were observing the same admitted replay/network ranges.

---

## 9. Hard stop verification

R3.14A output stopped after the conditional `new` bit.

The durable JSONL evidence did **not** expose fields for:

```text
name_id
unnamed post-name bit
object_id
spawn trajectory
property_present
stream_id
attribute payload
next actor envelope
next frame envelope
raw semantic state
```

The oracle itself was allowed to finish parsing so decode success could be established, but instrumentation output was observation-only and stopped at the admitted R3.14A boundary.

No production capability is claimed beyond this evidence boundary.

---

## 10. Outcome classification

R3.14A execution-spec Outcome A requires:

```text
oracle pin proven                              PASS
47/47 corpus identity valid                    PASS
47/47 oracle decode success                    PASS
field order observed consistently              PASS
bit offsets valid                              PASS
bounded actor-ID evidence sufficient           PASS
no unexplained format divergence               PASS
```

Decision:

```text
OUTCOME A — EVIDENCE SUFFICIENT
```

---

## 11. Boundaries opened by this decision

Opened for **planning/admission only**:

- first-frame native timing cursor contract planning;
- `actor_present` cursor contract planning;
- bounded actor-ID primitive contract planning;
- conditional `alive` / `new` envelope contract planning;
- R3.14C implementation planning for a native bit cursor + bounded-int primitive.

Not opened for production decoding yet.

---

## 12. Boundaries still closed

Still closed:

```text
native production bit cursor implementation until R3.14C admission
native actor_id bounded-int implementation until R3.14C admission
native first actor envelope production reader until R3.14D
name_id decoding
unnamed post-name bit decoding
object_id decoding
spawn trajectory payload decoding
existing-actor property loop
stream_id decoding
attribute payload decoding
actor lifecycle mutation from network bits
multi-actor iteration
multi-frame iteration
raw-state extraction
event extraction
replay slicing
skill mining
counterfactual rollout from native replay state
```

---

## 13. Next exact pass

Proceed to:

```text
R3.14B — evidence admission + native bit-cursor / bounded-int contract planning
```

R3.14B is a planning/contract pass. It must not silently become R3.14C implementation.
