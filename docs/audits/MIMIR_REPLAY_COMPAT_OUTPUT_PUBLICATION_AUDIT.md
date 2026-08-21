# Replay compatibility output publication audit

Status: **NON-CANONICAL AUXILIARY AUDIT / NO REPLAY CAPABILITY CLAIM**

Base commit: `02233c8125e658513dcb068370c48b1e8f15a01c`
Base tree: `fc9293d821dd3e6e269763c3c0ab091428c29490`

## Finding

`crates/mimir-cli/src/replay_compat.rs::run(...)` computes the complete compatibility rows and summary in memory, then publishes two files in sequence:

```rust
write_jsonl(&output, &rows)?;
write_pretty_json(&summary_output, &summary)?;
```

Both helpers create the parent directory and call `fs::write(...)` directly.

If the matrix write succeeds but the summary write fails, the call returns an error while a newly written matrix remains visible. The inverse failure shape is not possible with the current order, but callers can still observe a partial publication that does not have its matching summary.

This is not a replay-parser correctness defect. It is an artifact publication atomicity/integrity gap at the CLI reporting boundary.

## Failure examples worth testing

A future focused candidate should exercise failure injection or filesystem layouts proving that:

- matrix staging succeeds but summary publication failure leaves no newly published final matrix;
- existing final outputs are not silently truncated before a complete replacement is ready;
- a successful run publishes a matching matrix + summary pair;
- parent directory creation remains supported;
- JSONL newline behavior and pretty-summary shape remain byte-stable;
- no change is made to parser support gates, compatibility classification, tuple observation, or corpus semantics.

## Recommended narrow direction

Do not add transaction semantics to the replay parser. Keep this entirely in the compatibility-report output layer.

A narrow implementation can:

1. serialize both outputs completely before touching final paths;
2. write both to uniquely named staging files in their target directories;
3. only after both staged writes succeed, finalize the pair;
4. clean up staging files on failure;
5. explicitly document that two independent filesystem renames are still not a crash-proof multi-file transaction unless a directory-level publication strategy is adopted.

If stronger all-or-nothing visibility is required, publish into a newly created staging directory and rename the directory as one unit, rather than pretending two file renames are a real transaction.

## Non-claims

This audit:

- does not modify production Rust;
- does not modify `mimir-replay`;
- does not alter compatibility counts or supported tuples;
- does not alter fixtures/corpus, Cargo, workflows, continuity, or Skill Forge behavior;
- does not authorize a canonical R3.18 pass;
- does not claim that the current output is corrupt when both writes succeed.

Before any fix is admitted, reconstruct it from fresh `main`, re-check branch/PR ownership, and validate exactly one candidate SHA without duplicate Actions runs.
