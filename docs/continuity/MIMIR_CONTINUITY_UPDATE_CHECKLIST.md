# MIMIR — Continuity Update Checklist

Use this after a production milestone is completely published and validated.

The purpose is to prevent continuity docs from becoming another archaeological layer in the repository.

---

# 1. Preconditions

Do NOT update canonical continuity as “completed” until:

- [ ] clean production source commit exists;
- [ ] exact clean SHA full validation passed;
- [ ] fresh-main ancestry audit passed;
- [ ] publication used `force=false`;
- [ ] main points at expected production commit (or known docs-only descendant);
- [ ] exact published-main validation/readback passed;
- [ ] important test/corpus/differential counts were read from logs/artifacts, not guessed.

If publication CI is still running, continuity state stays on the previous completed milestone.

---

# 2. Update machine state

Edit `MIMIR_CONTINUITY_STATE.json`:

- [ ] `updated_date`
- [ ] `last_production_code_sha`
- [ ] `last_production_milestone`
- [ ] `last_production_milestone_name`
- [ ] `last_completed_read_only_audit` if applicable
- [ ] `current_pass`
- [ ] `current_pass_kind`
- [ ] `current_pass_goal`
- [ ] `current_pass_stop_boundary`
- [ ] supported replay count if changed
- [ ] evidence counters if changed
- [ ] newly opened boundaries
- [ ] still-closed boundaries
- [ ] next files / active spec path

Validate JSON syntax before commit.

---

# 3. Update human current state

Edit `MIMIR_CURRENT_STATE.md`:

- [ ] exact production SHA
- [ ] completed pass
- [ ] what production can now do
- [ ] what evidence proved
- [ ] what production still cannot do
- [ ] important negative/anti-regression facts
- [ ] next exact pass
- [ ] hard stop boundary
- [ ] any changed corpus/support counts

Never keep a completed pass described as “next.”

---

# 4. Append progress ledger

Append, do not rewrite:

- [ ] date
- [ ] pass ID/title
- [ ] base SHA
- [ ] production SHA
- [ ] outcome
- [ ] changed files
- [ ] evidence counts
- [ ] test/CI counts
- [ ] boundaries opened
- [ ] boundaries still closed
- [ ] negative facts
- [ ] next pass

If an earlier ledger fact was wrong, append a correction entry.

---

# 5. Active pass spec rotation

If current exact pass changed:

- [ ] create the new exact-pass spec or update canonical pointer;
- [ ] update `MIMIR_CONTINUE_HERE.md` reading order/pointer if filename changes;
- [ ] update `MIMIR_NEXT_CHAT_HANDOFF.md`;
- [ ] update state JSON active spec path if represented;
- [ ] preserve completed exact-pass spec as historical continuity evidence unless cleanup policy says otherwise.

Do not overwrite old exact-pass results to make them look like the new pass.

---

# 6. Boundary locks sync

If a capability boundary opened:

- [ ] move only that exact boundary from CLOSED/EVIDENCE-ONLY to OPEN/PRODUCTION;
- [ ] state the admission pass/commit;
- [ ] keep deeper boundaries closed;
- [ ] add new anti-regression locks discovered by evidence.

Example:

```text
opening native actor_id decode
DOES NOT automatically open
spawn payload, properties, attributes, frame iteration
```

---

# 7. Roadmap sync

Roadmap edits are required only when sequencing/architecture changed materially.

- [ ] mark no fake “percentage complete” unless evidence supports it;
- [ ] do not delete future phases merely because implementation changed;
- [ ] if a pass splits, record the split in near-term sequence;
- [ ] if evidence invalidates an assumption, update the relevant future dependency.

---

# 8. Next-chat handoff sync

The handoff must contain:

- [ ] repository name
- [ ] last production SHA
- [ ] current pass
- [ ] exact reading order
- [ ] current important evidence counts
- [ ] hard stop boundaries
- [ ] known process traps
- [ ] first-response audit questions

Copy/paste prompt should be sufficient without needing old chat memory.

---

# 9. Diff audit for continuity commit

Before publishing docs-only sync:

```text
expected files only under continuity docs / pointer README
no Rust source
no Cargo manifest/lock
no test corpus binaries
no temporary workflow
no oracle checkout
```

If continuity sync accidentally contains product code, split it.

---

# 10. README freshness

Check whether top-level README capability summary became materially false.

If yes:

- [ ] update only concise current capability pointer/summary;
- [ ] prefer linking to `MIMIR_CONTINUE_HERE.md` for rapidly changing detail;
- [ ] avoid duplicating the entire continuity state in README.

---

# 11. Self-reference rule

Do not try to embed the continuity docs commit's own SHA inside files in the same commit. That creates self-referential churn.

Record:

```text
last production code SHA
```

and derive current continuity head from GitHub `main`.

A docs-only commit newer than the recorded production SHA is valid.

---

# 12. Final continuity validation

Before marking sync complete:

- [ ] `MIMIR_CONTINUE_HERE.md` points to files that exist;
- [ ] JSON parses;
- [ ] current-state pass == JSON current pass;
- [ ] next-chat pass == JSON current pass;
- [ ] boundary locks match current state;
- [ ] progress ledger last entry matches completed milestone;
- [ ] no stale old pass is described as current in continuity folder;
- [ ] fresh `main` file reads confirm committed content.

---

# 13. Final report

```text
CONTINUITY SYNC
Production SHA documented:
Current pass:
Files updated:
JSON validation:
Docs-only diff:
Stale-pointer scan:
Result: PASS/FAIL
```

If FAIL, repair continuity before starting a new production capability pass.
