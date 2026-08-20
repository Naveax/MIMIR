# MIMIR — Next Chat Handoff

Canonical production is **R3.18AG** at `2d351e8ceb601e2fbe515d2977b2103a4b2c7976` / `4123820ce6537f2d4942cd0b5f72b52e43b96c1d` with parent `037a10a41848ca2621e1b64567c3c1bd7b2f6808`. Builder `32401660279/96531043622`, validation PR #55 exact-head CI `32402596061/96534073576`, and published-main CI `32402933798/96535174390` are SUCCESS; PR #55 was closed unmerged. Clean production scope is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18ag_post_ad_payload_control.rs`, with blobs `db923ebcb419d278f4ab0144fe7ed15b298b60fa` / `3f3e1c8f3f6deb7f2558862a1032f8a102131443`.

R3.18AF remains **Outcome A / CLOSED**: evidence `30286c07727539d68f551140838fb2ef6802a26e` / `32344981062/96351720877`, same-head CI `32345376481/96352906609`, artifact `9397743505` / `sha256:d7edeab657928c94c35c852ae302fd614cab92a52b7e44f671310200af4b268f`. Its immutable 47 witnesses observed false=0 / true=47 with mismatch 0, witness reselection 0, and next stream/header/payload/second-control consumption 0/0/0/0.

The active pass is **R3.18AH**, a read-only published-API differential. Validate published R3.18AG on exactly those 47 AF witnesses through the one-bit stop. Do not open the next header, payload, second control, generic property loop/cursor or any semantic/runtime boundary.

Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AG_DECISION.md`, and `docs/continuity/MIMIR_R3_18AH_EXECUTION_SPEC.md` before continuing.
