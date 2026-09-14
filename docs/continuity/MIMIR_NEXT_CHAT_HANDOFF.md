# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BS** at `5ab14575d0a698d752db35db76f3dbb300cdec8d` / `1c0b4c0a50385a34ba730a52a98a89423ff56869`.

R3.18BT is **Outcome A / CLOSED READ-ONLY** at `b687f700a7bf00f28671ca3adbb6613b582e7848` / `f573860e733689fa03767702f6f1750e222664c3`. Runner `34816904695/103889382147` SUCCESS and same-head CI `34816904663/103889381782` SUCCESS. Immutable artifact `10336951993` / size `5213` / `sha256:fef0df77821475ac3ee5acb417b500aa40708a573d286d30c5c42bcf23ef473d`. Published BS matches frozen BQ authority 2/2; false terminator excluded 1/1; mismatch/reselection 0; repeatability 2/2; post-stop poison 2/2; BR control consumed 0; production mutation 0.

Active pass: **R3.18BU — bounded post-BS next property-control production**. Use exactly the two admitted rows and immutable BR values: Boolean=false, ActiveActor=true. Recompute exact BS, require supplied equality and `control_start_bit == bs.stop_bit`, read exactly one checked LSB-first bit, stop at +1. Nothing after that bit is in scope.
