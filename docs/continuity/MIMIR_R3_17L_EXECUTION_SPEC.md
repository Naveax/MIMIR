# MIMIR R3.17L — Native K3 Real-Replay Differential Audit Execution Spec

**Pass type:** read-only differential audit
**Production mutation:** forbidden
**Production authority:** R3.17K Outcome A
**Contract authority:** R3.17J Outcome A
**Evidence authority:** R3.17I Outcome A

## Goal

Regenerate real K3 witness payloads ephemerally from the frozen 47-replay R3.17I lane and compare the published R3.17K native decoder against pinned Boxcars for every admitted exact structural/context group. This pass certifies the native implementation; it does not widen it.

## Frozen identities

```text
R3.17K production SHA       7390e3b145372252caaa8fa1fe3e0cd13b83336c
R3.17K production tree      eebe4e21de77a43b5d9d43a34a0bfb08e06bab02
lib.rs blob                 28d213f831c8968e6756a6ccea2cd7aa6cdbdfba
k3 groups module blob       da545a7144fefabab7f5be4f07fde71311065293
focused test blob           4d1434cc0e59a6e5c72a8404c102a87d71b8b223
R3.17K authority run/job    31836699291 / 94884467585 SUCCESS
R3.17K candidate CI         31837081536 / 94885655480 SUCCESS
R3.17K published-main CI    31837383875 / 94886588065 SUCCESS
R3.17J allowlist SHA256     9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
R3.17I evidence head        8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
R3.17I authority run/job    31812804986 / 94807233173 SUCCESS
R3.17I artifact             9223916983
R3.17I artifact digest      sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
R3.17I groups SHA256        04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b
pinned Boxcars SHA          c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane       47
exact admitted groups       1950
```

Before audit work, fetch fresh `main`, verify that the three production blobs above are unchanged, and verify the canonical J allowlist and R3.17I artifact identities. If production moved, reconstruct current truth before continuing.

## Real-witness reconstruction

Use the exact frozen 47 replay identities from R3.17I; do not widen the corpus. Instrument the pinned Boxcars oracle only at already-resolved K3 payload boundaries. Regenerate real payload observations ephemerally and deterministically select at least one real witness for **every one of the 1,950 R3.17J exact groups**.

The R3.17I group set is evidence-derived, so zero coverage for any admitted group is a contradiction or reconstruction failure, not permission to silently skip it.

Durable evidence may contain replay identity hashes/labels, frame/actor/property structural coordinates, context, exact bit ranges, packed structural codes, safe numeric/spatial values when required for comparison, and payload hashes. Do not persist unrelated player/account text or raw real payload bytes.

## Required native-vs-oracle comparisons

For every selected real witness, compare:

```text
resolved K3 tag / semantic variant
version 868.32 / net10 / RL223 context
payload_start_bit
payload_end_bit
payload_width
exact structural packed code
native success vs oracle success
```

Tag-specific comparisons:

### Location

Compare selected vector size, component width, raw x/y/z integer components, and semantic x/y/z.

### RigidBody

Compare sleeping branch, location vector structure/value, quaternion representation (`largest`, raw a/b/c, reconstructed x/y/z/w), and awake-only linear/angular vector structure/value. Sleeping witnesses must end immediately after quat56 and must not consume velocity-shaped trailing bits.

### ReplicatedBoost

Compare `grant_count`, `boost_amount`, `unused1`, `unused2`, exact 32-bit width and RL223=true gate.

### PickupNew

Compare presence branch, optional signed i32 instigator/reference, `picked_up`, and exact 9/41-bit width.

## Floating-point comparison rule

Before declaring equality, inspect the exact pinned Boxcars arithmetic for vector and quaternion reconstruction. If native and oracle perform the same operations in the same precision/order, require exact f32 bit equality. If the pinned source uses a materially different but mathematically equivalent operation order, define and persist a deterministic comparison rule before evaluating witnesses; do not improvise tolerances after observing mismatches.

## Negative controls

Regenerate or synthesize bounded controls that verify fail-closed behavior for at least:

```text
wrong major / minor / net_version
Location context/size pair absent from allowlist
vector selected size 20 / 21
vector truncation
RigidBody structural tuple absent from allowlist
RigidBody quat48 / quat56 truncation / invalid reconstruction
ReplicatedBoost RL223=false / truncation
PickupNew truncation
unsupported non-K3 tag
invalid payload start
trailing-bit non-consumption
atomic failure / no partial value escape
```

Negative controls do not authorize new shapes.

## Required gates

```text
fresh production identity                         PASS
47/47 replay identity verification                PASS
pinned Boxcars oracle decode                       47/47
R3.17I group reconstruction                        1950/1950
real witness group coverage                        1950/1950 minimum
native decode success on admitted witnesses        100%
tag / semantic variant match                       100%
context match                                      100%
payload start / end / width match                  100%
structural metadata / packed-code match            100%
semantic value match under predeclared rule        100%
negative controls                                  100%
bit monotonicity / packed-payload failures         0 / 0
privacy scan                                       PASS
production/Cargo/fixture/corpus/support mutation   0/0/0/0/0
normal CI on exact audit head                      PASS
```

## Outcome rules

- **Outcome A:** all 1,950 exact groups receive real witness coverage, every native/oracle comparison is exact under the predeclared numeric rule, negatives fail closed, privacy passes and mutation counts remain zero.
- **Outcome B:** reproducible evidence is insufficient to reconstruct one or more previously admitted groups; stop with targeted evidence work only. Do not widen or repair production.
- **Outcome C:** native/oracle mismatch, structural contradiction, source-identity contradiction or decoder defect. Stop. Repair evidence/contract/implementation in a separately admitted pass.

## Hard stop

R3.17L must not modify production Rust, Cargo files, fixtures, replay corpus or support lane. It must not consume a second property or advance actor/frame/lifecycle state. K4, raw-state, event, replay-slice, skill, runtime and export work remain closed.

## After Outcome A

Re-read `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md` and select the first dependency-valid unfinished pass. Do not pre-admit R3.18 merely because K3 differential closure succeeded.
