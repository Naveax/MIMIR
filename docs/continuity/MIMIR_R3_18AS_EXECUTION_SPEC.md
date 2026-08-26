# MIMIR R3.18AS — One Following-Property-Header Evidence After Published R3.18AQ Mixed Control

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production authority:** R3.18AQ `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`
**Differential authority:** R3.18AR `7dfe2a0fc451a40d4c750dd2e401a2f0aa36dd9d` / `32949846799/98118570100` / artifact `9599823813`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden

## Goal

Preserve exactly the immutable R3.18AR 47-row identity lane and its mixed control split. The seven false rows are terminators and must stop after the published AQ control. On only the exact forty true rows, observe one following property header through `payload_start`, compare it exactly with pinned Boxcars, and stop.

This pass characterizes the header boundary only. It does not publish a following-header composition and does not decode the following payload.

## Frozen authority

```text
canonical continuity base             5bf20063a829526cc090ada8c4221d6b42ae5655 / 8fa16095e28b418d12c3050c69462ecae64ba880
production SHA/tree                   e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
production parent                     ec2d6c29f90863d9e312856043d01fb98a0c2d2d
lib / AQ focused-test blobs           b886c58400de0efe0a6a6113d79e6f78e751a213 / 983cbda666f40cbc739b250eac87bc4ce0c9eb99
AR evidence head/tree                 7dfe2a0fc451a40d4c750dd2e401a2f0aa36dd9d / 85a48eebc2d3292c524f482b5c131156fa8d7931
AR authority run/job                  32949846799/98118570100 SUCCESS
AR same-head CI                       32949846724/98118570114 SUCCESS
AR artifact                           9599823813 / sha256:20c7edce0ea6cc2d47168e9cb9bcc517cdad9b9bde78dcf7caa472403e525326
AR frozen rows                        47
AR false / true                       7 / 40
AR mismatch / reselection             0 / 0
AR adjacent consumption               0/0/0/0
AP artifact                           9526988237 / sha256:b50b01bd87c0b61ca2e407abe43ac5db9fb15290f7cd3e908332d2ac2a26c4cc
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Witness reselection is forbidden. Header tag/context distribution is **not** frozen in advance and must be discovered from these exact forty true rows.

## Witness classification

For all 47 AR rows:
- reconstruct the exact published R3.18AQ result;
- require its control value/start/end/stop to equal AR;
- if false, classify as terminator and stop;
- if true, classify as a continuation row eligible for exactly one header observation.

Required split: terminator rows 7; continuation rows 40; total 47. A count or identity drift is Outcome B/C until explained; do not silently replace witnesses.

## Positive header path — exact 40 true rows

For each true row:
1. build the existing production lookup plan;
2. reconstruct the valid published AQ boundary;
3. invoke the existing stateless existing-actor property-header primitive at the exact AQ `property_present_start_bit`, using the same actor object and lookup plan;
4. require header `property_present == true`;
5. require header present-bit start/end to equal AQ start/end;
6. compare stream start/end/value/bound/prop-bit width exactly with pinned Boxcars;
7. compare resolved property object and resolved attribute tag exactly;
8. compare `payload_start_bit` and header stop exactly;
9. stop at `payload_start_bit`.

Do not invoke any K1/K2/K3/K4 payload decoder.

## Terminator path — exact 7 false rows

For every false row, AQ control must remain false and exact; no following-header lookup/success may be claimed; no stream/property lookup or payload boundary may appear after AQ stop; consumed header/payload/second-control bits remain zero.

## Evidence outputs

Report the actual forty-row distribution of resolved property objects, attribute tags, exact replay/version/net-version/RL223 context needed to explain header resolution, stream bounds/prop-id widths, exact header coordinates, and multiplicities of complete structural/context tuples. Do not infer a Cartesian allowlist. If multiple exact header contexts appear, a later contract pass must freeze exact evidence-supported tuples before production composition.

## Required negative controls

At minimum: truncation inside a deterministic true-row stream/header; unresolved stream/property lookup; wrong actor object; wrong exact context where required; true-row repeatability; poison beginning at payload_start; false terminator no-header path; and a source-scope guard proving zero payload decoder calls and no repeated/generalized property loop.

## Required gates

```text
AR witness identities                     47/47 exact
AR control reconstruction                 47/47 exact
false terminators                         7/7 exact stop
true continuation rows                    40/40
true-row header native success            40/40
property_present start/end                40/40 exact
stream start/end/value/bound              40/40 exact
resolved property object                  40/40 exact
resolved attribute tag                    40/40 exact
payload_start / header stop               40/40 exact
header tuple classification               40/40
unclassified/mismatch                     0
following payload bits consumed           0
second later control bits consumed        0
negative controls                         PASS
privacy                                   PASS
production/Cargo/fixture/corpus/support   0/0/0/0/0
same exact evidence-head normal CI        SUCCESS
```

Run focused boundary regressions plus Rust 1.85 fmt/check/test/clippy and the full repository verifier when repository code is used. Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs; reuse an equivalent exact run if present; rerun is never polling.

## Hard stop

No following-payload semantic decode, no second later property control, no production header composition, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
All 40 true-row following headers match exactly through `payload_start`; all 7 false rows remain terminators; header/context classification is complete; mismatch and unclassified counts are zero; negatives/full validation/privacy pass; production mutation is zero; payload/second-control consumption is 0/0. Then a separate contract/admission pass may be opened if exact header tuple membership must be frozen before production.

### Outcome B
A bounded header/context distinction or evidence gap exists. Record it and keep production following-header composition closed.

### Outcome C
Authority/witness drift, native/oracle header mismatch, false-row header access, payload/second-control consumption, production mutation, privacy failure or generalized chaining. Stop without widening.
