# MIMIR — R3.14B Execution Spec

**Pass:** `R3.14B — evidence admission + native bit-cursor / bounded-int contract planning`  
**Pass kind:** planning / contract / docs-only  
**Production Rust changes in this pass:** **FORBIDDEN**  
**Prerequisite:** `R3.14A Outcome A` recorded in `MIMIR_R3_14A_DECISION.md`  
**Next implementation pass if admitted:** `R3.14C — native bit cursor + bounded integer primitive implementation`

---

## 1. Why this pass exists

R3.14A proved the first supported-corpus actor envelope cursor against the pinned Boxcars oracle, but that evidence must not be converted directly into a broad frame decoder.

R3.14B narrows the implementation contract for the two primitives required before any native actor-envelope reader may exist:

```text
1. LSB-first network bit cursor
2. Rocket League bounded integer decoder
```

This pass admits only the contract. It does not consume production network bits and does not add a public replay capability.

---

## 2. Evidence authority

The format contract is grounded in:

```text
R3.14A decision artifact:
  docs/continuity/MIMIR_R3_14A_DECISION.md

successful evidence head:
  f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1

production baseline:
  ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa

pinned Boxcars:
  c70e77df7af81b436cb545d070bb90c82f562d0b

supported-lane manifest SHA-256:
  28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
```

R3.14A directly observed on all 47 supported replays:

```text
frame_start_bit       = 0
bit_after_time_delta  = 64
actor_present offset  = 64
actor_id start        = 65
actor_id end          = 76
alive offset          = 76
new offset            = 77
hard stop             = 78
```

All 47 actor-ID rows used:

```text
bound                 = 2047
low_width             = 10
bits_consumed         = 11
extra discriminator   = consumed
extra discriminator   = 0
actor_id              = 0
```

Therefore `channel_bits = 10` is not a fixed-width actor-ID decode contract.

---

## 3. Current production integration point

Current production already has:

```text
ReplayNetworkTimingPreambleV1
ReplayContentScaffoldV1
ReplayNetworkLookupPlanV1
```

`ReplayNetworkTimingPreambleV1` deliberately reads only the byte-aligned first 8 network bytes (`f32 time`, `f32 delta`) and stops before actor bits.

No native bit cursor helper was found in the current `mimir-replay` production source.

R3.14C should therefore introduce the narrow primitive in `crates/mimir-replay/src/lib.rs` as an internal implementation detail, with tests in the same crate, without widening the public replay capability surface.

---

## 4. R3.14C allowed source scope

Unless fresh repository truth proves a smaller necessary support file is required, R3.14C production changes are restricted to:

```text
crates/mimir-replay/src/lib.rs
```

Allowed changes:

- private/internal bit-cursor implementation;
- private/internal bounded-integer primitive;
- focused unit tests for those primitives;
- minimal error helper additions required by those tests/implementation.

Not allowed:

```text
Cargo.toml dependency additions
Cargo.lock changes
Boxcars dependency/vendor/copy
public actor-envelope reader
public frame iterator
actor state table
name_id/object_id/spawn/property/attribute decoding
raw-state/event/skill changes
support-lane expansion
```

If fresh implementation reality requires a Cargo/dependency change, R3.14C must stop and re-plan instead of silently widening scope.

---

## 5. Planned native bit cursor contract

Recommended internal shape:

```rust
struct NetworkBitCursor<'a> {
    bytes: &'a [u8],
    bit_position: usize,
}
```

The exact private type name may change if current source naming conventions demand it, but semantics are fixed by this contract.

Required operations:

```text
new(bytes)
position_bits() -> usize
remaining_bits() -> usize
read_bit() -> Result<bool>
read_bits_le(width) -> Result<u64>
read_bounded_u32(max_exclusive, low_width) -> Result<u32>
```

The cursor is relative to the beginning of the supplied network byte slice.

R3.14D, not R3.14C, will decide how the production actor-envelope reader constructs that slice from `ReplayContentScaffoldV1` / `ReplayNetworkLookupPlanV1`.

---

## 6. Bit ordering contract

Network bits are consumed **least-significant-bit first within each byte**, matching the admitted oracle behavior.

For byte:

```text
0b1010_0110
```

logical read order is:

```text
bit0=0
bit1=1
bit2=1
bit3=0
bit4=0
bit5=1
bit6=0
bit7=1
```

`read_bits_le(width)` assembles the first consumed bit as output bit 0, the next as output bit 1, and so on.

Reads may cross byte boundaries without realigning.

No byte-rounding is permitted between fields.

---

## 7. Cursor semantics

### 7.1 Initial state

```text
bit_position = 0
remaining_bits = bytes.len() * 8
```

### 7.2 Successful read

A successful read advances by exactly the number of bits consumed.

### 7.3 Failure atomicity

All primitive read failures must be cursor-atomic:

> if a read cannot complete, `bit_position` remains exactly where it was before the call.

This applies to:

- insufficient remaining bits;
- invalid requested width;
- invalid bounded-integer parameters;
- missing required bounded-integer discriminator bit.

This rule is deliberate. A failed primitive must not poison all later error reporting by leaving a half-advanced cursor.

### 7.4 Allocation / unsafe policy

Primitive reads must:

```text
allocate no heap data in the hot read path
use no unsafe
perform no I/O
perform no logging
mutate no actor state
```

---

## 8. `read_bit` contract

`read_bit()`:

1. checks that at least one bit remains;
2. identifies `byte_index = bit_position / 8`;
3. identifies `bit_index = bit_position % 8`;
4. returns `(bytes[byte_index] >> bit_index) & 1 != 0`;
5. advances `bit_position` by exactly one.

On insufficient data:

```text
explicit Mimir error
cursor unchanged
```

---

## 9. `read_bits_le(width)` contract

Allowed width:

```text
0..=64
```

Decision for width `0`:

```text
return 0
consume 0 bits
```

For width `1..=64`:

- require at least `width` bits before mutating the cursor;
- consume bits LSB-first;
- assemble into `u64` using consumed bit index as output bit index;
- advance exactly `width` bits.

For width `>64`:

```text
explicit invalid-width error
consume 0 bits
```

---

## 10. Rocket League bounded-integer contract

R3.14A and the pinned oracle establish this planning algorithm.

Inputs:

```text
max_exclusive
low_width
```

Use a wide intermediate (`u64`) for arithmetic.

Pseudo-contract:

```text
validate max_exclusive > 0
validate low_width <= 32 for the planned u32 primitive

low = read_bits_le(low_width)
range = 1 << low_width
up = low + range

if up < max_exclusive:
    discriminator = read_bit()
    if discriminator:
        value = up
    else:
        value = low
else:
    value = low

require value < max_exclusive
return value
```

The preflight check must ensure enough bits for the complete path before permanently advancing the cursor. In particular, when `up < max_exclusive`, lack of the discriminator bit is a failed atomic read.

---

## 11. Why this is not fixed-width decoding

R3.14A current-corpus example:

```text
max_exclusive = 2047
low_width     = 10
low           = 0
range         = 1024
up            = 1024
1024 < 2047   = true
```

Therefore an extra discriminator bit is required.

Observed first actor:

```text
discriminator = 0
value         = 0
consumed      = 11 bits
```

A naive `read_bits_le(10)` implementation would leave the cursor one bit early and corrupt the subsequent `alive` and `new` fields.

That exact anti-regression is the primary reason R3.14A existed.

---

## 12. Bound/source rule

R3.14C implements the generic primitive only. It must not choose actor/property bounds on its own.

Future callers must pass already-admitted bounds from the static lookup plan:

```text
actor_id:
  max_exclusive = ReplayNetworkLookupPlanV1.max_channels
  low_width     = ReplayNetworkLookupPlanV1.channel_bits

stream/property id later:
  max_exclusive / width come from the corresponding admitted object/property lookup plan
```

R3.14C must not parse metadata, inspect filenames, infer builds, or broaden support to obtain those bounds.

---

## 13. Error contract

R3.14C should use the repository's existing `MimirError` / `Result` pattern.

Exact private helper/error strings may follow current local conventions, but focused tests must distinguish at least:

```text
insufficient network bits
invalid bit width
invalid bounded-integer maximum
invalid bounded-integer low width / impossible configuration
bounded result outside admitted maximum (defensive invariant)
```

No panic is allowed for replay-controlled input.

Panics in tests for impossible programmer-only setup are not a substitute for replay-input validation.

---

## 14. Required R3.14C unit tests

The implementation pass must cover at least:

### Bit cursor

1. LSB-first bit ordering inside one byte.
2. `read_bits_le` crossing a byte boundary.
3. exact cursor position after consecutive mixed-width reads.
4. width `0` returns zero and consumes zero bits.
5. width `64` works when exactly 64 bits remain.
6. width `>64` fails without cursor movement.
7. insufficient `read_bit` fails without cursor movement.
8. insufficient multi-bit read fails without cursor movement.

### Bounded integer

9. `max_exclusive = 0` fails without cursor movement.
10. `max_exclusive = 1` produces only valid zero without over-reading.
11. R3.14A form: `max=2047`, `low_width=10`, low `0`, discriminator `0` -> value `0`, 11 consumed bits.
12. same low bits with discriminator `1` -> value `1024`, 11 consumed bits.
13. edge low `1023`: `up=2047`, so no discriminator; value `1023`, 10 consumed bits.
14. missing required discriminator fails atomically.
15. synthetic back-to-back bounded reads preserve exact cursor alignment.
16. returned value is always `< max_exclusive` for admitted synthetic cases.

### Regression locks

17. no public actor/frame capability type introduced by R3.14C.
18. no external parser dependency added.
19. existing `mimir-replay` tests remain green.

---

## 15. Validation required for R3.14C

At minimum:

```text
cargo fmt --all
cargo check --workspace --all-targets --all-features
cargo test -p mimir-replay -- --nocapture
cargo test --workspace --all-targets --all-features
cargo clippy --workspace --all-targets --all-features -- -D warnings
git diff --check
```

Repository-level verifier/CI must also remain green on the exact candidate SHA before publication.

R3.14C is not admitted from focused unit tests alone.

---

## 16. R3.14C hard stop

R3.14C stops after the reusable private primitives exist and are tested.

It must **not** add code that reads:

```text
first frame time/delta into a new native frame object
actor_present
actor_id as an actor-envelope production result
alive
new
name_id
object_id
spawn trajectory
property_present
stream_id
attribute payload
next actor
next frame
```

Those caller semantics begin in R3.14D or later according to the roadmap.

---

## 17. R3.14B admission criteria

R3.14B is admitted only if:

```text
R3.14A Outcome A decision artifact present
bounded-int algorithm unambiguous
bit ordering unambiguous
cursor failure atomicity explicit
R3.14C source scope explicit
R3.14C required tests explicit
hard stop explicit
no production Rust change
no dependency change
continuity/knowledge graph synchronized
normal CI passes
knowledge archive verifier passes
```

---

## 18. R3.14B outcome

The contract above is sufficient to proceed without another evidence pass.

```text
R3.14B OUTCOME: ADMITTED / COMPLETE
```

Next exact pass:

```text
R3.14C — native bit cursor + bounded integer primitive implementation
```

R3.14C may implement only the primitives defined here. The first actor-envelope production reader remains R3.14D.
