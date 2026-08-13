# MIMIR — Next Chat Handoff

Bu dosyadaki prompt yeni bir ChatGPT/Codex konuşmasına doğrudan verilebilir.

---

# Copy/paste prompt

```text
MIMIR projesine mevcut GitHub gerçeğinden devam ediyoruz.

Repository:
Naveax/MIMIR

ÖNEMLİ:
Önce fresh GitHub main'i kontrol et. Eski chat hafızası, historical executor_next dosyaları veya geçmiş planning artifacts current capability'yi override edemez.

Zorunlu okuma sırası:
1. MIMIR_CONTINUE_HERE.md
2. MIMIR_KNOWLEDGE_GRAPH.md
3. docs/continuity/MIMIR_CONTINUITY_STATE.json
4. docs/continuity/MIMIR_CURRENT_STATE.md
5. docs/continuity/MIMIR_R3_14A_DECISION.md
6. docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md
7. docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md
8. docs/continuity/MIMIR_PASS_PROTOCOL.md
9. docs/continuity/MIMIR_BOUNDARY_LOCKS.md
10. docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md
11. docs/continuity/MIMIR_PROGRESS_LEDGER.md
12. MIMIR_ALL_SOURCES_SUPERBOOK.md
13. docs/chatgpt-archive/README.md
14. docs/chatgpt-archive/SOURCE_REGISTRY.md
15. docs/chatgpt-archive/VALIDATION_MATRIX.md
16. docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md

Authority order:
current source/tests
> exact-SHA evidence
> MIMIR_CONTINUE_HERE current override
> structured continuity state
> admitted decision / active pass specs
> boundary locks
> archive/superbook/history

Current production code checkpoint:
ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
R3.13 — static replay network lookup plan.

R3.14 read-only audit:
COMPLETE.

R3.14A:
COMPLETE / Outcome A — evidence sufficient.

Exact R3.14A evidence identity:
- production SHA: ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
- evidence head: f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
- pinned Boxcars SHA: c70e77df7af81b436cb545d070bb90c82f562d0b
- supported replay lane: 47 / 47
- selector manifest SHA256: 28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
- artifact ZIP SHA256: d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
- oracle parse success: 47 / 47
- schema_errors: 0
- bit_offset_monotonicity_failures: 0
- production mutation: 0

Observed common first-envelope cursor across all 47 supported replays:
- time + delta: bits 0..64
- actor_present: bit 64
- actor_id: bits 65..76
- alive: bit 76
- new: bit 77
- R3.14A hard stop: bit 78

Current observed actor-ID bounded decode in these 47 first-envelope vectors:
- bound = 2047
- low_width = 10
- bits_consumed = 11
- extra discriminator consumed in 47 / 47
- extra discriminator value = 0 in 47 / 47
- actor_id = 0 in 47 / 47

R3.14B:
COMPLETE / contract admitted.

Contract summary:
- one private/internal LSB-first network bit cursor
- read_bit / bounded read_bits behavior
- exact cursor position accounting
- atomic fail-closed truncation behavior
- one canonical Rocket League bounded-u32 primitive
- no independent ad-hoc actor-ID helper
- no actor semantics in primitive layer

ACTIVE EXACT PASS:
R3.14C — native bit cursor + bounded integer primitive implementation.

Read and obey:
docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md

R3.14C source scope:
- production Rust source allowed only in crates/mimir-replay/src/lib.rs unless the exact spec explicitly says otherwise
- focused tests in the same crate are allowed
- no Cargo dependency change
- no external parser dependency
- no support-lane expansion

R3.14C must implement only:
- private/internal network bit cursor
- private/internal canonical bounded-u32 primitive
- focused synthetic + oracle-derived tests

R3.14C HARD STOP:
- no ReplayNetworkFirstActorEnvelope production result type
- no actor_present/actor_id/alive/new replay-envelope parser
- no name_id
- no unnamed post-name bit
- no object_id
- no spawn trajectory payload
- no property loop
- no stream_id production decode path
- no attribute payload decode
- no actor lifecycle mutation
- no multi-actor iteration
- no multi-frame iteration
- no raw state
- no events
- no replay slices / skills

Important bounded integer rule:
Do not implement bounded integers as fixed-width read_bits(width). Use the exact low-bits + value/bound-dependent discriminator algorithm admitted in R3.14B. Failure must not partially advance the cursor.

Actor lifecycle anti-regression retained from earlier evidence:
- duplicate actor ID alone is NOT malformed
- same actor ID + NewActor + same class overwrite observed 141,511 times
- class-changing overwrite observed 0 times in the admitted supported evidence

Process:
1. fresh main SHA
2. verify no production drift past the continuity checkpoint
3. inspect active R3.14C spec and current mimir-replay source/tests
4. create an implementation branch from fresh main
5. implement only primitive scope
6. focused tests
7. full required validation / CI with fail-fast native exit propagation
8. audit diff against hard stop
9. reconstruct/publish clean exact source change only
10. force-free publication to fresh main
11. exact published-main readback/CI
12. only after true admission update continuity + knowledge graph

If fresh main already contains a newer admitted production milestone, stop using R3.14C as current and first repair continuity from repo truth.

Do not repeat R3.14A oracle work unless current evidence identity is disproven.
Do not skip to R3.14D/full actor decoder.
```

---

# Interpretation notes

Repository is fixed as `Naveax/MIMIR`; do not ask the user to repeat it.

Historical header/body/footer/static-network work is already closed. In particular, do not restart:

```text
fixture_003 BoolProperty work
three-fixture header closure
source materialization planning
body boundary discovery
content/footer scaffold discovery
footer lookup materialization
attribute-tag registry
spawn-trajectory registry
R3.13 static lookup plan
R3.14 read-only order audit
R3.14A oracle evidence
R3.14B contract admission
```

A historical document saying “network parsing unimplemented” must be interpreted by layer. Structural/body/footer/static lookup work exists; the native actor-envelope reader still does not.

If continuity is stale, current code/tests and exact-SHA evidence win. Repair the control plane forward; do not roll code backward to make docs look consistent.

If the user only says “devam et”, default behavior is:

```text
fresh main
→ mandatory graph reading order
→ active pass verification
→ execute the first unfinished canonical pass
→ admit only after exact validation
→ update continuity + knowledge graph
```
