from __future__ import annotations

import json
from pathlib import Path

PROD = "bad2db9d5043a7a0087a4fab1d278df5f36c7717"
BASE = "c42836647673cecc47cc9c89908da1de11d8a222"


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


# 1. Root continuation handbook: append newest override, preserve old history.
path = "MIMIR_CONTINUE_HERE.md"
text = read(path)
marker = "## R3.14C PRODUCTION ADMITTED / ACTIVE R3.14D"
if marker in text:
    raise SystemExit("continue-here R3.14C marker already present")
text += f"""

---

## R3.14C PRODUCTION ADMITTED / ACTIVE R3.14D

> **CURRENT OVERRIDE:** This section supersedes earlier R3.14C `ACTIVE` wording in this historical continuation file. Fresh code/tests and exact-SHA evidence still outrank prose.

Current exact state:

```text
main / last production code SHA = {PROD}
production milestone            = R3.14C — private native network bit cursor + bounded-u32 primitive
R3.14A                          = COMPLETE / Outcome A
R3.14B                          = COMPLETE / contract admitted
R3.14C                          = COMPLETE / PRODUCTION
ACTIVE NEXT PASS                = R3.14D — first actor envelope header native reader
```

R3.14C durable decision:

```text
docs/continuity/MIMIR_R3_14C_DECISION.md
```

R3.14C clean production identity:

```text
pre-pass main              = {BASE}
production SHA             = {PROD}
source file                = crates/mimir-replay/src/lib.rs
source Git blob            = 3ff6c7823f45126595e7e59f7b5fb50980d8234c
source SHA256              = ac1c2ae2919ad0c5d6d8ea615dd5dac82f4c5e5240f33618ef5e74ef9cb1cb92
clean branch CI            = 31698938025 SUCCESS
published-main CI          = 31699241010 SUCCESS
```

Validation evidence:

```text
focused tests              = 19 PASS
R3.14A actor-id vectors    = 47/47 value match
R3.14A end-bit vectors     = 47/47 match
mimir-replay regression    = PASS
workspace check/test       = PASS
clippy -D warnings         = PASS
corpus verifier            = PASS
knowledge verifier         = PASS
Cargo locked               = PASS
hard-stop source scope     = PASS
```

What R3.14C opened:

```text
private NetworkBitCursor
private LSB-first read_bit/read_bits_le
private canonical read_bounded_u32
atomic truncation/error cursor behavior
```

What R3.14C did NOT open:

```text
actor-envelope production result
actor_present/actor_id/alive/new replay reader
name_id/object/spawn/property/stream/attribute payloads
actor state
multi-actor
multi-frame
raw state/events/skills
```

The exact R3.14D execution spec is:

```text
docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md
```

R3.14D may consume only:

```text
first frame time raw/value
first frame delta raw/value
actor_present
bounded actor_id if present
alive if present
new if alive
STOP
```

Hard stop remains before `name_id` and everything after it. R3.14D implementation is not the 47-replay differential admission; that remains R3.14E.

Repository hygiene note: before R3.14C, stale `Cargo.lock` state was repaired separately at `{BASE}` and `scripts/verify_repo.ps1` now enforces Cargo `--locked`. This is reproducibility maintenance, not replay capability expansion.
"""
write(path, text)


# 2. Human current state: update top identity and append latest admitted state.
path = "docs/continuity/MIMIR_CURRENT_STATE.md"
text = read(path)
text = replace_once(
    text,
    "**Production code checkpoint:** `ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa`",
    f"**Production code checkpoint:** `{PROD}`",
    "current-state production sha",
)
text = replace_once(
    text,
    "**Production milestone:** `R3.13 — static replay network lookup plan`",
    "**Production milestone:** `R3.14C — private native network bit cursor + bounded-u32 primitive`",
    "current-state production milestone",
)
text = replace_once(
    text,
    "**Next exact pass:** `R3.14C — native bit cursor + bounded integer primitive implementation`",
    "**Next exact pass:** `R3.14D — first actor envelope header native reader`",
    "current-state next pass",
)
marker = "# 18. R3.14C production admission / R3.14D active"
if marker in text:
    raise SystemExit("current-state R3.14C marker already present")
text += f"""

---

# 18. R3.14C production admission / R3.14D active

R3.14C is now a production milestone at:

```text
{PROD}
```

Production now contains one private/internal LSB-first network bit cursor and one canonical bounded-u32 decoder with atomic failure behavior. The primitive passed 19 focused tests and all 47 R3.14A actor-ID value/end-bit vectors, then full locked repository validation, clean reconstruction, force-free publication, and published-main CI.

Durable decision:

```text
docs/continuity/MIMIR_R3_14C_DECISION.md
```

The first actor-envelope reader is still not production capability. It is the active next pass:

```text
R3.14D — first actor envelope header native reader
docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md
```

R3.14D opens only the first frame timing pair and one first actor header through `new`, then stops. The 47-replay native-vs-Boxcars admission remains R3.14E.

Current one-line truth:

> **MIMIR now has native private network bit primitives in production, but it still does not have an admitted actor-envelope reader; the next exact pass is R3.14D and the hard stop remains immediately after the first actor `new` bit.**
"""
write(path, text)


# 3. Machine-readable state.
path = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(path))
state["last_production_code_sha"] = PROD
state["last_production_milestone"] = "R3.14C"
state["last_production_milestone_name"] = "private native network bit cursor + bounded-u32 primitive"
state["current_pass"] = "R3.14D"
state["current_pass_kind"] = "narrow production implementation: first frame + first actor envelope header native reader"
state["current_pass_goal"] = "Use the admitted private R3.14C bit cursor and bounded-u32 primitive to natively read first-frame time/delta and one first actor envelope through actor_present, actor_id, alive, and new, then stop."
state["current_pass_stop_boundary"] = "Stop immediately after actor_present when false, alive when false, or new when alive. Never consume name_id, the post-name bit, object_id, spawn payload, property loop, stream_id, attribute payload, second actor, second frame, raw state, events, or skills."
state["r3_14c"] = {
    "outcome": "admitted / production",
    "pre_pass_main_sha": BASE,
    "production_sha": PROD,
    "production_tree": "88057e47c96d98e6034e8066f320de2ebebef912",
    "source_file": "crates/mimir-replay/src/lib.rs",
    "source_git_blob": "3ff6c7823f45126595e7e59f7b5fb50980d8234c",
    "source_sha256": "ac1c2ae2919ad0c5d6d8ea615dd5dac82f4c5e5240f33618ef5e74ef9cb1cb92",
    "focused_tests": 19,
    "oracle_vector_rows": 47,
    "oracle_vector_value_match": "47/47",
    "oracle_vector_end_bit_match": "47/47",
    "validation_head_sha": "349f20328cef6e7f0a3c46b279a787583442a652",
    "validated_bot_sha": "8ccd629f9e6eba749b234afe0a80b2b4df7eca7d",
    "validation_artifact_id": 9180345101,
    "validation_artifact_sha256": "0f64e842d0ced4c5566717954be2a684f6735080e9eb8edac9c03e2218d295d7",
    "clean_branch_ci_run": 31698938025,
    "published_main_ci_run": 31699241010,
    "private_bit_cursor_in_production": True,
    "canonical_bounded_u32_in_production": True,
    "actor_envelope_reader_in_production": False,
}
state["repository_hygiene"] = {
    "cargo_lock_sync_sha": BASE,
    "cargo_lock_stale_dependency_repaired": "mimir-cli -> mimir-replay",
    "verify_repo_cargo_locked": True,
    "capability_expansion": False,
}
state["next_files_to_read"] = [
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_R3_14A_DECISION.md",
    "docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md",
    "docs/continuity/MIMIR_R3_14C_DECISION.md",
    "docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md",
    "docs/continuity/MIMIR_PASS_PROTOCOL.md",
    "docs/continuity/MIMIR_BOUNDARY_LOCKS.md",
    "docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md",
    "docs/continuity/MIMIR_PROGRESS_LEDGER.md",
]
write(path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


# 4. Append-only progress ledger.
path = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
text = read(path)
marker = "## 2026-08-13 — R3.14C — Native bit cursor + bounded integer primitive implementation"
if marker in text:
    raise SystemExit("R3.14C ledger entry already present")
text += f"""

---

## 2026-08-13 — Repository hygiene — Cargo lock synchronization / locked verification

Production SHA: `{BASE}`
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

Production base SHA: `{BASE}`
Production commit SHA: `{PROD}`
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
"""
write(path, text)


# 5. Boundary locks: append newest current override.
path = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
text = read(path)
marker = "## CURRENT OVERRIDE — At R3.14D"
if marker in text:
    raise SystemExit("R3.14D boundary override already present")
text += f"""

---

## CURRENT OVERRIDE — At R3.14D

R3.14C is now OPEN / PRODUCTION at `{PROD}` for only:

```text
private LSB-first NetworkBitCursor
private read_bit / read_bits_le
private canonical bounded-u32 primitive
```

R3.14D is the active narrow implementation boundary:

```text
first frame time + delta
first actor_present
bounded actor_id if present
alive if present
new if alive
STOP
```

Still CLOSED:

```text
name_id
post-name one-bit field
object_id
spawn payload
property_present loop
stream_id production path
attribute payload
second actor
second frame
actor lifecycle mutation
raw state
events
skills
```

R3.14D implementation does not by itself close the oracle differential requirement. `R3.14E` remains required before R3.15.
"""
write(path, text)


# 6. Roadmap current pointer/status.
path = "docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md"
text = read(path)
text = replace_once(text, "**Scope:** from current R3.14C checkpoint to the full MIMIR target architecture", "**Scope:** from current R3.14D checkpoint to the full MIMIR target architecture", "roadmap scope")
text = replace_once(text, "**Current production checkpoint:** R3.13 static network lookup plan", "**Current production checkpoint:** R3.14C private native bit cursor + bounded-u32 primitive", "roadmap production")
text = replace_once(text, "**Current next pass:** R3.14C native bit cursor + bounded integer primitive implementation", "**Current next pass:** R3.14D first actor envelope header native reader", "roadmap next")
text = replace_once(text, "# C. R3.14C — Native bit cursor + bounded integer primitive implementation — ACTIVE", "# C. R3.14C — Native bit cursor + bounded integer primitive implementation — COMPLETE / PRODUCTION", "roadmap C status")
text = replace_once(text, "# D. R3.14D — First actor envelope header native reader", "# D. R3.14D — First actor envelope header native reader — ACTIVE", "roadmap D status")
write(path, text)


# 7. Continuity README current exact spec pointers.
path = "docs/continuity/README.md"
text = read(path)
text = replace_once(
    text,
    "### `MIMIR_R3_14C_EXECUTION_SPEC.md`\n**Şu anda yapılacak exact pass.** Private native bit cursor + bounded integer primitive implementation only; no actor-envelope reader yet.",
    "### `MIMIR_R3_14C_DECISION.md`\nCompleted R3.14C production admission for the private native bit cursor and canonical bounded-u32 primitive.\n\n### `MIMIR_R3_14D_EXECUTION_SPEC.md`\n**Şu anda yapılacak exact pass.** First frame + one first actor-envelope header through `new`, then hard stop before `name_id`.",
    "continuity README active spec",
)
text = replace_once(text, "R3.14C'den full MIMIR hedef mimarisine kadar uzun vadeli sıra", "R3.14D'den full MIMIR hedef mimarisine kadar uzun vadeli sıra", "continuity README roadmap")
write(path, text)


# 8. Superbook current admission update.
path = "MIMIR_ALL_SOURCES_SUPERBOOK.md"
text = read(path)
marker = "## CURRENT REPLAY DECODER ADMISSION UPDATE — R3.14C PRODUCTION / R3.14D ACTIVE"
if marker in text:
    raise SystemExit("superbook R3.14C marker already present")
text += f"""

---

## CURRENT REPLAY DECODER ADMISSION UPDATE — R3.14C PRODUCTION / R3.14D ACTIVE

Current repository truth now supersedes earlier superbook passages that stop at the R3.13/R3.14A boundary.

```text
R3.14C production SHA = {PROD}
```

R3.14C admits only the private native network bit cursor and canonical bounded-u32 primitive. It was validated with 19 focused tests, all 47 R3.14A actor-ID vectors, full locked workspace verification, clean reconstruction, force-free publication, and published-main CI.

Active exact pass:

```text
R3.14D — first actor envelope header native reader
docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md
```

R3.14D stops after the first actor `new` bit. `name_id`, object/spawn/property/attribute payloads, second actor/frame iteration, actor state, raw state, events, and skills remain closed. R3.14E remains the separate 47-replay native-vs-Boxcars differential audit.

Historical archived parser code remains evidence/migration material; it does not override this current production boundary.
"""
write(path, text)


# 9. Next-chat handoff: replace with current concise exact prompt.
path = "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md"
write(path, f"""# MIMIR — Next Chat Handoff

Bu dosyadaki prompt yeni bir ChatGPT/Codex konuşmasına doğrudan verilebilir.

---

# Copy/paste prompt

```text
Naveax/MIMIR reposundan fresh GitHub main gerçeğine göre devam et.

Önce MIMIR_KNOWLEDGE_GRAPH.md içindeki mandatory reading order'ı uygula. MIMIR_CONTINUE_HERE.md, structured continuity state, current state, R3.14A decision, R3.14B contract, R3.14C decision, R3.14D exact spec, boundary locks, roadmap ve ledger'ı oku. Sonra Superbook + SOURCE_REGISTRY + VALIDATION_MATRIX + HISTORICAL_TO_CURRENT_MAPPING ile historical/current bilgiyi çapraz doğrula.

Current production SHA:
{PROD}

Current production milestone:
R3.14C — private native network bit cursor + canonical bounded-u32 primitive.

R3.14C facts:
- source only: crates/mimir-replay/src/lib.rs
- private LSB-first NetworkBitCursor
- private read_bit/read_bits_le
- private canonical read_bounded_u32
- atomic failure/rollback
- 19 focused tests
- 47/47 R3.14A actor-ID value match
- 47/47 R3.14A end-bit match
- clean CI 31698938025 SUCCESS
- published-main CI 31699241010 SUCCESS

Repository hygiene prerequisite already closed separately:
- c42836647673cecc47cc9c89908da1de11d8a222
- stale Cargo.lock synchronized
- verify_repo.ps1 now uses Cargo --locked
- this is NOT replay capability expansion

ACTIVE EXACT PASS:
R3.14D — first actor envelope header native reader.

Exact spec:
docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md

R3.14D may natively consume only:
1. first frame time raw u32 -> f32
2. first frame delta raw u32 -> f32
3. actor_present
4. bounded actor_id if actor_present
5. alive if actor_present
6. new if alive
7. STOP

Do not skip time/delta by setting cursor=64. Consume the first 64 bits through the R3.14C cursor and verify raw bits agree with ReplayNetworkTimingPreambleV1.

Branch contract:
- actor_present=false => actor_id/alive/is_new None, stop
- alive=false => actor_id Some, alive Some(false), is_new None, stop
- alive=true => consume new, set is_new Some(...), stop

HARD STOP:
- no name_id
- no post-name bit
- no object_id
- no spawn trajectory payload
- no property loop
- no stream_id
- no attribute payload
- no second actor
- no second frame
- no actor lifecycle mutation
- no raw state/events/skills

Use only current admitted support lane. No BuildVersion/header widening. No Boxcars production dependency. Cargo.lock/manifests must not change.

Process:
fresh main audit -> implementation branch -> focused tests -> full locked validation -> hard-stop diff audit -> clean source reconstruction onto fresh main -> exact clean CI -> force=false publication -> published-main readback/CI -> continuity + knowledge graph sync.

R3.14D implementation success does NOT replace R3.14E. After R3.14D, the next pass is R3.14E: 47-replay native-vs-pinned-Boxcars exact differential audit for time raw bits, delta raw bits, actor_present, actor_id, alive, new, stop bit.

If fresh main is newer than {PROD}, inspect the newer production code first and repair continuity from repo truth before following this prompt.
```

---

Historical work before R3.14D must not be restarted. Current code/tests and exact-SHA evidence outrank old chat memory and historical executor files.
""")

print("R3_14C_CONTINUITY_SYNC_PATCH=PASS")
