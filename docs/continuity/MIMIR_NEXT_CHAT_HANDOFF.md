# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AY** at `2558cc0559422a3e6695e1501f20d96d83b23e6d` / `93198ad2a4f929ac62b87beddbc9d5b5665f08d1`. R3.18AZ is now **CLOSED / Outcome A**: evidence `f46479faa2b230f7fde474f7f7696a1024420879` / run `33086674062/98568084290` SUCCESS, same-head natural CI `33086674797/98568087263` SUCCESS, artifact `9652520412` / `sha256:558c709e242d74150755565d07c7968853abad0a1de6c5f49cd8f5920e7f9fc4`, downloaded digest exact and inner manifest 13/13 PASS.

R3.18AZ proves published AY exact on the immutable 40-row AW payload lane: published AY 40/40, AW native/oracle 40/40, Int=40, width32=40, semantic range 5..300, mismatch 0, witness reselection 0, and AX following-control consumption 0. The seven upstream AU false terminators remain outside the payload lane.

The active pass is **R3.18BA bounded post-AY mixed following-control production**. Recompute one valid AY payload, consume exactly one AX-admitted `property_present` bit at AY stop, preserve both false=37 and true=3, and stop one bit later. No following stream/header/payload or second control is open.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
