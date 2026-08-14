# MIMIR R3.17F — Evidence-Supported K2 Contract Admission Spec

**Pass type:** contract-only
**Production implementation:** forbidden
**Input authority:** R3.17E Outcome A

## Goal

Freeze deterministic atomic decoding contracts only for K2 semantic variants actually observed by R3.17E.

## In scope

- ActiveActor exact 33-bit contract.
- String signed i32 length with observed Empty, Windows1252 and UTF16 branches, exact end-bit and truncation semantics.
- QWordString observed legacy 64-bit QWord branch and observed RL223 Windows1252 text branch.
- UniqueId observed Steam, PlayStation, PsyNet and Epic variants with evidence-supported version/width behavior.
- PartyLeader only observed Some(Epic, Windows1252 declared=33).
- Atomic malformed/truncation rules and privacy-safe test vectors derived from immutable R3.17E evidence identities.

## Not admitted

PartyLeader None/non-Epic variants, unobserved UniqueId systems/combinations, unobserved QWordString branches, any shape inferred only from Boxcars/type names, production K2 code, second property/loop continuation, actor/frame lifecycle widening, K3/K4, raw-state/event/skill/runtime/export, Cargo/corpus/support-lane widening.

## Admission gate

Outcome A requires a complete contract table for every admitted observed shape, deterministic success/end-bit semantics, explicit malformed/truncation behavior, privacy-safe vectors and zero contradiction with R3.17E. Outcome B requests targeted evidence. Outcome C stops the wave.

## Next pass on Outcome A

`R3.17G — direct native K2 decoder implementation for contract-admitted variants only`.
