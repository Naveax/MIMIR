# MIMIR export execution-ledger prefix audit

Status: **NON-CANONICAL AUXILIARY AUDIT / NO PRODUCTION CLAIM**

Base commit: `02233c8125e658513dcb068370c48b1e8f15a01c`
Base tree: `fc9293d821dd3e6e269763c3c0ab091428c29490`
Owner lane: auxiliary only. This document does not alter the R3.18 canonical replay chain.

## Finding

`crates/mimir-export/src/lib.rs` correctly routes general export-index paths through `validate_relative_path_text(...)`. That helper rejects blank paths, absolute paths, parent traversal, current-directory components, root components, and platform prefixes by accepting only `Component::Normal` path components.

The execution-ledger index boundary adds a second intended restriction: every `relative_result_path` must stay under the `ledger` directory.

The current check in `validate_execution_ledger_index_entry(...)` is string-prefix based:

```rust
if !entry
    .relative_result_path
    .starts_with(EXECUTION_LEDGER_DIR_NAME)
{
    // reject
}
```

with:

```rust
pub const EXECUTION_LEDGER_DIR_NAME: &str = "ledger";
```

This does not prove that the first path component is exactly `ledger`.

## Minimal counterexample

A normal relative path such as:

```text
ledger-evil/results/result-0000.json
```

satisfies all of these current conditions:

- it is relative;
- every component is normal;
- it ends in `.json`;
- its raw string starts with `ledger`.

It is therefore capable of passing the intended "stay under ledger" prefix gate even though its first path component is `ledger-evil`, not `ledger`.

This is not a `..` escape from the export bundle root. The existing component validation still prevents that. The defect is narrower: a tampered execution-ledger index can point at a sibling path inside the bundle whose textual name merely shares the `ledger` prefix.

## Intended invariant

For every admitted execution-ledger result path:

```text
first path component == "ledger"
```

A string prefix is insufficient evidence for that invariant.

## Recommended narrow correction

Keep `validate_relative_path_text(...)` as the authority for normalization, retain its returned `PathBuf`, and use component-aware path prefix matching:

```rust
let relative_path = validate_relative_path_text(&entry.relative_result_path)?;

if !relative_path.starts_with(Path::new(EXECUTION_LEDGER_DIR_NAME)) {
    return Err(MimirError::message(format!(
        "execution ledger result path must stay under {}: {}",
        EXECUTION_LEDGER_DIR_NAME, entry.relative_result_path
    )));
}
```

`Path::starts_with` compares complete path components, unlike `str::starts_with`.

Do not widen this correction into a general path rewrite. General export-index path normalization is already fail-closed and should remain unchanged.

## Focused negative controls required before admission

A future production candidate should prove at least:

- `ledger/results/result-0000.json` remains accepted by the ledger path validator;
- `ledger-evil/results/result-0000.json` is rejected;
- `ledger2/result.json` is rejected;
- `ledger_backup/result.json` is rejected;
- absolute paths remain rejected;
- `ledger/../outside.json` remains rejected;
- non-JSON result paths remain rejected;
- existing valid execution-ledger persistence/load tests remain unchanged;
- general export bundle traversal protections remain unchanged.

## Scope / non-claims

This audit:

- does not modify `mimir-export` production Rust;
- does not modify workflows, Cargo, fixtures, corpus, continuity, or replay parsing;
- does not claim arbitrary filesystem escape;
- does not claim R3.18 capability or admission;
- does not authorize merging while canonical parallel slots own the main chain.

Before any future fix is admitted, reconstruct the candidate from fresh `main`, repeat branch/PR ownership checks, and use exact-head CI without duplicate Actions runs.
