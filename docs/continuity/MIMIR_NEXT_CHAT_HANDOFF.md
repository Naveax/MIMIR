# MIMIR — Next Chat Handoff

Canonical production is **R3.18AQ** at `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`. R3.18AS is closed Outcome A as read-only following-header evidence and R3.18AT is closed Outcome A as an exact-context contract.

R3.18AT contract authority: `docs/continuity/MIMIR_R3_18AT_ADMITTED_HEADER_CONTEXTS.json` / `sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5`. Membership is exact tuple equality over `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`. Exactly 16 contexts are admitted with multiplicities summing to 40. All observed headers are `Int`. The exact seven AQ-false rows remain terminators and are outside header membership.

Source evidence remains R3.18AS: evidence `475650fea59332f74b9f69da50e3e4471622ab7e`; run/job `32959321642/98147938829` SUCCESS; same-head CI `32959321531/98147938016` SUCCESS; artifact `9603335255` / `sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45`; frozen 47 rows / false=7 / true=40 / exact true headers 40/40 / mismatch 0 / payload-control consumption 0/0. AS canonical publication helper `32967201830/98172273710` succeeded.

The active pass is **R3.18AU bounded production**. Validate/recompute one published AQ prior. False must remain a no-header terminator with zero post-AQ reads. True may invoke the existing stateless following-header primitive once, must require exact R3.18AT membership, and must stop at `payload_start`.

Do not decode the following payload, read another control bit, admit any context outside the exact AT set, or create a generic/repeated property loop. Before any workflow dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
