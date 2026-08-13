# MIMIR — Next Chat Handoff

Bu dosyadaki prompt yeni bir ChatGPT/Codex konuşmasına doğrudan verilebilir.

---

# Copy/paste prompt

```text
Naveax/MIMIR reposundan fresh GitHub main gerçeğine göre devam et.

Önce MIMIR_KNOWLEDGE_GRAPH.md içindeki mandatory reading order'ı uygula. MIMIR_CONTINUE_HERE.md, structured continuity state, current state, R3.14A decision, R3.14B contract, R3.14C decision, R3.14D exact spec, boundary locks, roadmap ve ledger'ı oku. Sonra Superbook + SOURCE_REGISTRY + VALIDATION_MATRIX + HISTORICAL_TO_CURRENT_MAPPING ile historical/current bilgiyi çapraz doğrula.

Current production SHA:
bad2db9d5043a7a0087a4fab1d278df5f36c7717

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

If fresh main is newer than bad2db9d5043a7a0087a4fab1d278df5f36c7717, inspect the newer production code first and repair continuity from repo truth before following this prompt.
```

---

Historical work before R3.14D must not be restarted. Current code/tests and exact-SHA evidence outrank old chat memory and historical executor files.
