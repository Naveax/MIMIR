# MIMIR — Current Canonical State

**Continuity date:** 2026-08-15
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `492cc8218be7abc6db8f75acaea33d009ab2f175`
**Production milestone:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`
**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`
**Completed K4 contract:** `R3.17N — Outcome A / 161/161 byte-identical groups / zero cross-product widening`
**Completed K4 production:** `R3.17O — Outcome A / 161/161 exact contract implementation / zero widening`
**Current exact pass:** `R3.17P — native K4 real-replay differential audit`

## 1. Truthful production boundary

Production is now R3.17O. MIMIR may decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload and stop at the exact one-value end bit. K4 success requires exact membership in the canonical 161-row structural/context allowlist; independent field unions do not admit a value.

```text
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
production tree              a66c47d7fb58da508188e64d42141987a0021a07
production parent            3392c28ba8ec7d72766303646c0ceb57ed1e5a19
lib.rs blob                  0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
k4 groups blob               103503e25bc5af48381df021ab58133694fcece6
k4 native blob               a9c41f3bb11343165183ac9c815ab8fdf085936c
focused K4 test blob         70437244bb49224281ee3a2e745e7b8a4b7a093a
R3.17N allowlist SHA256      80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
R3.17O authority run/job     31885987240 / 95015252318 SUCCESS
R3.17O exact-candidate CI    31886194387 / 95015736899 SUCCESS
R3.17O published-main CI     31886353485 / 95016105618 SUCCESS
```

The first two disposable implementation runs are not authority. `31885789107 / 95014781583` stopped before Rust because temporary tooling incorrectly assumed the canonical JSONL was tuple-sorted. `31885905139 / 95015053496` stopped before Rust because the independent equality checker compared non-admission evidence fields. The authoritative third run repeated every substantive gate after those plumbing-only corrections.

## 2. R3.17O production closure

```text
contract groups               161 / 161 exact
independent allowlist equality PASS
cross-product widening        0
all 161 synthetic positives   PASS
wrong context/tag/start        rejected
truncation                     rejected
Reservation malformed/text    rejected
Demolish cross-products        rejected
LoadoutsOnline unknown/cross   rejected
unobserved TeamLoadout version rejected
RL223 tuple mismatch           rejected
exact one-value end            PASS
full mimir-replay suite        PASS
workspace check/test/clippy    PASS
full repository verifier       PASS
production scope               exactly 4 files
Cargo/fixture/corpus/support   unchanged
```

The K4 API is separate and exposes `ReplayNetworkK4DecodeContextV1`, K4 semantic structures, `ReplayNetworkK4DecodeV1`, `R3_17N_K4_ADMITTED_GROUPS_V1`, and `decode_replay_network_k4_v1`. `LoadoutsOnline` receives the caller-resolved object table so product-attribute object IDs can be resolved without inventing a new lookup authority.

## 3. Evidence and contract authority

R3.17M remains the real-replay wire-format evidence authority: 47/47 pinned Boxcars decode, 39,463 K4 occurrences, all 11 target tags, 161 exact groups, 617 privacy-safe witnesses, zero structural failures. R3.17N remains the exact contract authority: the 161 admitted groups are byte-identical to the R3.17M group artifact and cross-product widening is zero.

```text
R3.17M authority head         a50f09857f36ac52cec30b4bf3efbde9e15bb564
R3.17M run/job                31881779861 / 95005282281 SUCCESS
R3.17M artifact               9246249473
R3.17M artifact digest        sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
R3.17N group SHA256           80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
R3.17N group blob             b5fa6aaa729772ab3d113703952effe2346c9866
R3.17N contract blob          76deabf8241b419ca224645106d2a19b041e20f8
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane         47
```

## 4. R3.17P exact next pass

R3.17P is read-only. Regenerate real K4 payload witnesses from the exact frozen 47-replay R3.17M lane and certify the published R3.17O native decoder against pinned Boxcars for **all 161 exact groups**. Compare tag, version/context, payload start/end/width, exact structural shape and semantic value. Sensitive account/player/title text may be compared in memory but must not be written in clear text to durable evidence.

Outcome A requires 161/161 real group coverage and 100% native/oracle equality, negative controls, privacy PASS, zero production/Cargo/fixture/corpus/support mutation, and normal CI on the exact audit head.

## 5. Still closed

```text
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
R3.18 reopening before R3.17P Outcome A + roadmap dependency check
```
