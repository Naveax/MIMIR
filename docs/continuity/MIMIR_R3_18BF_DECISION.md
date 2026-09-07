# MIMIR R3.18BF — Published R3.18BE Mixed Following-Header Differential Decision

**Date:** 2026-09-07
**Outcome:** **A — CLOSED / ADMITTED READ-ONLY EVIDENCE**
**Canonical production:** R3.18BE `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`
**Evidence head/tree:** `5a3f875a445f9a3a2176788555089562948c3676` / `d4b0b0510d24f5c0ba0f3d748201d9fed4ea7e0f`
**Evidence run/job:** `34098102185` / `101666129830` SUCCESS

## Decision

R3.18BF closes Outcome A. Published R3.18BE reproduced the exact immutable forty-row BA/BC/BD-backed lane with no witness reselection and no adjacent consumption.

- 37 BA-false rows remained successful no-header terminators.
- 3 BA-true rows returned exactly the frozen following headers.
- Exact R3.18BD membership remained 3/3 with multiplicity 3.
- Observed true tags remained **Boolean=2 / Float=1**.
- Published/native authority mismatch was 0.
- Witness reselection was 0.
- Following-payload and second-later-control consumption were 0/0.
- The seven upstream AU false terminators remained outside the BA/BE/BF lane.

The v1 evidence run `34097535331/101664404031` is explicitly non-authority. It failed closed at helper `rustfmt --check` before differential execution and produced only failure artifact `10009188799`. It was not rerun. The corrected v2 used a new SHA and independently passed authority, differential, full-validation, same-head-CI, privacy and artifact gates.

## Exact authority

```text
continuity base SHA/tree              cbfc861e1b570fcb2e9e1faf8b6bd16149b549b9 / cec0a3bbc64834b9288fe3effb7474387eb024ed
canonical production SHA/tree         1d717d3e82179edd85b197968f46b8f951a3e828 / 72cf2b907437a1ba62cc9deebd7608f7d0372f81
production parent                     3fa88f27201ee91c51a3bb7a623c00b46204c1e0
lib / BE focused-test blobs           92d9d1893d75f9f0bd5ca921d8cf80455b88f0c3 / 78f32c79a3526cbfeac4e32ccc06e5965cd3e97b
BE decision / BF spec blobs           7a1b410cc029ddcf8960420d60ae8ccba09d2060 / 86735a8adb67686c3905d809705c1f7066c6f716
BD contract                           sha256:33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27
BF evidence head/tree                 5a3f875a445f9a3a2176788555089562948c3676 / d4b0b0510d24f5c0ba0f3d748201d9fed4ea7e0f
BF evidence run/job                   34098102185/101666129830 SUCCESS
BF same-head CI                       34098102183/101666129957 SUCCESS
BF artifact                           10009534065 / 9998 bytes
BF artifact digest                    sha256:79a5d254876d19d90e03dcfeff650755d8b816d8a6869e13b8468eebd7d60bdc
BF inner manifest                     sha256:35747c9813f56e58c1515dc301cf6a0d3d3a86fd0b068fba609948016d0e45ce
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted read-only result

```text
frozen rows                           40/40
false no-header                       37/37
true exact header                     3/3
exact BD contexts                     3/3
BD multiplicity sum                   3
true tag distribution                 Boolean=2 / Float=1
mismatch                              0
witness reselection                   0
following payload consumed            0
second later control consumed         0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                               PASS
```

## Hard stop

BF does not admit payload production. No payload decoder is authorized on the 37 false rows or seven upstream AU false terminators. No second later property-control bit, generalized/repeated property cursor, actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

## Next gate

R3.18BG may inspect exactly one following primitive payload on the **three BF-true rows only**, using BF artifact `10009534065` as the direct row authority. Boolean rows have one-bit primitive width and the Float row has 32-bit primitive width, but BG must independently derive and compare exact current values and boundaries against pinned Boxcars. Historical AW/AM/AN payload coordinates or values are methodology only and may not be inherited. Only BG Outcome A may open a later, separate payload-end control-bit evidence pass.
