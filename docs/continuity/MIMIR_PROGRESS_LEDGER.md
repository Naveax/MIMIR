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

