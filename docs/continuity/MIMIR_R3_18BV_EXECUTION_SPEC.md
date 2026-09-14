# MIMIR R3.18BV — Published R3.18BU One-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`
**Production mutation:** forbidden
**Control authority:** R3.18BR `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / artifact `10267123608` / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1`
**Witness reselection:** forbidden

## Goal
Validate published BU on exactly two immutable rows. Require independently recomputed published BS equality, exact BR start/end/value/stop identity, repeatability and post-stop poison stability. Consume nothing adjacent.

## Frozen rows
```text
external_fixtures/sample_002.replay                                      11239 -> 11240  false
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay 3238  -> 3239   true
```
Expected: exact=2/2, false/true=1/1, mismatch=0, reselection=0, BP-false excluded=1/1, following stream/header/payload/second-control=0/0/0/0.

## Required checks
- exact production SHA/tree/lib/test/spec and BU CI receipts;
- reconstruct published BS independently and require BU prerequisite equality;
- exact control start/end/stop/value against BR;
- deterministic repeatability 2/2;
- truncate at control start -> atomic reject; corrupt BS/context/tag/actor/fabricated row -> reject;
- poison bits beginning at BU stop -> BU result unchanged;
- source-scope guard: one bounded control read, no following decoder/loop;
- focused BU regression, workspace fmt/check/test/clippy and repository verifier;
- same-head natural CI SUCCESS; privacy-safe deterministic evidence artifact + SHA-256 manifest; no production/Cargo/fixture/corpus/support mutation.

## Continuation classification
False row terminates. True row is the only possible later continuation candidate. BV does not decode a following header. Outcome A alone may open a separate later one-header evidence pass on that single true row.

## Hard stop
No following stream/header/payload, second control, generalized/repeated cursor, actor/frame/runtime widening, witness reselection or production mutation.

## Outcome gate
**A:** exact 2/2 + prerequisite 2/2 + false/true 1/1 + all negatives/validation PASS + adjacent consumption 0.
**B:** bounded mismatch/narrower subset only; no widening.
**C:** authority drift, published mismatch, adjacent access, mutation/privacy/generic chaining; stop.
