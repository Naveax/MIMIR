# MIMIR R3.18BB — Published R3.18BA Mixed Following-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Frozen control authority:** R3.18AX `465a3f2fc71e5eed6f00c16a04738031bef8d82c` / artifact `9644869549` / `sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9`
**Production mutation:** forbidden
**Following stream/header/payload:** forbidden
**Second later control:** forbidden

## 1. Goal

Validate published R3.18BA against exactly the immutable forty R3.18AX witnesses without reselection. Reconstruct the published prerequisites, call published BA once per frozen row, and require exact equality with the frozen AX control start, boolean value and one-bit end boundary.

The immutable distribution is **false=37 / true=3**. Both classes must be successful BA results. False rows terminate at BA stop. True rows are only continuation candidates for a later separate pass; BB itself does not decode their following header.

## 2. Exact lane

For every one of the exact forty AX witnesses:

1. reconstruct the exact valid published R3.18AY prerequisite;
2. call published R3.18BA;
3. require BA control start == AX frozen control start == AY stop;
4. require BA boolean == AX frozen boolean;
5. require BA end/stop == AX frozen end == start + 1;
6. repeat and require exact identical result;
7. poison bits beginning at BA stop and require the returned BA result unchanged;
8. stop.

Expected totals:

```text
rows                 40/40
false                37
true                 3
mismatch             0
witness reselection  0
```

The seven upstream AU false terminators remain outside the BB lane and must never reach a BA control success.

## 3. Required negatives

At minimum:
- corrupt/mismatched AY prior -> reject before BA success;
- wrong actor authority -> reject;
- unresolved lookup -> reject;
- wrong exact version context -> reject;
- upstream AU false terminator -> no AY/BA success;
- repeat identical invocation -> exact equality;
- poison bits beginning at BA stop -> result unchanged;
- source-scope guard -> exactly one AY recomputation and one control read, with no generic loop/header/payload decode;
- next stream/header/payload/second-control consumption remains 0/0/0/0.

Exact bit-level truncation immediately before the control is inherited from immutable R3.18AX evidence (`TRUNCATION_BEFORE_CONTROL=PASS 40/40`). All forty frozen control starts are non-byte-aligned, so BB must not fabricate a partial-byte EOF claim through the byte-slice production API. Carrier truncation may be tested only for fail-closed behavior actually representable by `&[u8]`.

## 4. Validation

Require:
- exact forty frozen witness identities;
- published BA versus frozen AX start/value/end/stop exact 40/40;
- false=37 / true=3;
- mismatch 0;
- witness reselection 0;
- repeatability PASS 40/40;
- post-stop poison isolation PASS 40/40;
- all authority/context/lookup negatives PASS;
- adjacent stream/header/payload/second-control consumption 0/0/0/0;
- focused BA tests PASS;
- full mimir-replay/workspace fmt/check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy scan PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an equivalent exact run if present. Rerun is never polling.

## 5. Continuation classification

The frozen BA boolean controls only the next evidence candidate set:
- exact 37 false rows are terminators and must stop at BA;
- exact 3 true rows are candidates for a later separate one-header evidence pass.

R3.18BB itself authorizes no following header, payload or second control.

## 6. Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 7. Outcome gate

### Outcome A

Published R3.18BA is exact on all forty immutable AX witnesses with false=37 / true=3, mismatch 0, witness reselection 0, all negatives/full validation PASS and adjacent consumption 0/0/0/0. A later separate read-only pass may investigate exactly one following header on only the three true rows.

### Outcome B

A bounded mismatch or narrower supported subset is isolated. Admit only supported facts and keep following-header evidence closed.

### Outcome C

Authority/witness drift, published mismatch, rejection of an AX-admitted boolean class, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
