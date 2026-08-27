# MIMIR — Next Chat Handoff

Canonical production is **R3.18AY** at `2558cc0559422a3e6695e1501f20d96d83b23e6d` / `93198ad2a4f929ac62b87beddbc9d5b5665f08d1`, parent `dae58bc2d27aef2daac02b626ae37dbd309706bc`. The production commit is exact two-file scope: `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18ay_post_au_payload.rs`.

R3.18AY closure receipts: builder `33074574884/98525314306` SUCCESS; builder-head CI `33074574882/98525439235` SUCCESS; validation-only PR #206 closed unmerged after exact candidate CI `33075136792/98527244393` SUCCESS; published-main CI `33075583682/98528794945` SUCCESS. Fresh-main ancestry, force=false publication and exact SHA/tree readback passed.

The admitted behavior is deliberately narrow: exactly the 40 AW true payload rows decode one Int/32 payload and stop at payload end; all seven AU false terminators are rejected before payload decoding. R3.18AX's later one-bit distribution false=37 / true=3 remains evidence-only and production consumes zero of those control bits.

The active pass is **R3.18AZ published-R3.18AY one-following-payload differential**. Reuse exactly the immutable forty-row R3.18AW authority, compare published AY against AW plus direct-native/oracle identity, require exact tag/start/end/width/value and deterministic repeatability, and stop at payload end. Production mutation and AX control consumption are forbidden.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
