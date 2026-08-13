# MIMIR — R3.14C Execution Spec

**Pass:** `R3.14C — native bit cursor + bounded integer primitive implementation`  
**Pass kind:** narrow production implementation + focused tests + audit + publication  
**Prerequisite:** `R3.14A Outcome A` + admitted `R3.14B` contract  
**Primary production file:** `crates/mimir-replay/src/lib.rs`  
**Hard stop:** private primitives only; no actor-envelope production reader  
**Next pass after successful admission:** `R3.14D — first actor envelope header native reader`

---

## 1. First actions in the implementation pass

Before editing:

```text
1. fetch fresh main;
2. record exact main SHA;
3. inspect commits since the continuity publication;
4. confirm no newer production replay milestone exists;
5. read MIMIR_R3_14A_DECISION.md;
6. read MIMIR_R3_14B_EXECUTION_SPEC.md completely;
7. inspect current crates/mimir-replay/src/lib.rs and its tests;
8. confirm Cargo.toml/Cargo.lock need no change;
9. open a dedicated implementation branch from fresh main.
```

If fresh production truth differs materially from the contract, stop and repair planning first.

---

## 2. Allowed implementation scope

Default allowed source path:

```text
crates/mimir-replay/src/lib.rs
```

Allowed content:

- one canonical private network bit cursor;
- one canonical private bounded-u32 helper/method;
- focused unit tests in the existing `mimir-replay` test structure;
- minimal private error helpers consistent with current `MimirError` conventions.

Forbidden without a new planning decision:

```text
Cargo.toml
Cargo.lock
new runtime dependency
Boxcars dependency/vendor source
other crates
fixtures/corpus changes
public actor/frame capability type
actor lifecycle state
support-version widening
```

---

## 3. Required private primitive behavior

Implement the R3.14B contract exactly:

```text
LSB-first bit ordering within each byte
exact bit_position accounting
read_bit
read_bits_le(0..=64)
read_bounded_u32(max_exclusive, low_width)
atomic failure semantics
no allocation in hot primitive path
no unsafe
```

Do not optimize by weakening observable cursor behavior.

---

## 4. Bounded integer rule that must be implemented

Conceptual algorithm:

```text
low = low_width LSB-first bits
range = 1 << low_width
up = low + range

if up < max_exclusive:
    discriminator = one more bit
    value = up if discriminator else low
else:
    value = low
```

Use sufficiently wide arithmetic for `range` / `up` so the primitive cannot overflow while validating inputs.

All failures are cursor-atomic.

R3.14A anti-regression vector:

```text
max_exclusive = 2047
low_width = 10
low = 0
up = 1024 < 2047
extra discriminator required
extra discriminator = 0
result = 0
consumed = 11 bits
```

A fixed 10-bit actor ID primitive is automatically a failed implementation.

---

## 5. Required focused tests

At minimum implement the 19 contract tests from R3.14B:

### Cursor

1. LSB-first ordering within one byte.
2. cross-byte multi-bit read.
3. exact position after mixed-width consecutive reads.
4. width 0 returns 0, position unchanged.
5. width 64 succeeds with exactly 64 available bits.
6. width >64 fails atomically.
7. empty/insufficient `read_bit` fails atomically.
8. insufficient multi-bit read fails atomically.

### Bounded integer

9. max 0 fails atomically.
10. max 1 returns the only valid value without over-read.
11. max 2047 / width 10 / low 0 / discriminator 0 => value 0, 11 bits.
12. same with discriminator 1 => value 1024, 11 bits.
13. low 1023 => up 2047, no discriminator, value 1023, 10 bits.
14. missing required discriminator fails atomically.
15. back-to-back bounded reads remain exactly aligned.
16. all admitted synthetic outputs are `< max_exclusive`.

### Regression/scope

17. no public actor/frame result type added.
18. no external parser dependency added.
19. existing replay tests remain green.

Add additional edge tests if implementation reveals a real arithmetic/cursor boundary; do not reduce this minimum set.

---

## 6. Focused validation before full workspace validation

Run:

```text
cargo fmt --all
cargo test -p mimir-replay <focused primitive tests> -- --nocapture
cargo test -p mimir-replay -- --nocapture
git diff --check
```

Re-open the implementation and focused tests after execution. Do not infer correctness from green output alone.

---

## 7. Full validation gate

Before admission:

```text
cargo fmt --all
cargo check --workspace --all-targets --all-features
cargo test -p mimir-replay -- --nocapture
cargo test --workspace --all-targets --all-features
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test -p mimir-export -- --list
pwsh -NoProfile -File ./scripts/verify_test_corpus.ps1
pwsh -NoProfile -File ./scripts/verify_mimir_knowledge_archive.ps1
git status --short
git diff --check
git diff
```

Use repository wrappers where current main requires them, but native-command exit status must remain fail-fast.

---

## 8. Differential vector gate

R3.14C is primitive-only, but it should replay the exact actor-ID primitive vector proven in R3.14A.

Required equality for the admitted vector:

```text
value = 0
bits consumed = 11
end bit = start bit + 11
```

If practical without widening production capability, include a table-driven test using the R3.14A current bound/width vector.

Do not add a 47-replay production parser loop merely to satisfy this primitive pass; full replay-envelope differential belongs to R3.14E after R3.14D creates the envelope reader.

---

## 9. Error and panic policy

Replay-controlled input must never panic.

Errors must be explicit for:

```text
invalid width
insufficient bits
invalid maximum
invalid bounded configuration
missing required discriminator
impossible defensive result
```

Atomicity must be asserted in tests by comparing cursor position before and after failure.

---

## 10. Publication construction

Use the established clean-publication protocol:

```text
implementation/evidence branch
→ focused tests
→ full validation
→ source/diff audit
→ reconstruct only admitted production source changes onto fresh main ancestry if needed
→ compare ancestry
→ force=false publication
→ exact published-SHA CI/readback
→ continuity sync
```

Temporary workflows and evidence scripts must not be smuggled into the clean production commit.

---

## 11. R3.14C hard stop

The final production diff must not consume or expose actor-envelope semantics.

Forbidden in R3.14C:

```text
read first-frame actor_present as a public production result
return actor_id from a replay reader
consume alive/new for a replay envelope
name_id
post-name bit
object_id
spawn trajectory
property_present
stream_id
attribute payload
actor mutation
multi-actor
multi-frame
raw state
```

Private synthetic tests may feed arbitrary bit patterns to the primitive; that is not replay-envelope parsing.

---

## 12. R3.14C admission criteria

R3.14C may close only when:

```text
private bit cursor implemented
private bounded integer implemented
all required focused tests pass
atomic failure proven
fixed-width anti-regression proven
no dependency change
no public envelope capability introduced
full workspace validation passes
corpus/knowledge verification passes
clean diff audited
exact publication SHA validated
continuity synced
```

Failure of any item keeps R3.14C open.

---

## 13. Next pass if admitted

Only after R3.14C is published and continuity-synced:

```text
R3.14D — first actor envelope header native reader
```

R3.14D may use the primitive to consume the already-evidenced narrow fields, still stopping before `name_id` / spawn / property payload.
