# MIMIR R3.18AN — Bounded Post-AK One Following-Payload Production Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production:** `3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38` / `3efcc244bca55623b12bb21eb277753fc61144d4`
**Parent:** `6f92e817a88056ba303229541ae04a5d5e03239b`

## Decision

R3.18AN is admitted as the minimum production composition after R3.18AK. It revalidates/recomputes the exact R3.18AK/R3.18AJ header authority, starts exactly at the validated `payload_start`, reuses the existing stateless primitive scalar decoder for exactly one R3.18AM-admitted `Int` payload, requires width 32, and stops exactly at payload end. No next property-control bit is consumed.

## Exact authority

```text
production SHA/tree                  3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38 / 3efcc244bca55623b12bb21eb277753fc61144d4
parent                               6f92e817a88056ba303229541ae04a5d5e03239b
lib blob                             9d6b5ae2898cee745a17de9d1d7ef4b8fbd0e822
focused test blob                    8aa48b2b74d0956d1d2e965d056e1cf14a81f703
R3.18AJ contract                     sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AM evidence head                842b94ed4c4e57323433585fea48116ecf18989b
R3.18AM artifact                     9443581172
corrective builder V6                32517430779/96882095196 SUCCESS
builder receipt artifact             9459403588 / sha256:0c2e93e7e1eab13c2327d4fa9cabd743cc4e123965189360b21efdf1877a210a
validation-only PR                   #192 closed unmerged
exact-head validation CI             32517915620/96883593252 SUCCESS
published-main CI                    32518304295/96884776442 SUCCESS
published-run discovery              32519544607/96888554951 SUCCESS
published receipt artifact           9460031187 / sha256:49a73a6d7bb2ac5bd9f69d32746037ee1cf67baa5d9649c53c5c8a07820d8194
published CI / Knowledge Archive     1 / 0
duplicate guard                      PASS
```

## Frozen behavior

- exact R3.18AK/AJ header authority remains mandatory;
- payload tag is `Int` only;
- payload width is exactly 32 bits;
- frozen AM lane is 47/47 with semantic range 1..415;
- final `stop_bit` equals the payload end;
- next property-control bits consumed: 0;
- no generic property cursor or repeated property loop is exposed.

## Validation

Corrective V6 passed the focused AN suite, AK/W/AA/AG source-scope regressions, full workspace `check`, `clippy -D warnings`, tests, and repository verification. The exact clean candidate then passed normal PR CI. PR #192 was validation-only and closed unmerged. Fresh main was force-free fast-forwarded to the exact candidate; natural published-main CI succeeded and the independent discovery helper proved exactly one matching CI run and no Knowledge Archive run for the source-only publish.

Historical V4 and V5 helper failures are not semantic contradictions: V4 failed only a Clippy identity-op after focused/source-scope PASS; V5 passed full repository validation and failed only unauthenticated git transport. Neither immutable SHA was rerun. V6 is authority.

## Clean scope

Exactly two files changed from parent to production: `crates/mimir-replay/src/lib.rs` (+131) and `crates/mimir-replay/tests/r3_18an_post_ak_payload.rs` (+767). Cargo, fixtures, corpus, docs, workflows and support files were unchanged in the production commit.

## Hard stop

Another property-control bit, alternate payload tags/layouts, repeated/generalized property loops/cursors, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior are not admitted.

## Next gate

R3.18AO is read-only published-production differential validation. It must reuse exactly the immutable R3.18AM witnesses and prove published R3.18AN equals the frozen AM/direct-native/oracle identity through one payload end with mismatch zero, witness reselection zero, production mutation zero and next-control consumption zero.
