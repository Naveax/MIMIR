# MIMIR R3.17L Decision — Native K3 Differential Audit

**Outcome:** A — ADMITTED / COMPLETE
**Pass type:** read-only real-replay differential audit
**Production Rust:** unchanged
**Canonical production SHA:** `7390e3b145372252caaa8fa1fe3e0cd13b83336c`
**Continuity base:** `6b73a7e8f8639f8078dff0e656fc0fb9ea0bbc18`

## Authority

- evidence head: `0febcde7b312b6724e86ba156c700b41cf0562b7`
- authority workflow run/job: `31871353806 / 94980384463` — SUCCESS
- exact-head normal CI run/job: `31871353749 / 94980384205` — SUCCESS
- artifact: `9243555556` (`r317l-native-k3-differential-v3`)
- artifact digest: `sha256:514580727df642ebde04d69824402db46ed48ff66755d4b17c0db6e69ac5eb3d`
- artifact ZIP size: 287,021 bytes
- pinned Boxcars: `c70e77df7af81b436cb545d070bb90c82f562d0b`
- R3.17J allowlist SHA256: `9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911`

The first two R3.17L runs are not authority. Attempt 1 stopped at external-probe Cargo workspace plumbing after already proving 47/47 replay regeneration and 1,950/1,950 real-witness group coverage. Attempt 2 stopped before audit work because Windows resolved `bash` to the WSL launcher. V3 froze the V1 workflow blob, used exact Git Bash, and made only the empty external-probe `[workspace]` repair. Semantic and tolerance rules were unchanged.

## Differential result

```text
replay identity                   47/47
Boxcars oracle decode             47/47
K3 occurrences regenerated        1,699,169
exact group reconstruction        1,950/1,950
real witness group coverage       1,950/1,950
native decode success             1,950/1,950
tag / value variant match         1,950/1,950
context match                     1,950/1,950
payload start/end/width match     1,950/1,950
packed-code match                 1,950/1,950
semantic-value match              1,950/1,950
mismatches                        0
negative controls                 PASS / 7 focused tests
bit monotonicity failures         0
packed-payload failures           0
privacy                           PASS
production mutation               0
Cargo mutation                    0
fixture mutation                  0
corpus mutation                   0
support-lane mutation             0
```

The frozen quaternion rule allowed at most `1e-5` absolute difference only for the reconstructed largest component because pinned Boxcars uses chained f32 `mul_add` while native production uses equivalent explicit f32 operations. The observed maximum was `5.960464477539063e-08`. Non-largest quaternion components and vector components were compared by exact f32 bit identity.

## Durable receipt hashes

```text
aggregate                         2d2f153f8f23f07efae3e90216acf9f7c2d4df83548825a622a5a1343e37f5f0
source scope                      05dad8c789c61ed0ad25654544625ae67f0a969e68067efaa18e1c7c8c36b4fc
numeric rule                      7bf0f71e178b9c3c132473d3c67ee194e3b7cea54fb6690fec69fcd39b6a1190
replay identity                   b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation patch     4c7f92eb0315b5f62fb0d7ed059c775ed1381c351033ccfbfa218d9e308e068f
witness manifest                  e1b80971cc1787692d5355f14a6b18d49fdffd31baf7350b7783d6be6ae623ab
match rows                        ff4c908872a6ff46a58cabaff0d13b12691360a3e82ca00f3c5b5caf2466a6b5
summary                           aade96f9a47d6ba4cf74ef2b27370e7f6758c8041e0a8951ce418b9965c92fe2
negative controls                 a0a5dacc2c544d913f20bbbd68b2f736a33ca0974181fc62f4e1e410eeb66e7c
receipt manifest                  ecdf56c674627de997e7de417a8f50335b03d170c494fe5b5207f1f581048677
V3 driver receipt                 bd2ac7c6fea99d140ba2f89240846d6e326b0badd69eda4b0c685a20e7a68365
```

The artifact was downloaded independently after the workflow. Its ZIP SHA256 matched the GitHub artifact digest exactly, all 14 expected files were present, and all 11 hashes listed by the internal receipt manifest recomputed without mismatch. The instrumentation patch contains field-name literals such as `raw_bits_hex`, but the durable witness/match/summary evidence contains no raw payload bytes or player/account identity.

## Admission

R3.17K is now differentially validated on the complete R3.17J exact K3 structural/context group surface represented by the frozen 47-replay lane. This closes the K3 spatial/physics wave without widening the production decoder.

R3.17L does **not** admit a second property, property-loop iteration, next actor/frame, lifecycle mutation, K4 payload decoding, raw state, events, replay slicing, skills, runtime or export widening.

## Next pass

The execution roadmap still places the K4 gameplay-structured attribute wave inside R3.17 before R3.18 property-loop work. Therefore the next pass is:

**R3.17M — K4 Gameplay Structured Wire-Format Evidence**

Production implementation remains forbidden in R3.17M.
