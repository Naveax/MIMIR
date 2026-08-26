# MIMIR — Next Chat Handoff

Canonical production is **R3.18AQ** at `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`. R3.18AS is closed Outcome A as read-only one-following-header evidence.

R3.18AS authority: evidence `475650fea59332f74b9f69da50e3e4471622ab7e` / tree `1303071ad3031f4095e29d775afd243286a67b64`; run/job `32959321642/98147938829` SUCCESS; same-head natural CI `32959321531/98147938016` SUCCESS with exact run count 1 and rerun 0; artifact `9603335255` / `13250` bytes / `sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45` with independently downloaded ZIP digest exact and inner manifest 13/13 PASS.

Scientific result: frozen rows 47/47; **7/7 false terminators**; **40/40 true following headers exact** through `payload_start`; native/oracle mismatch 0; unclassified 0; 16 unique complete contexts; all 40 headers `Int`; witness reselection 0; following-payload/second-control consumption 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; negatives/privacy PASS.

The active pass is **R3.18AT contract-only**. Freeze exact membership across `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)` for exactly the 16 AS contexts with multiplicities summing to 40. Keep the 7 false rows outside header membership. Reject tag-only/component-only/Cartesian/versionless/RL223-dropped or flipped/older-contract-inherited membership.

Do not mutate production, decode the following payload, read another control bit, or create a generic/repeated property loop. A later production composition requires separate admission after AT Outcome A.

Before any workflow dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run if present. Rerun is never polling.
