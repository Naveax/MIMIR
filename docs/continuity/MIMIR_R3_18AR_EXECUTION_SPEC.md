# MIMIR R3.18AR — Published R3.18AQ Mixed Following-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18AQ `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`
**Production mutation:** forbidden
**Following stream/header/payload:** forbidden
**Second later control:** forbidden

## Goal

Validate the published R3.18AQ one-control API against exactly the immutable R3.18AP 47-row authority lane. Prove that published AQ reconstructs the valid R3.18AN prerequisite, begins exactly at the frozen AP control start, returns the exact frozen boolean, ends/stops exactly one bit later, and consumes nothing adjacent.

The immutable distribution is **false=7 / true=40**. Both classes are successful published AQ results.

## Frozen authority

```text
production SHA/tree                  e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
parent                               ec2d6c29f90863d9e312856043d01fb98a0c2d2d
lib/test blobs                       b886c58400de0efe0a6a6113d79e6f78e751a213 / 983cbda666f40cbc739b250eac87bc4ce0c9eb99
AQ execution spec blob               fa8e5f6798a42fbeeed86b3b14ea7e4f39b35ebb
AQ builder                           32860339919/97842469079 SUCCESS
AQ builder receipt                   9568109670 / sha256:1d865740559cb0748f840b3cca3d4ab9c627ac251bc15f6f99dbabb20c2e3afe
AQ validation PR                     #197 closed unmerged
AQ exact-head CI                     32861522922/97846413853 SUCCESS
AQ published-main CI                 32861924684/97847764026 SUCCESS
AP evidence head/tree                736ac33c099a9183693bfcb2b5f5b74704a8808e / 840011b603b5bb330e018bd060650cfb3af29b73
AP authority                         32745234196/97489066582 SUCCESS
AP artifact                          9526988237 / sha256:b50b01bd87c0b61ca2e407abe43ac5db9fb15290f7cd3e908332d2ac2a26c4cc
AP frozen rows                       47
AP distribution                      false=7 / true=40
AP adjacent consumption              0/0/0/0
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Witness reselection is forbidden.

## Exact differential lane

For every one of the exact 47 AP witnesses:

1. reconstruct the exact valid published R3.18AN prerequisite;
2. call the published R3.18AQ API once;
3. require AQ `property_present_start_bit` == frozen AP control start == AN stop;
4. require AQ boolean == frozen AP boolean;
5. require AQ end/stop == frozen AP control end == start + 1;
6. repeat and require exact identical result;
7. stop.

Expected totals:
```text
rows                 47/47
false                7
true                 40
mismatch             0
witness reselection  0
```

## Required negative controls

At minimum:
- truncate exactly before the AQ control bit -> reject atomically;
- wrong actor authority -> reject before AQ control success;
- unresolved lookup -> reject before AQ control success;
- wrong exact context -> reject;
- corrupt/mismatched AN prior -> reject;
- repeat identical invocation -> exact equality;
- poison bits beginning at AQ stop -> returned one-bit result unchanged;
- source-scope guard -> exactly one control read and no generic loop/header/payload decode;
- next stream/header/payload/second-control consumption remains 0/0/0/0.

Because both booleans are admitted, flipping a frozen bit is not an API-malformed negative. If used as a differential mutation, it must be reported as frozen-value mismatch rather than as expected API rejection.

## Validation

Require:
- exact 47/47 frozen witness identities;
- published AQ versus frozen AP value/start/end/stop exact 47/47;
- published AN prerequisite exact 47/47;
- false=7 / true=40;
- mismatch 0;
- witness reselection 0;
- repeatability PASS 47/47;
- all negative controls PASS;
- adjacent stream/header/payload/second-control consumption 0/0/0/0;
- focused R3.18AQ tests PASS;
- full mimir-replay/workspace fmt/check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy scan PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an equivalent exact run if present. Rerun is never polling.

## Continuation classification

The frozen boolean controls continuation:
- the exact 7 false rows are terminators and must stop after the AQ control;
- the exact 40 true rows are continuation candidates.

AR itself does not decode any following header. Only if AR closes Outcome A may a separate later pass investigate exactly one following property header on the exact 40 true continuation rows, stopping at that header's payload start.

## Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
Published R3.18AQ is exact on all 47 immutable AP witnesses with false=7 / true=40, mismatch 0, witness reselection 0, all negative/full validations PASS and adjacent consumption 0/0/0/0. A later separate read-only pass may investigate one following header on exactly the 40 true continuation rows.

### Outcome B
A bounded mismatch or narrower supported subset is isolated. Admit only supported facts and keep following-header evidence closed.

### Outcome C
Authority/witness drift, published mismatch, rejection of an AP-admitted boolean class, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
