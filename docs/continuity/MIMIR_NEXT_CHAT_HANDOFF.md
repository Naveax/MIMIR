# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BE** at `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`.

R3.18BF is **Outcome A / CLOSED** at `5a3f875a445f9a3a2176788555089562948c3676` / run `34098102185/101666129830` SUCCESS with same-head CI `34098102183/101666129957` SUCCESS. Authoritative artifact `10009534065` / `sha256:79a5d254876d19d90e03dcfeff650755d8b816d8a6869e13b8468eebd7d60bdc`; inner manifest `sha256:35747c9813f56e58c1515dc301cf6a0d3d3a86fd0b068fba609948016d0e45ce`. Published BE matched all 40 frozen rows: false=37, true=3 exact headers, BD contexts=3/3, Boolean=2 / Float=1, mismatch/reselection 0/0, payload/second-control 0/0.

Active pass: **R3.18BG — one following primitive payload evidence**. Use BF artifact as direct row authority. Only the 3 BF-true rows may enter payload decoding. Reconstruct published BE/header first, decode exactly one current primitive scalar, compare to pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`, preserve Float raw bits, stop at payload end. The 37 BF-false rows and 7 upstream AU false terminators never invoke the payload decoder. Expected family Boolean=2 width1, Float=1 width32. Historical AW/AM/AN coordinates/values are not authority. Next property-control consumption remains zero.

Before dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse existing exact runs. Rerun is never polling.
