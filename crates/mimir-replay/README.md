# mimir-replay

`mimir-replay` owns the replay-reader traits and the first minimal replay-header reader boundary.

## Default Reader

`UnsupportedReplayReader` remains the truthful unsupported default. It does not parse replay bytes,
does not call `MinimalReplayHeaderReader`, and should stay distinguishable from any explicit opt-in
parser path.

## Explicit Opt-In Header Reader

`MinimalReplayHeaderReader` is explicit opt-in only. Callers must choose it directly and must pass
already admitted bytes through `ReplayInput::Memory`.

Parser-success is admitted only for ReplayInput::Memory, the exact fixture-supported tuple, and header-only parsing ending at 8 + header_size. Parser-success is not admitted broadly.

The admitted first minimal boundary is:

- input is `ReplayInput::Memory`
- `ReplayInput::Memory.label` is non-empty and already admitted by the caller
- `ReplayInput::Memory.bytes` are already admitted by the caller
- parsing stops at `8 + header_size`
- the supported tuple is exactly the fixture-supported tuple
- the result is only a `ReplayHeader`

Callers must not derive parser facts from path, hash, filename, provenance, artifact id, fixture id,
or any label convention. Fixture identity can help an external audit establish which bytes were
supplied, but it is not parser evidence and must not widen parser admission.

## Non-Claims

A successful `MinimalReplayHeaderReader` call is not replay-source materialization. It does not
prove that a replay path, filename, hash, receipt, or artifact id was read or validated by the
parser.

A successful header parse is not body parsing, raw-state parsing, frame parsing, footer parsing, or
event parsing. CRC validation is not performed. `ReplayInput::File` is unsupported by this reader.

No export behavior, runtime behavior, CLI behavior, backend replay parser dependency, broad replay
version-family support, nested array semantic parsing, UTF-16 support, or unencountered
property-kind support is implied by this crate-level opt-in reader.

## Explicit Opt-In Usage Sketch

This sketch is only for callers that already hold admitted bytes and a non-empty admitted label.
It is not a file loader, fixture locator, runtime integration, export integration, or broad parser
claim.

```rust
use mimir_replay::{MinimalReplayHeaderReader, ReplayInput, ReplayReader};

let reader = MinimalReplayHeaderReader;
let input = ReplayInput::Memory {
    label: admitted_non_empty_label,
    bytes: already_admitted_bytes,
};

let header = reader.read_header(&input)?;
```

The caller remains responsible for proving that `admitted_non_empty_label` and
`already_admitted_bytes` were admitted before this call. The reader must not be treated as support
for `ReplayInput::File`, CRC validation, body/raw-state/frame/event parsing, export, runtime, or CLI
behavior.
