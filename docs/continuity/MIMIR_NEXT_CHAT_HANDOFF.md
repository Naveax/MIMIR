# MIMIR — Next Chat Handoff

Canonical production is now **R3.18BI** at `def8e959239106e25d95091fcfcf468fec59e228` / `61ca1c3cdf504f4c1eaef3001cbe81984414c537`.

R3.18BI production is Outcome A / CLOSED. It publishes exactly the three immutable R3.18BG payload rows: Boolean=2 / Float=1, widths 1/1/32, exact semantic/start/end/stop identity, and zero R3.18BH control-bit consumption. Production builder `34158571800/101855439564` SUCCESS, validation PR #213 closed unmerged, exact-head PR CI `34159120199/101857049780` SUCCESS, published-main CI `34159530318/101858247592` SUCCESS.

R3.18BH next-control evidence remains read-only Outcome A: exact 3/3, false=1 / true=2, artifact `10023482583`. Do not infer production permission from that observation.

Active pass: **R3.18BJ — Published R3.18BI One-Following-Payload Differential**. Compare published BI against immutable BG/BH authority. Require exact payload success 3/3, 37 BE-false rows rejected before payload decoding, 7 upstream AU-false rows outside success, and zero BH/later consumption. Production mutation and witness reselection are forbidden.

Before dispatch or rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. CI waiting is not a reason to duplicate the same SHA/workflow/input.
