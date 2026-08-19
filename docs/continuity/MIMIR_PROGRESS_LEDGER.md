# MIMIR — Progress Ledger

**Policy:** append-only milestone ledger.
Do not rewrite old entries to make history prettier. If an earlier entry is later found wrong, append a correction entry.

---

# How to append a milestone

Use this template:

```text
## YYYY-MM-DD — PASS_ID — TITLE
Production base SHA:
Production commit SHA:
Pass type:
Outcome:

What changed:
- ...

Evidence:
- ...

Validation:
- ...

Boundaries opened:
- ...

Boundaries still closed:
- ...

Important negative facts / anti-regressions:
- ...

Next exact pass:
- ...
```

A docs-only continuity sync commit is not a production milestone; it may be mentioned under the milestone it documents.

---

# Condensed historical baseline

The detailed historical record remains in existing `docs/` and `executor_*` artifacts. This ledger intentionally starts with a condensed continuity baseline rather than duplicating hundreds of old pass files.

## Historical replay-header foundation

MIMIR progressed from an explicit unsupported replay-reader boundary into narrow real replay parsing through evidence-driven exact version/build admission.

Important retained principles:

- no fake `ReplayHeader` success;
- exact support before broad wildcard support;
- `ReplayInput::Memory` as the narrow parser carrier;
- structural evidence separated from parser success;
- malformed/error boundaries tested;
- header/body/network layers opened in separate passes.

The old fixture_001/002/003 implementation plans/checklists are historical now, not the active `next` state.

---

# Replay body/footer/static-network progression

Before R3.13, production progressively admitted:

```text
ReplayBodyBoundaryV1
ReplayContentScaffoldV1
ReplayFooterScaffoldV1
ReplayFooterLookupMaterializationV1
ReplayNetworkTimingPreambleV1
ReplayNetworkAttributeTagV1
ReplayNetworkSpawnTrajectoryV1
```

Key evidence from that progression included:

- checked-in body framing matching corpus structure;
- content scaffold through network payload;
- footer structure through known footer sections;
- observed opaque terminal tail forms;
- raw footer object/name/class-index/net-cache materialization;
- first network timing/precondition evidence;
- conservative attribute tag admission.

These milestones established prerequisites but did not constitute a native network frame decoder.

---

# 2026-08-13 continuity checkpoint — R3.13

## R3.13 — Static replay network lookup plan

**Production commit SHA:** `ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa`
**Commit message:** `Add replay network lookup plan`
**Pass type:** production implementation + differential audit + publication
**Outcome:** closed / production

### What changed

Production added a static network-decoder lookup plan derived from already-admitted header/footer structure.

The plan includes:

- `ReplayNetworkResolvedPropertyV1`;
- `ReplayNetworkObjectLookupV1`;
- `ReplayNetworkLookupPlanV1`;
- object-index lookup table;
- effective inherited stream/property mapping;
- `max_prop_id`;
- `prop_id_bits`;
- separate spawn trajectory table;
- channel/build-derived flags required by later decoder stages.

### Critical negative fact

R3.13 does **not** consume actor/frame network payload bits.

It is static preparation for later decoding.

### Differential evidence

Supported replay lane:

```text
47 replays
```

Attribute update oracle comparison:

```text
3,990,310 / 3,990,310 matched
unresolved_stream = 0
property_object_mismatch = 0
decoded_not_implemented_hits = 0
```

Interpretation:

MIMIR's production registry/hierarchy resolves the same property object IDs as the pinned Boxcars oracle for every checked supported-corpus attribute update.

### Actor lifecycle finding discovered in differential work

Repeated `NewActor` on an already-used actor ID is not automatically malformed.

Observed:

```text
same actor ID, same class overwrite = 141,511
same actor ID, different class overwrite = 0
```

Pinned Boxcars explicitly permits the same-class overwrite behavior.

Anti-regression rule:

```text
DO NOT implement duplicate actor ID => malformed
```

### Boundaries opened

- static per-object network lookup plan;
- inherited stream/property resolution;
- per-object bounded property-ID parameters;
- static spawn trajectory lookup;
- decoder prerequisite flags.

### Boundaries still closed

- native actor bits;
- native frame iteration;
- spawn payload decode;
- property payload decode;
- attribute payload decode;
- actor lifecycle state table;
- raw state;
- events;
- replay-to-skill path.

### Next

Read-only R3.14 format audit.

---

# 2026-08-13 continuity checkpoint — R3.14

## R3.14 — Native bitstream order read-only audit

**Pass type:** read-only format audit
**Production source changed:** no
**Outcome:** sufficient to plan R3.14A

### Exact order established

```text
frame:
  f32 time
  f32 delta

  actor_present bit
  if actor_present:
      bounded actor_id
      alive bit

      if !alive:
          delete

      if alive:
          new bit

          if new:
              version-gated name_id
              1 bit
              object_id
              spawn trajectory
          else:
              property_present bit loop
              bounded stream_id
              attribute payload
```

### Critical bounded integer finding

Actor ID and stream ID use Rocket League's bounded-integer behavior, not a plain constant-width integer read.

Low bits may be followed by a value-dependent discriminator bit. Cursor correctness must therefore be proven before a native envelope reader is trusted.

### Decision

Do not implement the full frame/actor decoder.

Next exact pass:

```text
R3.14A — temporarily instrument pinned Boxcars and collect first-frame + first-actor-envelope-header differential evidence over all 47 supported replays.
```

Evidence stop boundary:

```text
time
delta
actor_present
actor_id
alive
new
STOP
```

---

# Next ledger entry placeholder

## R3.14A — First frame + first actor envelope differential evidence

Status: **NOT YET COMPLETED** at continuity bootstrap.

When completed, append a new dated entry below this line with:

- MIMIR base SHA;
- exact oracle SHA;
- exact 47 replay manifest identity;
- time/delta evidence counts;
- actor_present distribution;
- actor_id bit-consumption range;
- alive/new distribution;
- mismatch/error counts;
- Outcome A/B/C;
- next exact pass.

Do not edit the R3.13/R3.14 entries to smuggle R3.14A results into history.


---

## 2026-08-13 — R3.14A — First frame + first actor envelope differential evidence

Production base SHA: `ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa`
Production commit SHA: unchanged; evidence-only pass
Pass type: pinned-oracle differential evidence
Outcome: **A — evidence sufficient**

What changed:
- no production Rust source changed;
- the exact 47-replay production-supported lane was selected from 103 checked replay files;
- pinned Boxcars was observation-instrumented only through the first actor-envelope `new` bit;
- durable decision recorded in `MIMIR_R3_14A_DECISION.md`.

Evidence:
- evidence head `f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1`;
- Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`;
- selector `103 total / 47 supported / 56 unsupported`;
- 47 unique supported SHA-256 identities;
- selector manifest `28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55`;
- 47/47 oracle full parse success;
- 47/47 first-envelope evidence rows;
- `schema_errors=0`;
- `bit_offset_monotonicity_failures=0`;
- artifact ZIP SHA-256 `d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b`.

Observed first-envelope cursor:
- `time+delta`: bits `0..64`;
- `actor_present`: bit `64`;
- actor ID: bits `65..76`;
- `alive`: bit `76`;
- `new`: bit `77`;
- hard stop: bit `78`.

Bounded actor-ID observation:
- bound 2047;
- low width 10;
- 11 bits consumed in all 47 rows;
- extra discriminator consumed in all 47 rows;
- first actor ID 0 in all 47 rows.

Boundaries opened:
- sufficient evidence for native bit-cursor and bounded-int contract planning only.

Boundaries still closed:
- native production envelope reader;
- name/object/spawn/property/attribute decode;
- actor lifecycle mutation;
- multi-actor / multi-frame;
- raw state / events / skills.

Next exact pass:
- `R3.14B — evidence admission + native bit-cursor / bounded-int contract planning`.

---

## 2026-08-13 — R3.14B — Native bit-cursor / bounded-int contract planning

Production base SHA: `ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa`
Production commit SHA: unchanged; docs/contract pass
Pass type: evidence admission + implementation contract
Outcome: **ADMITTED / COMPLETE**

What changed:
- R3.14A Outcome A was converted into an exact native primitive contract;
- LSB-first bit ordering was fixed;
- cursor position/remaining-bit semantics were fixed;
- failure atomicity was made mandatory;
- bounded integer low/up/discriminator behavior was fixed;
- R3.14C source scope, hard stop, tests, validation, and publication protocol were fixed;
- exact implementation spec created as `MIMIR_R3_14C_EXECUTION_SPEC.md`.

Validation/admission facts:
- no production Rust source change;
- no dependency change;
- actor-envelope production reader remains closed;
- R3.14C is restricted to private primitives plus focused tests.

Boundaries opened:
- private native network bit-cursor primitive implementation;
- private canonical bounded-u32 primitive implementation.

Boundaries still closed:
- production actor envelope/result parsing;
- all fields after the primitive layer;
- all semantic state/event/skill layers.

Next exact pass:
- `R3.14C — native bit cursor + bounded integer primitive implementation`.


---

## 2026-08-13 — Repository hygiene — Cargo lock synchronization / locked verification

Production SHA: `c42836647673cecc47cc9c89908da1de11d8a222`
Pass type: repository reproducibility maintenance
Outcome: **CLOSED / PRODUCTION HYGIENE**

What changed:
- synchronized the pre-existing stale `Cargo.lock` entry so `mimir-cli` records its already-existing `mimir-replay` workspace dependency;
- changed `scripts/verify_repo.ps1` so dependency-resolving Cargo commands run with `--locked`.

Important negative fact:
- this did not widen replay support or add a replay capability;
- it was separated from R3.14C so the replay milestone remained one-source-file only.

---

## 2026-08-13 — R3.14C — Native bit cursor + bounded integer primitive implementation

Production base SHA: `c42836647673cecc47cc9c89908da1de11d8a222`
Production commit SHA: `bad2db9d5043a7a0087a4fab1d278df5f36c7717`
Pass type: narrow production implementation + clean reconstruction + publication
Outcome: **ADMITTED / PRODUCTION**

What changed:
- added private `NetworkBitCursor` to `crates/mimir-replay/src/lib.rs`;
- added LSB-first `read_bit` and `read_bits_le`;
- added one canonical bounded-u32 primitive;
- added atomic truncation/error cursor behavior;
- added 19 focused tests, including all 47 R3.14A actor-ID value/end-bit vectors.

Evidence / validation:
- source Git blob `3ff6c7823f45126595e7e59f7b5fb50980d8234c`;
- source SHA-256 `ac1c2ae2919ad0c5d6d8ea615dd5dac82f4c5e5240f33618ef5e74ef9cb1cb92`;
- validation head `349f20328cef6e7f0a3c46b279a787583442a652`;
- validation artifact SHA-256 `0f64e842d0ced4c5566717954be2a684f6735080e9eb8edac9c03e2218d295d7`;
- focused tests `19/19`;
- oracle actor-ID vectors `47/47` value match and `47/47` end-bit match;
- full mimir-replay regression PASS;
- workspace check/test PASS;
- clippy `-D warnings` PASS;
- corpus + knowledge verifiers PASS;
- clean branch CI run `31698938025` SUCCESS;
- published-main CI run `31699241010` SUCCESS.

Boundaries opened:
- private native network bit cursor;
- private canonical bounded-u32 primitive.

Boundaries still closed:
- first actor-envelope production reader;
- all fields after `new`;
- actor lifecycle state;
- multi-actor / multi-frame;
- raw state / events / skills.

Next exact pass:
- `R3.14D — first actor envelope header native reader`.


---

## 2026-08-13 — R3.14D — First actor envelope header native reader

Production base SHA: `9c0f81a084b2df0e64496af87c0edc50814bcbc6`
Production commit SHA: `7b17cb9033b6c71d476e500380d78402cbb3c56d`
Pass type: narrow production implementation + clean reconstruction + publication
Outcome: **ADMITTED / PRODUCTION**

What changed:
- added native first-frame/first-actor result/reader through `new`;
- consumed timing raw bits through the native cursor and cross-checked timing preamble raw bits;
- used canonical bounded-u32 for actor ID;
- preserved branch-dependent `Option` state and stopped before `name_id`.

Validation:
- 17 focused tests PASS;
- full locked repository verifier PASS;
- source blob `67752868807c0b7169e46f22762c7a0ea9efce40`;
- source SHA-256 `06b767622108ca1aea82ee5c0aad6cc503fbcfddaba05012cf022dd901a5a385`;
- validation artifact SHA-256 `dab3a48ef1b58cbbbd39c832009fc722d047c21f84c12cb4e8f7cc69313a935d`;
- clean CI `31702049792` SUCCESS;
- published-main CI `31702341993` SUCCESS.

Next exact pass: `R3.14E — native first-envelope differential audit`.
---

## 2026-08-13 — R3.14E admitted

- Production base remained `7b17cb9033b6c71d476e500380d78402cbb3c56d`.
- Exact 47 replay identities verified.
- Pinned Boxcars oracle identity verified.
- Native first-envelope exact matches: 47/47 for all required fields and structural context.
- Mismatch/native-error/identity-error: 0/0/0.
- Production source mutation: 0.
- Outcome A admitted.
- Next: R3.15A evidence-only NewActor branch audit.

## 2026-08-17 — R3.18I admitted

- Outcome A, read-only evidence; production unchanged at `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`.
- Evidence `45090a2c18fb517088bb411782bbaed0d7d68199`; workflow `31975063743/95233164711` SUCCESS; same-head CI `31975063703/95233164610` SUCCESS.
- Artifact `9270842140` / `sha256:9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2`; 94/94 exact; 47 terminators + 47 continuations; Int=46/String=1; mismatch 0; third-property bits 0.
- Next exact pass: R3.18J bounded native second-property payload composition.

## 2026-08-17 — R3.18J published

- Outcome A / production `330ab01890a7c09eff1805e437584fb3be0a1134`.
- Exact two-file clean scope: lib + focused R3.18J test.
- Implementation `31975731621/95234808797`, candidate CI `31975907582/95235253244`, published CI `31976100231/95235742210` SUCCESS.
- Exactly one optional second payload is now production; Int plus exact-context String only; following property bit remains closed.
- Next pass: R3.18K published API differential.

## 2026-08-17 — R3.18K published second-payload differential

- Outcome A / read-only evidence closed.
- Production remains `330ab01890a7c09eff1805e437584fb3be0a1134` (R3.18J).
- Authority: `926ddd88331ef0372b17b495cb06502010ab39ac`; evidence `31977860600/95239932737` SUCCESS; same-head CI `31977860563/95239932564` SUCCESS.
- Artifact `9271561853` / `sha256:a455984c1149cb8f186eedb34d3e148fe45b8592c928cd9246d36cd52843262f`.
- 94/94 exact = 47 terminators + 47 continuations; Int=46 / String=1; mismatch 0.
- 47/47 terminator no-lookup and 47/47 real payload truncation controls PASS; wrong context/tag, repeatability, poison PASS.
- Following-property bits consumed 0; witness reselection 0; privacy PASS; mutation `0/0/0/0/0`.
- Next: R3.18L following-property one-bit read-only evidence.

## 2026-08-17 — R3.18L following-property control-bit evidence

- Outcome A / read-only evidence closed; production remains `330ab01890a7c09eff1805e437584fb3be0a1134`.
- Authority `9205ac1616e686589938f952782a32f03d0d1488`; evidence `31978791346/95242213413` SUCCESS; same-head CI `31978791304/95242213357` SUCCESS.
- Artifact `9271817700` / `sha256:db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c`.
- 47/47 published R3.18J reconstructions exact before one-bit observation; control distribution false=0 / true=47; mismatch 0.
- Truncation, repeatability, post-control poison and prior-stop mismatch controls PASS 47/47.
- Following stream/header/payload consumption 0/0/0; witness reselection 0; privacy PASS; mutation `0/0/0/0/0`.
- MIMIR validation used Rust 1.85.0; pinned Boxcars oracle build was isolated to stable rustc 1.90.0 due external transitive dependency MSRV.
- Next: R3.18M true-only bounded after-second-payload control-bit production composition.

## R3.18N — Published Following-Control Differential

- status: **Outcome A / ADMITTED / READ-ONLY**
- production remains `fd74ba8c520ab83b808730572c41e45d6dc616e6`
- evidence `9bbf59745c950b7be5a5a592724f41db80874973` / `32007040663` / `95318554719` SUCCESS
- same-head CI `32007040500` / `95318554225` SUCCESS
- artifact `9280430420` / `sha256:772447a31e174355b3848605357667936ca522777d601dda504896aa0f663102` / 21060 bytes
- frozen 47/47; false=0 true=47; published R3.18M/oracle mismatch=0
- following stream/header/payload/another-control bits consumed 0/0/0/0; reselection=0
- next canonical pass: **R3.18O following-property header evidence**

## 2026-08-17 — R3.18O — Following-property header evidence

Production base SHA: `fd74ba8c520ab83b808730572c41e45d6dc616e6`
Production commit SHA: unchanged
Pass type: read-only evidence / differential
Outcome: **A — ADMITTED / READ-ONLY**

What changed:
- no production code changed;
- the exact frozen 47-row R3.18N lane was extended only through one following existing-actor property header and stopped at `payload_start`.

Evidence:
- evidence `5046e1594b87ce2828db5faa48aceba456c3166f` / `32017369100` / `95349613184` SUCCESS;
- same-head CI `32017369071` / `95349613066` SUCCESS;
- artifact `9284144768` / `25129` bytes / `sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d`;
- artifact inner manifest 11/11 exact;
- R3.18J reconstruction 47/47; published R3.18M control 47/47; following header 47/47; mismatch 0;
- 18 exact structural context tuples over 47 rows; Boolean=39 / ActiveActor=8;
- all 47 rows 868.32/net10; witness reselection 0.

Validation:
- property-present and stream truncation, prior-stop mismatch, wrong actor-stream context, outside-exact-tuple, repeatability and post-payload-start poison controls PASS;
- following payload / another-control bits consumed 0/0;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy PASS.

Boundaries opened:
- evidence support only for the exact 18 observed following-header structural contexts.

Boundaries still closed:
- production composition of that following header;
- any context outside the exact observed tuples;
- following payload, another control, repeated/generalized property loop, next actor/frame/lifecycle and all semantic/runtime layers.

Important negative facts / anti-regressions:
- tag/component membership alone is not support;
- do not cross-product individually observed bounds, widths, object indices or tags;
- Boxcars continuing its own parse after the instrumentation point is not MIMIR observer consumption.

Next exact pass:
- `R3.18P — following-property header exact-context contract`.

## 2026-08-17 — R3.18O immutable receipt correction

Fresh exact-run artifact re-download caught stale receipt values before R3.18P admission. Correct ZIP digest: `e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d`. Exact tuple identities and inner hashes were corrected; aggregate Outcome A facts and production boundary are unchanged. R3.18P remains active and must use corrected authority.

## 2026-08-17 — R3.18P — Following-property header exact-context contract

Production SHA: `fd74ba8c520ab83b808730572c41e45d6dc616e6` (unchanged)
Pass type: contract-only
Outcome: **A — ADMITTED**

- immutable R3.18O authority reverified;
- exact 18 full structural tuples admitted with exact multiplicities summing to 47;
- committed contract SHA-256 `0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b`;
- tag/component-only, Cartesian-product, version-drop and nineteenth-tuple widening remain rejected;
- no production/Cargo/fixture/corpus/support mutation.

Next exact pass: **R3.18Q bounded following-property header production composition**; hard stop remains following `payload_start`.

## 2026-08-17 — R3.18Q — bounded following-property header production — Outcome A

- Published production `f41c59d26ed6c810a640b4fa8cd76129decb32aa` / tree `606db4b5778e5218f2bd0117cc5dd72d7f3e37a5`; parent `1a3f89e7256c7c7ff4bf6b747a434504f1f2e572`.
- Authority `32026722346/95377559363` SUCCESS; exact-candidate CI `32027055064/95378560725` SUCCESS; published-main CI `32027421491/95379649817` SUCCESS.
- Clean scope: `crates/mimir-replay/src/lib.rs` + `crates/mimir-replay/tests/r3_18q_following_header.rs` only.
- R3.18P exact contract `0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b`; 18 exact contexts; 47/47 frozen production compositions exact.
- Q/R3.18M control equality 47/47; Q/stateless-header equality 47/47; following payload / another-control consumption 0/0.
- Opened R3.18R read-only published-API differential; production frozen.


---

## 2026-08-17 — R3.18R — Published following-property header differential
Production base SHA: `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
Production commit SHA: unchanged (`f41c59d26ed6c810a640b4fa8cd76129decb32aa`)
Pass type: read-only differential evidence
Outcome: A — admitted

What changed:
- No production code changed. Canonical continuity records the completed published-Q differential and opens R3.18S read-only following-payload discovery.

Evidence:
- authority head/tree `47bf441f2c795702e4ee75c66b4dbe710ccc9a9c` / `0dd95a0f8d4e8729191176d1e2614cbafd75d80e`; run/job `32044430149/95429267025` SUCCESS;
- artifact `9292549978` / `18820` bytes / `sha256:142a2480f38a7ddc4f74e73dd9ce84ed70ccd740645f05d2e90579825927220f`;
- published-Q rows 47/47; R3.18M control equality 47/47; stateless-header equality 47/47;
- exact R3.18P contexts 18/18 and multiplicities 47/47; native/oracle mismatch 0;
- Boolean=39, ActiveActor=8, all 868.32/net10; witness reselection 0;
- following payload / another-control consumption 0/0; privacy PASS.

Validation:
- same-head normal CI `32044430126/95429266690` SUCCESS;
- Q truncation, wrong actor, unresolved lookup, wrong version, repeatability and post-payload poison controls 47/47;
- fabricated Cartesian and component/tag/version widening negatives PASS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.

Boundaries opened:
- read-only R3.18S may investigate exactly one following payload on the frozen 47-row lane.

Boundaries still closed:
- production following-payload composition; another property control; repeated/generalized loops/cursors; next actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening.

Important negative facts / anti-regressions:
- Boolean=39 and ActiveActor=8 are observed tag counts, not payload-width or semantic contracts.
- R3.18R consumed zero payload and zero later-control bits.

Next exact pass:
- R3.18S — following-property payload contract / evidence discovery.


---

## 2026-08-17 — R3.18S — Following-property payload contract / evidence
Production base SHA: `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
Production commit SHA: unchanged (`f41c59d26ed6c810a640b4fa8cd76129decb32aa`)
Pass type: read-only payload-boundary/semantic evidence
Outcome: A — admitted

What changed:
- No production code changed. The exact frozen 47-row following-payload lane was independently compared against pinned Boxcars and existing MIMIR lower-level decoders.

Evidence:
- authority head/tree `7fed9a90d2cb1e356b2a388503650b434d7f3f87` / `c552e5ef2cb8e7d1cb3b4022b3ff1ec6dc763989`; run/job `32047433925/95438466699` SUCCESS;
- artifact `9293436309` / `18955` bytes / `sha256:dac07647e288bfc3b177000e1bfa6b9cfd892b80fd77d46c2f4974a3832cf422`;
- 47/47 rows and 18/18 exact R3.18P contexts; witness reselection 0; native/oracle mismatch 0;
- Boolean 39 rows × 1 bit; ActiveActor 8 rows × 33 bits;
- repeatability, truncation, wrong-decoder, wrong-exact-context and post-payload/next-control poison invariance 47/47;
- another-control bits consumed 0; privacy PASS.

Validation:
- same-head normal CI `32047433876/95438466663` SUCCESS;
- artifact ZIP digest matched GitHub artifact digest; all nine inner manifest entries verified;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.

Important negative fact:
- Boolean and ActiveActor are total fixed-width value domains; there is no invalid complete 1-bit/33-bit pattern to fabricate. Truncation is the structural malformed-payload control.

Boundaries opened:
- R3.18T may attempt bounded production composition of exactly one Boolean|ActiveActor following payload.

Boundaries still closed:
- another property control/header/payload; repeated/generalized loops/cursors; context widening; next actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening.

Next exact pass:
- R3.18T — bounded following-property payload production composition.


---

## 2026-08-17 — R3.18T — Bounded following-property payload production composition
Production base SHA: `ac1b284099a01be895c3e9d644a9d98b6dfe3da2`
Production commit SHA: `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b`
Pass type: production implementation
Outcome: A — published

What changed:
- Added exactly one public bounded composition for the following payload after R3.18Q.
- Reused existing primitive-scalar Boolean and K2 ActiveActor decoders; no duplicate wire decoder or generic loop was introduced.

Authority / validation:
- implementation `32049639448/95445637593` SUCCESS;
- clean-candidate CI `32049893219/95446478223` SUCCESS;
- PR #23 CI `32050205389/95447503058` SUCCESS;
- published-main CI `32050650336/95448937493` SUCCESS;
- lib/test blobs `cf992670b461e9d923e773ed375bef2b42aea20d` / `430676ec118fa0755a9c64abc0067bf5c5c88d05`; tree `a6f27fe606cd3446da02ef1cb8cf53fff071e383`.

Clean scope:
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/tests/r3_18t_following_payload.rs`
- Cargo/lock/fixture/corpus/docs/support mutation 0/0/0/0/0/0.

Admitted behavior:
- Boolean exactly 1 bit; ActiveActor exactly 33 bits; exact nested R3.18P context remains mandatory; stop exactly at one payload end; another-control bits consumed 0.

Boundaries still closed:
- another property control/header/payload; generalized property loops/cursors; context/tag widening; next actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening.

Next exact pass:
- R3.18U — published R3.18T following-payload differential on the immutable R3.18S 47-row lane.

## R3.18U — Published R3.18T following-payload differential — Outcome A / CLOSED

- Production unchanged: `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b` / tree `a6f27fe606cd3446da02ef1cb8cf53fff071e383`.
- Final evidence head/tree: `a53d0c8b4c88bab229e5ac9ec2db7dda5f9400b4` / `f0c716278ef47665e43572d0129c4e8acd9be182`.
- Authority: `32055189778 / 95463604513` SUCCESS; same-head CI `32055189737 / 95463604366` SUCCESS.
- Artifact: `9296199852` / `20181` bytes / `sha256:13262328812bc56c9ea58bbc42364308fb6c65487c51f062296b14993f3a626e`; ZIP digest and internal SHA-256 manifest verified.
- Exact lane: 47/47 rows, 18/18 R3.18P contexts, Boolean=39×1 bit, ActiveActor=8×33 bits.
- Published-T/frozen-S mismatch 0; embedded header identity 47/47; witness reselection 0.
- Repeatability, truncation, wrong actor, unresolved lookup, wrong context, fabricated context and post-payload poison controls: 47/47.
- Another-control consumption 0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.
- Superseded initial attempt failed only on transient GitHub artifact-download HTTP 503 before semantic evidence; final authority used unchanged evidence criteria with bounded transport retry.
- Next pass opened: R3.18V, read-only exactly-one-next-property-control-bit evidence.

## R3.18V — Next property-control bit evidence — Outcome A / CLOSED

- Production unchanged: `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b` / tree `a6f27fe606cd3446da02ef1cb8cf53fff071e383`.
- Evidence head/tree: `2b0c9f01559e77a6fdf21a097b8ab4d1a27b6ff5` / `229b3d68a82f6dadc19518614e27ff09e8006ad2`.
- Authority `32057732310 / 95471639989` SUCCESS; same-head CI `32057732335 / 95471640230` SUCCESS.
- Artifact `9297068554` / `20484` bytes / `sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2`; ZIP digest and 11-entry internal manifest verified.
- Published R3.18T reconstruction exact 47/47.
- One-bit distribution discovered without filtering: false=0 / true=47; pinned Boxcars vs independent read mismatch 0.
- Truncation, repeatability, prior-stop mismatch and post-control poison: PASS 47/47.
- Next stream/header/payload/second later control consumption 0/0/0/0; witness reselection 0.
- Production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.
- Next pass opened: R3.18W true-only bounded production control composition.

## 2026-08-17 — R3.18W production published / R3.18X opened

- Outcome A production: `58872e94f00ef094807f21ab2ff984ac66b97d91` / tree `d6965d77903ea99dad0465bb350b6a673ee7dd00`; parent `49011a8be77e59b1834c0ecbb648ee6d699ca6c8`.
- Exact clean scope: `crates/mimir-replay/src/lib.rs` + `crates/mimir-replay/tests/r3_18w_following_payload_control.rs`.
- Authority `32060501395/95480474127`, clean candidate CI `32062120856/95485540552`, PR #27 CI `32062533181/95486877308`, published CI `32062965119/95488256583` all SUCCESS.
- R3.18W validates one exact R3.18T following-payload end, reads exactly one LSB-first control bit, admits true only, rejects false, and stops one bit later.
- R3.18V frozen evidence remains `9297068554` / `sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2` with 47 true, 0 false and adjacent consumption 0/0/0/0.
- Production/Cargo/fixture/corpus/docs/support mutation outside the two-file clean production scope: 0/0/0/0/0/0.
- Opened R3.18X as a separate read-only published-W differential on exactly the same 47 V witnesses.

## 2026-08-17 — R3.18X Outcome A admitted / R3.18Y opened

- R3.18X authority `32065498170/95496521378` SUCCESS on exact evidence head `75259a9b3705b16b21d89b975ee584a7765e8134` / tree `fe90b38c98039cd1dde05b96613645d0ab69a8a9`.
- Same-head normal CI `32065498109/95496518762` SUCCESS.
- Artifact `9299790869` / 19761 bytes / `sha256:ac32daa92d88f1753da34123d074dcd8f3c98c58fdeb0b91f89cb837ea02ebff`; ZIP digest exact; 8/8 internal manifest payload hashes PASS.
- Frozen rows 47/47; true=47 false=0; published T exact 47/47; published W vs frozen V mismatch 0.
- Repeatability/truncation/false/prior-boundary/post-stop-poison negatives 47/47; adjacent stream/header/payload/second-control 0/0/0/0.
- Witness reselection 0; privacy PASS; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.
- Opened R3.18Y as separate read-only one-header discovery. No P-contract inheritance by assumption; no payload or another control.


## 2026-08-18 — R3.18Y Outcome A admitted; R3.18Z opened

- Y evidence head/tree: `413d6c24f8f390a57c21ed345f3f868c263f413c` / `c48630bf89c23a8348936f2adbb8f0c9ad0c977b`.
- Authority `32076198677/95529856476` SUCCESS; same-head normal CI `32076881407/95531867271` SUCCESS via CI-only PR #30, closed without merge.
- Immutable artifact `9303584468` / `19642` / `sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29`; 9/9 manifest payloads verified and ZIP digest exact.
- Exact result: 47/47 rows; 18 complete seven-field contexts; multiplicity sum 47; ActiveActor=39, Int=7, UniqueId=1; native/oracle mismatch 0; witness reselection 0.
- All structural negatives 47/47; following payload bits 0; another-control bits 0; R3.18P inheritance assumed 0; privacy PASS; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.
- Production remains R3.18W `58872e94f00ef094807f21ab2ff984ac66b97d91`. R3.18Z is contract-only and may admit only exact tuple membership.


## 2026-08-18 — R3.18Z Outcome A admitted; R3.18AA opened

- Production unchanged: `58872e94f00ef094807f21ab2ff984ac66b97d91` / `d6965d77903ea99dad0465bb350b6a673ee7dd00`.
- Boundary-specific contract: `MIMIR_R3_18Z_ADMITTED_HEADER_CONTEXTS.json` / `sha256:81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9`.
- Exact membership: 18 complete seven-field tuples; multiplicity sum 47; ActiveActor=39 / Int=7 / UniqueId=1.
- Frozen Y authority `413d6c24f8f390a57c21ed345f3f868c263f413c` / `32076198677/95529856476` SUCCESS; same-head CI `32076881407/95531867271`; artifact `9303584468` / `sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29`.
- R3.18P historical contract `0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b` was not inherited; P-valid/Z-absent tuple `(60,5,102,Boolean,868,32,10)` is rejected.
- Tag-only, component-only, Cartesian, versionless, nineteenth-tuple and cross-boundary negatives PASS.
- Production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.
- Opened R3.18AA for exactly one Z-admitted post-W header through payload_start only.

## 2026-08-18 — R3.18AA production published; R3.18AB opened

- Outcome A production: `9392240c49f95766c214afee9865fed4155a87a4` / tree `968520d480f78c528086e4e31b2ce307f4f8d232`; parent `ac24d29edeacd04152afe318e25ae296385159c3`.
- Clean production scope: `crates/mimir-replay/src/lib.rs` + `crates/mimir-replay/tests/r3_18aa_post_w_following_header.rs`; blobs `46523f47f94231362b60f8aee038e943e41c7972` / `7df8f84af37d771b12da1334bd195634e4cc6a54`.
- R3.18Z authority: `sha256:81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9`; exact_tuple_only 18 contexts / multiplicity 47; R3.18P inheritance false.
- Builder `32142503228/95728286216`, clean candidate CI `32143161309/95730448274`, published-main CI `32143631391/95731995111` all SUCCESS.
- Focused R3.18AA tests 5/5 PASS; full repository/workspace/clippy verification PASS.
- Production behavior: one valid W true control -> exactly one stateless following header -> exact Z tuple gate -> stop at payload_start.
- Real ActiveActor/Int/UniqueId representatives PASS; truncation/wrong actor/wrong version/Cartesian/P-only-Z-absent/repeatability/post-payload-poison negatives PASS.
- Following payload / another-control consumption 0/0; no loop/cursor; Cargo/docs/workflow/fixture/corpus/support mutation outside clean production scope 0.
- Opened R3.18AB as a separate read-only published-AA differential on the exact immutable 47-row Y lane.

---

## 2026-08-19 — R3.18AB — Published R3.18AA post-W following-header differential

Production SHA: `9392240c49f95766c214afee9865fed4155a87a4` / tree `968520d480f78c528086e4e31b2ce307f4f8d232`
Pass type: read-only published-production differential
Outcome: **A — ADMITTED / CLOSED**

Evidence:
- exact frozen R3.18Y lane 47/47, witness reselection 0;
- authority head/tree `b2f4b73600165b2d83389b6ce43709b64beba52a` / `8d36c8c7118db8c6f0d28c4ae88e0400cf4a3cd1`;
- authority run/job `32230919566/96000311036` SUCCESS; same-head CI `32230919652/96000311479` SUCCESS;
- artifact `9357559410` / `12607` bytes / `sha256:4b6d72b154440ee2b819f5a5ecb6fa3768e086b7ec4ba0d0c53d0e8e3ad23d99`; downloaded ZIP digest exact and inner manifest 9/9 PASS;
- published-AA/frozen-Y/direct-native mismatch 0; Z contexts 18/18; multiplicities 47/47; ActiveActor=39 / Int=7 / UniqueId=1;
- repeatability, truncation, wrong actor, unresolved lookup, wrong version and post-payload poison 47/47; Cartesian and R3.18P-valid/Z-absent negatives retained by focused suite;
- following-payload/another-control bits 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.

Superseded attempt:
- `f2f79e47fefbe7ee95ea5df84c78a86868f57bb3` / `32229955227/95997443235` failed only because a byte-prefix truncation harness cut at `payload_start / 8`, leaving complete header bytes on 8 unaligned rows; positive/equality checks were already 47/47. Corrected authority uses a prefix before the post-W control/header byte. Production was never changed.

Boundaries opened:
- R3.18AC read-only ordinal-3 following-property payload evidence only.

Boundaries still closed:
- post-AA payload production composition; another property control; loops/cursors; next actor/frame; semantic/runtime/export widening.

Next exact pass:
- `R3.18AC — post-AA following-property payload real-replay evidence`.
