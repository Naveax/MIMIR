# MIMIR — R3.14D Exact Execution Spec

**Pass:** `R3.14D — first actor envelope header native reader`  
**Pass type:** narrow production implementation  
**Admitted production base:** `bad2db9d5043a7a0087a4fab1d278df5f36c7717`  
**Primary source scope:** `crates/mimir-replay/src/lib.rs`

## 1. Goal

Implement the smallest native production reader that consumes the first network frame timing pair and exactly one first actor-envelope header through the `new` bit by using the R3.14C private bit primitives.

This pass is not a frame iterator, actor lifecycle engine, spawn decoder, property decoder, or attribute decoder.

## 2. Preconditions

Before changing production source, re-prove:

```text
fresh main == or descends from bad2db9d5043a7a0087a4fab1d278df5f36c7717
R3.14C private NetworkBitCursor exists
R3.14C read_bounded_u32 exists
Cargo verification is --locked
R3.14A decision remains Outcome A
pinned Boxcars SHA remains c70e77df7af81b436cb545d070bb90c82f562d0b
supported production lane remains 47 replays unless separately admitted
```

If newer production code has changed the active boundary, stop and repair continuity from repository truth.

## 3. Exact wire order opened by this pass

```text
network bit 0
  read 32 bits -> time raw u32 -> f32
  read 32 bits -> delta raw u32 -> f32
  read actor_present bit

  if actor_present == false:
      STOP

  read actor_id using canonical R3.14C bounded-u32 primitive
  read alive bit

  if alive == false:
      STOP

  read new bit
  STOP
```

The R3.14A supported-corpus common first-envelope evidence was:

```text
time + delta   bits 0..64
actor_present  bit 64
actor_id       bits 65..76
alive          bit 76
new            bit 77
stop           bit 78
```

Those exact offsets are evidence expectations for the current 47-row lane, not a hard-coded parser shortcut.

## 4. Required production API

Use repository naming conventions and keep the result deliberately narrow.

Admitted shape:

```rust
pub struct ReplayNetworkFirstActorEnvelopeV1 {
    pub timing: ReplayNetworkTimingPreambleV1,
    pub first_frame_time_raw_u32: u32,
    pub first_frame_delta_raw_u32: u32,
    pub actor_present: bool,
    pub actor_id: Option<u32>,
    pub alive: Option<bool>,
    pub is_new: Option<bool>,
    pub stop_bit: u64,
}
```

Reader surface:

```rust
pub trait ReplayNetworkFirstActorEnvelopeReader {
    fn read_network_first_actor_envelope(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkFirstActorEnvelopeV1>;
}

pub struct MinimalReplayNetworkFirstActorEnvelopeReader;
```

Minor naming changes are allowed only when needed to match existing source conventions. The semantic field set and hard stop are fixed.

## 5. Reuse existing admitted layers

Do not duplicate header/build/support logic.

The implementation must reuse the current production structural/timing lane so that:

- exact header support predicates remain unchanged;
- `ReplayInput::File` remains unsupported unless a separate pass opens it;
- `network_start` / `network_size` come from admitted content structure;
- `num_frames`, `max_channels`, and `channel_bits` come from admitted production logic;
- the existing terminal-first-frame and timing validation policy is preserved.

`ReplayNetworkTimingPreambleV1` already rejects a `0.0 / 0.0` first-frame terminal marker. R3.14D must not read an actor bit after such a terminal timing pair.

## 6. Cursor requirements

The implementation must actually consume the timing pair through the R3.14C bit cursor.

Forbidden shortcut:

```text
set cursor position = 64
then start actor parsing
```

Required:

```text
read_bits_le(32) for time raw bits
read_bits_le(32) for delta raw bits
convert with f32::from_bits
```

The raw timing bits read through the cursor must match the already-admitted `ReplayNetworkTimingPreambleV1` values by `to_bits()`.
Any internal disagreement is a fail-closed error, not a reason to choose one representation silently.

## 7. Branch-state contract

The optional fields must preserve branch structure exactly.

### actor_present == false

```text
actor_id = None
alive = None
is_new = None
stop_bit = cursor immediately after actor_present
```

### actor_present == true, alive == false

```text
actor_id = Some(...)
alive = Some(false)
is_new = None
stop_bit = cursor immediately after alive
```

### actor_present == true, alive == true

```text
actor_id = Some(...)
alive = Some(true)
is_new = Some(...)
stop_bit = cursor immediately after new
```

Do not synthesize `false` for fields whose branch was never consumed.

## 8. Actor ID rule

Actor ID must call the single canonical R3.14C bounded-u32 primitive.

Inputs for the current lane:

```text
max_exclusive = admitted max_channels
low_width     = admitted channel_bits
```

Do not add an actor-specific fixed-width helper.
Do not manually consume a discriminator outside the canonical primitive.

## 9. Error policy

Fail closed for at least:

- insufficient network bytes for the timing pair;
- timing/raw-bit mismatch against the admitted timing preamble;
- missing `actor_present` bit;
- truncated actor-ID low bits;
- missing required actor-ID discriminator;
- invalid bounded integer configuration;
- missing `alive` bit;
- missing `new` bit when `alive == true`;
- any checked offset/range conversion failure.

A failed reader call must not return a partial success object.

## 10. Allowed source changes

Production Rust source:

```text
crates/mimir-replay/src/lib.rs
```

Focused tests may be added in the same crate/file according to current repository layout.

No other production Rust file is admitted by default.

## 11. Forbidden changes

R3.14D must not change:

```text
Cargo.toml
Cargo.lock
workspace dependencies
header/version/build support tuples
fixtures
checked-in replay corpus
static lookup semantics
attribute tag registry
spawn trajectory registry
```

No Boxcars production dependency.
No external replay parser dependency.

## 12. HARD STOP after `new`

The reader must not consume or expose:

```text
name_id
version-gated name-id payload
unnamed one-bit field after name_id
object_id
spawn trajectory payload
property_present
stream_id
attribute payload
second actor_present
second actor
second frame
network trailer
actor state mutation
raw state
events
replay slices
skills
```

For the currently observed 47 first-envelope rows, successful `alive=true` / `new=true` results should stop at bit 78. R3.14D must not inspect bit 78 as the start of the next field.

## 13. Focused tests required before publication

At minimum:

```text
1. first timing raw bits are consumed LSB-first and match preamble to_bits
2. actor_present=false branch stops immediately and leaves all later fields None
3. actor_present=true + alive=false branch leaves is_new None
4. actor_present=true + alive=true + new=false stops after new
5. actor_present=true + alive=true + new=true stops after new
6. bounded actor ID discriminator=0 path
7. bounded actor ID discriminator=1 path
8. bounded actor ID threshold/no-discriminator path
9. missing actor_present -> error
10. truncated actor ID low bits -> error
11. missing required actor ID discriminator -> error
12. missing alive -> error
13. missing new when alive=true -> error
14. terminal-first-frame remains rejected before actor parsing
15. File input remains unsupported
16. historical exact-admitted fixtures remain regression-green
17. existing R3.14C primitive tests remain green
```

Synthetic network slices may be used for branch/error coverage, but they must exercise the same production helper rather than a test-only decoder clone.

## 14. Validation gate

Use the repository verifier on the exact candidate source and keep Cargo locked.

Required minimum:

```text
cargo fmt --all -- --check
cargo test --locked -p mimir-replay -- --nocapture
cargo check --locked --workspace --all-targets --all-features
cargo test --locked --workspace --all-targets --all-features
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
cargo test --locked -p mimir-export -- --list
scripts/verify_test_corpus.ps1
scripts/verify_mimir_knowledge_archive.ps1
scripts/verify_repo.ps1
```

Native-command failures must propagate non-zero status.

## 15. Clean reconstruction / publication

Follow the permanent protocol:

```text
disposable implementation branch
→ focused + full validation
→ audit exact source diff
→ reconstruct only validated durable source blob onto fresh main
→ exact clean-SHA CI
→ fresh-main ancestry check
→ force=false publication
→ published-main exact readback
→ published-main exact CI
→ continuity sync
```

Temporary workflow/evidence tools do not enter the clean production commit.

## 16. R3.14D completion meaning

Successful R3.14D means:

> MIMIR can natively materialize one first-frame/first-actor envelope header through `new` for the currently admitted production lane, using its own bit cursor and bounded integer primitive.

It does **not** yet mean the 47-replay native output has been differentially admitted against Boxcars. That is R3.14E.

## 17. Next pass after successful R3.14D

```text
R3.14E — native first-envelope differential audit
```

R3.14E must compare MIMIR vs pinned Boxcars over all 47 supported replays for:

```text
time raw bits
delta raw bits
actor_present
actor_id
alive
new
stop bit
```

Any mismatch blocks R3.15A.
