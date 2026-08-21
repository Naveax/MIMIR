# MIMIR R3.18AN — Dependency-Gated Slot 4 Preparation

**Status:** NON-CANONICAL / PREPARATION ONLY  
**Parallel slot:** 4/5  
**Requested target offset:** 3  
**Initial canonical frontier:** R3.18AK  
**Provisional target identity:** R3.18AN, derived only as `R3.18AK + 3 sequential canonical passes`  
**Preparation base:** `f20f529e3ada6e9a671ea91e5676a17a00770145` / tree `98c675811cca4e4d7f0122c762f371548c9266c2`  
**Capability claim:** NONE

> This file is intentionally not an execution spec, admission decision, contract, or production capability. It records only work that is safe before the prerequisite chain is canonical. Future canonical specs/decisions outrank this preparation completely.

## 1. Why this preparation is dependency-gated

At slot initialization, canonical `main` was `5e26e7d3ceceac9752c35dde9c5074a1cd15262d`, which admitted R3.18AJ and opened R3.18AK. During the same execution window, `main` advanced by direct fast-forward to the exact R3.18AK production candidate `f20f529e3ada6e9a671ea91e5676a17a00770145`.

R3.18AK is not treated as CLOSED here merely because its source commit is present on `main`. Canonical closure still requires exact published-main validation/readback and continuity admission. R3.18AL and R3.18AM are not assumed to exist or to have any particular outcome.

Therefore the requested offset-3 target can be named provisionally as R3.18AN by sequence position, but its **pass class, payload family, exact authority, API, contract and admitted behavior remain unknown until its predecessors publish canonical execution specs/decisions**.

## 2. Frozen authority available now

```text
R3.18AG production
  SHA  2d351e8ceb601e2fbe515d2977b2103a4b2c7976
  tree 4123820ce6537f2d4942cd0b5f72b52e43b96c1d

R3.18AI evidence
  rows 47/47
  exact complete seven-field header contexts 17
  observed header tags Int=47
  native/oracle mismatch 0
  witness reselection 0
  artifact 9424764320
  artifact sha256 ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5

R3.18AJ contract
  exact_tuple_only
  contexts 17
  multiplicity sum 47
  observed header tags Int=47
  sha256 cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
  R3.18Z inheritance false
  R3.18P inheritance false

R3.18AK clean source candidate / current main during preparation
  SHA  f20f529e3ada6e9a671ea91e5676a17a00770145
  tree 98c675811cca4e4d7f0122c762f371548c9266c2
  parent 5e26e7d3ceceac9752c35dde9c5074a1cd15262d
  exact source scope lib.rs + r3_18ak_post_ag_following_header.rs
  validation-only PR #62 closed unmerged
  PR exact-head CI 32454918857 SUCCESS
  corrected builder 32454544283 / job 96689214219 SUCCESS
  builder artifact 9436810006
```

The presence of the AK source commit on `main` is not by itself the published-main closure receipt.

## 3. Required canonical prerequisite chain

Before any R3.18AN production implementation or publication, require all of the following from fresh repository truth:

1. **R3.18AK canonical CLOSED**
   - exact source SHA/tree/blob identities;
   - exact published-main validation SUCCESS/readback;
   - continuity and knowledge graph synced;
   - next pass explicitly named.
2. **R3.18AL canonical result**
   - use whatever exact pass class and authority the admitted AK continuity names;
   - if it is the expected published-AK differential, require immutable 47-row authority, zero witness reselection, zero mismatch and exact stop-boundary accounting;
   - do not manufacture that result if another slot owns it.
3. **R3.18AM canonical result**
   - use its actual execution spec/decision rather than inferred sequence symmetry;
   - if it is payload evidence, require exact immutable rows, payload starts/ends/widths/semantic identities, native-oracle comparisons, negatives, mutation counters and artifact manifest;
   - do not infer payload form from the preceding header tag alone.
4. Fresh `main` re-read immediately before target implementation.

If any prerequisite chooses Outcome B/C or changes the next-pass identity, this preparation must be revised rather than replayed mechanically.

## 4. Critical anti-assumption lock

R3.18AI/R3.18AJ observed `Int=47` for the **header tag**. That does **not** independently prove the R3.18AN payload contract, exact width, semantic result or production eligibility.

Forbidden before a canonical payload-evidence authority exists:

```text
Int header tag => assume 32-bit payload authority
select primitive scalar decoder solely from tag name
invent payload_end coordinates
invent semantic values
invent a 47-row payload equality claim
invent R3.18AM Outcome A
```

Only the future admitted evidence may open those statements at this boundary.

## 5. Historical analogues already inspected

The nearest production-payload analogues establish a reusable process pattern, not reusable target data:

### R3.18J
- evidence-first bounded payload production;
- reuse existing lower-level decoder rather than duplicate wire logic;
- exact admitted tag/context gate;
- exact payload-end stop;
- no later property control;
- no generic cursor/loop.

### R3.18T
- start only from an already-valid bounded following-header result;
- admit only exact evidence-observed payload families and widths;
- preserve typed lower-level result identity;
- fail closed on wrong context/tag/truncation;
- poison after payload end must not affect the result;
- another-control consumption remains zero.

### R3.18AD
- complete header/context authority remains mandatory at the payload boundary;
- lower-level decoder support elsewhere does not widen the boundary;
- exact evidence-observed layouts only;
- clean source scope and publication validation are separate from evidence.

No analogue permits component-wise, tag-only, width-only or Cartesian widening.

## 6. Provisional target source boundary

If and only if the future canonical R3.18AN spec is a bounded payload-production pass, the smallest likely source surface is:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_18an_*.rs
```

This is a preparation estimate, **not an allowed-file grant**. The canonical R3.18AN execution spec must define the exact files before mutation.

Potential source strategy, only after evidence authorizes it:

1. accept/recompute the exact published predecessor header result;
2. require complete predecessor structural/context authority;
3. begin at exactly `header.payload_start_bit`;
4. reuse the lower-level decoder explicitly supported by the new evidence;
5. verify exact payload width/end/value/context required by that evidence;
6. return one bounded typed payload result;
7. stop exactly at payload end;
8. read zero bits of another property control;
9. expose no generic/repeatable property iterator or cursor.

## 7. Prepared focused test matrix

The exact vectors and expected values remain placeholders until the prerequisite evidence is canonical. Required categories are already fixed:

- exact real replay representatives from the immutable prerequisite witness set;
- exact prior/header reconstruction before payload decode;
- payload start equality to predecessor stop;
- exact payload end/width/value equality from evidence;
- deterministic repeatability;
- truncation at every newly consumed payload boundary;
- wrong prior / wrong actor / unresolved lookup where applicable;
- wrong exact version/context;
- tag or payload layout outside the exact new evidence set;
- component/Cartesian/older-contract-only widening rejection;
- post-payload poison invariance;
- explicit zero another-control consumption;
- no newly introduced property `while`/`for` loop;
- no generic public repeatable cursor;
- full previous focused regressions unchanged.

## 8. Clean-candidate and validation protocol

Once all prerequisites are canonical and the actual R3.18AN spec exists:

```text
fresh main
-> re-read target authority/spec
-> inspect duplicate branch/PR/candidate/run/receipt state
-> reconstruct target from fresh canonical parent
-> focused Rust 1.85 validation
-> full mimir-replay/workspace/check/test/clippy/repo verifier
-> audit exact changed-file scope
-> freeze exact candidate SHA/tree/blobs
-> before any PR/run: check equivalent queued/waiting/in_progress run
-> reuse existing equivalent run instead of rerun
-> one validation-only PR if required; DO NOT MERGE
-> close validation PR unmerged after SUCCESS
-> fresh main ancestry audit
-> force=false fast-forward publication
-> exact published-main validation/readback
-> only then canonical Outcome A/closure
```

CI waiting never authorizes duplicate dispatch. Independent target archaeology/tests/spec work should continue while an existing run is active.

## 9. Hard stops preserved by this preparation

This preparation opens **nothing**. In particular it does not open:

- any post-AK payload production;
- another property-control bit;
- false success semantics;
- a repeated/generalized property loop;
- a generic property cursor;
- alternate unobserved payload layout;
- next actor/frame/lifecycle behavior;
- raw state, events, replay slices, skills, counterfactual execution, runtime or export behavior;
- Cargo/dependency/support/corpus expansion.

## 10. Rebase/reconstruction rule

This preparation branch is based on `f20f529e...` only because that was fresh `main` when the safe preparation began. It must **not** become a production publication base if canonical prerequisites advance main.

When R3.18AN becomes executable:

- fetch fresh `main`;
- verify the complete prerequisite authority chain;
- discard stale candidate assumptions;
- deterministically reconstruct the clean target candidate from the then-current canonical parent.

## 11. Current preparation decision

```text
RESULT  = dependency-gated preparation complete
OUTCOME = N/A; no canonical target pass has executed
PRODUCTION MUTATION = 0
CANONICAL MAIN MUTATION BY THIS SLOT = 0
CAPABILITY WIDENING = 0
TARGET CLOSED = false
```

The next safe action is to reuse the canonical R3.18AK/AL/AM results as they appear, then read the actual R3.18AN execution spec before writing any production code.
