# MIMIR — Mandatory Pass Protocol

**Status:** mandatory for all future MIMIR work  
**Applies to:** evidence, planning, implementation, audit, publication, continuity sync

---

# 1. Why this protocol exists

MIMIR deliberately grows through narrow evidence-backed passes. The protocol prevents three recurring failure modes:

1. **capability inflation** — a format observation becomes a fake production claim;
2. **scope drift** — a narrow parser change quietly opens unrelated boundaries;
3. **false green validation** — a workflow appears successful while a native command actually failed.

The protocol is not ceremony for its own sake. Binary replay parsing punishes one-bit mistakes by corrupting everything after them, so “probably correct” is an expensive form of optimism.

---

# 2. Pass classes

Every pass must declare exactly one primary class.

## 2.1 Evidence pass

Purpose:

- observe format behavior;
- compare against oracle/reference;
- collect corpus distributions;
- identify candidate invariants;
- never claim native production support.

Default production source policy: **no source change**.

## 2.2 Admission / policy pass

Purpose:

- decide which evidence becomes a production contract;
- define accepted and rejected forms;
- define malformed/unsupported/error boundaries;
- explicitly list what remains closed.

Default source policy: docs/artifacts only unless the pass explicitly includes contract code.

## 2.3 Implementation-planning pass

Purpose:

- map admitted contract to exact code locations/types/helpers/tests;
- define allowed-file set;
- define test matrix;
- define rollback/failure conditions.

No capability claim yet.

## 2.4 Implementation pass

Purpose:

- implement only the admitted contract;
- write focused regression/malformed tests;
- do not widen adjacent boundaries.

## 2.5 Audit/admission pass

Purpose:

- independently inspect implementation scope;
- verify tests actually exercise real behavior;
- check locked boundaries did not open;
- choose Outcome A/B/C.

## 2.6 Publication pass

Purpose:

- reconstruct clean source-only commit;
- validate exact clean SHA;
- re-check fresh main ancestry;
- publish with `force=false`;
- validate exact published main SHA.

## 2.7 Continuity sync pass

Purpose:

- update canonical state after a milestone truly closes;
- never pretend an in-flight branch is production.

---

# 3. Mandatory pass header

Every executor prompt/report begins with:

```text
PASS ID:
PASS TYPE:
BASE SHA:
EXPECTED MAIN SHA / ancestor:
ALLOWED FILES:
FORBIDDEN FILES:
INPUT CORPUS:
ORACLE/REFERENCE (if any):
OPEN BOUNDARY:
HARD STOP BOUNDARY:
EXPECTED OUTPUTS:
VALIDATION GATES:
PUBLICATION POLICY:
```

If any of these are unknown and materially affect correctness, discover them before implementation.

---

# 4. Preflight repository audit

Before every nontrivial pass:

```text
fetch origin/main
resolve main SHA
inspect latest commits
inspect working tree / branch state
compare expected base to current main
read continuity state
read active exact-pass spec
inspect target code and tests
```

If base drift exists:

### Docs-only continuity drift

May proceed after confirming production source is unchanged and updating the branch base as required.

### Production-code drift

Stop. Re-audit current code and update the pass plan. Never blindly replay an old patch onto new production code.

---

# 5. Source-of-truth rule

Order:

```text
current source/tests
> exact-SHA CI/evidence
> continuity machine state
> current-state doc
> active pass spec
> boundary locks
> roadmap
> historical artifacts
> chat memory
```

A chat summary is never enough to override current code.

---

# 6. Evidence discipline

## 6.1 Evidence is not implementation

Examples:

```text
oracle can decode field X
!= MIMIR can decode field X

structural scanner locates section Y
!= semantic Y parser exists

lookup registry resolves stream IDs
!= attribute payload decoder exists
```

## 6.2 Evidence must be reproducible

Every evidence artifact should record:

```text
MIMIR base SHA
input identity / manifest
oracle identity / SHA if used
script/tool identity
output schema version
run timestamp if relevant
aggregate counts
error count
```

## 6.3 No cherry-picked success corpus

If a pass claims “supported 47,” it must use the exact 47-replay set as defined by production admission/evidence, not a convenient subset.

If a pass claims a format-wide property, use the broadest checked-in corpus appropriate for that claim.

---

# 7. External oracle protocol

External parsers such as Boxcars are references, not hidden production backends.

Mandatory rules:

1. exact immutable oracle revision;
2. pin recorded in evidence;
3. clean oracle checkout before instrumentation;
4. instrumentation diff recorded;
5. instrumentation must not alter decode semantics;
6. oracle dependency does not enter production automatically;
7. production implementation must still be independently tested;
8. differential mismatch is investigated, not papered over.

Never use “latest” as a differential oracle pin.

---

# 8. Narrow implementation rule

An implementation pass receives an exact allowed-file list.

Example:

```text
ALLOWED:
crates/mimir-replay/src/lib.rs

FORBIDDEN:
Cargo.toml
Cargo.lock
other crates
README capability changes
normal production workflows
```

After implementation:

```text
git diff --name-only
```

must equal the expected scope.

Unexpected file drift means fail/repair, not “probably harmless.”

---

# 9. Dependency lock discipline

Parser passes that do not intentionally add dependencies must not change dependency manifests/lockfiles.

If Cargo touches `Cargo.lock` during validation despite no intended dependency change:

- determine whether baseline lock drift already exists;
- do not bundle incidental lock regeneration into parser source commit;
- restore lock to the parent state;
- validate source using the same repository policy used by canonical CI;
- handle lock maintenance separately.

---

# 10. PowerShell / native process fail-fast rule

This is mandatory because prior workflow evidence showed that PowerShell steps can remain green after native command failure.

After native commands, explicitly check exit status.

Example:

```powershell
& cargo test -p mimir-replay -- --nocapture
if ($LASTEXITCODE -ne 0) {
    throw "cargo test failed with exit code $LASTEXITCODE"
}
```

Apply to:

```text
cargo
git
python
rustc
external oracle binaries
custom compiled evidence tools
```

Do not treat GitHub Actions `success` as sufficient if command exit propagation is not proven.

---

# 11. Test design rules

Each implementation pass should include four categories where applicable:

## 11.1 Real happy path

Checked-in real replay(s), not only synthetic bytes.

## 11.2 Regression

Previously supported behavior must remain unchanged.

## 11.3 Malformed / truncation / wrong-kind

Each newly admitted structural field should have fail-closed tests for incorrect shape where practical.

## 11.4 Scope-lock tests

Examples:

- unsupported version remains unsupported;
- future field remains unopened;
- no wildcard admission;
- `NotImplemented` tag remains fail-closed;
- duplicate actor ID rule reflects evidence rather than intuition.

Synthetic tests should not replace corpus regression; corpus regression should not replace surgical malformed tests.

---

# 12. Focused validation phase

Before full workspace CI, run the smallest strong set:

```text
cargo fmt --all -- --check
cargo check -p target-crate --all-targets --all-features
cargo test -p target-crate -- --nocapture
cargo clippy -p target-crate --all-targets --all-features -- -D warnings
```

If cross-crate seams exist, include the directly affected consumer crate.

A focused pass must fail immediately on any failed native command.

---

# 13. Temporary workflow isolation

Temporary workflows/scripts used to patch or instrument on GitHub are scaffolding.

They may exist on:

```text
evidence branch
implementation branch
validation-trigger branch
```

They must not enter the clean production commit unless separately admitted as permanent tooling.

Reason:

- keeps main history about product code rather than one-off orchestration;
- prevents temporary secrets/paths/oracle assumptions becoming runtime policy;
- makes source diff auditable.

---

# 14. Source-only clean reconstruction

After focused validation:

1. capture verified source blob(s)/content;
2. fetch fresh `main`;
3. reconstruct only allowed source changes on the exact fresh main parent;
4. restore/remove temporary files;
5. audit diff.

Clean commit requirements:

```text
behind main = 0
expected ahead relation only
changed files == allowed files
no temporary workflows
no incidental Cargo.lock
no evidence script unless explicitly productionized
```

If clean reconstruction uses `git checkout <sha> -- file`, remember it stages the file. Scope checks must account for index and working tree correctly.

---

# 15. Exact-SHA validation

Full validation must prove the runner checked out the exact clean commit.

First gate:

```text
git rev-parse HEAD == EXPECTED_CLEAN_SHA
```

Then run canonical repository verifier/full test matrix.

A successful run on “same branch, probably same tree” is weaker than exact-SHA evidence and is not the preferred publication gate.

---

# 16. Full validation expectations

Canonical full validation normally includes:

```text
cargo fmt check
cargo check workspace/all targets/all features
mimir-replay tests
mimir-skill tests
workspace tests
clippy -D warnings
corpus integrity/hash verification
compatibility/admission matrix
repository verification wrapper
```

Exact commands may evolve; use current canonical repo scripts/CI as source of truth.

The final report must quote/load the important counts, not just “CI green.”

---

# 17. Fresh-main publication gate

Immediately before publication:

```text
fetch main again
compare clean commit vs fresh main
```

Require:

```text
clean commit is descendant / fast-forward candidate
no unexpected main commits requiring rebase/reconstruction
```

Publish:

```text
force = false
```

Force push is forbidden for ordinary MIMIR production passes.

---

# 18. Publication readback

After main moves:

1. resolve exact new main SHA;
2. confirm it equals the clean production SHA expected for source pass;
3. run/fetch exact-main validation;
4. read back key counts;
5. only then mark production milestone closed.

Do not announce “production closed” before publication CI/readback is complete.

---

# 19. Continuity sync protocol

After publication closes, make a docs-only continuity update.

At minimum change:

```text
MIMIR_CONTINUITY_STATE.json
MIMIR_CURRENT_STATE.md
MIMIR_PROGRESS_LEDGER.md
MIMIR_NEXT_CHAT_HANDOFF.md
active exact-pass spec pointer/content
```

Update fields:

```text
last_production_code_sha
last_completed_milestone
current_pass
new evidence counts
newly opened boundaries
still closed boundaries
next exact stop boundary
```

Do not update continuity to an in-flight branch result.

---

# 20. Outcome model

Every pass ends with explicit outcome.

## Outcome A

Evidence/implementation is sufficient; proceed to the named next pass.

## Outcome B

Bounded gap; retain progress but open only a targeted follow-up.

## Outcome C

Contradiction/regression; do not widen capability. Reopen earlier policy/evidence.

Avoid vague endings such as “mostly works.”

---

# 21. Mandatory final report format

```text
PASS:
TYPE:
BASE SHA:
RESULT:
OUTCOME:
CHANGED FILES:
TEMPORARY FILES:
TESTS / COUNTS:
CORPUS RESULT:
DIFFERENTIAL RESULT:
BOUNDARIES OPENED:
BOUNDARIES STILL CLOSED:
CLEAN COMMIT SHA:
PUBLISHED MAIN SHA:
PUBLICATION CI:
CONTINUITY SYNC:
NEXT EXACT PASS:
```

Fields not applicable should say `N/A`, not disappear.

---

# 22. Stop conditions

Stop capability widening immediately if any occurs:

- base SHA drift involving production code;
- oracle pin unknown;
- corpus identity mismatch;
- unexpected source file modification;
- native command failed;
- test runner did not check exact SHA;
- differential mismatch with no explanation;
- malformed test reveals ambiguous cursor semantics;
- current evidence cannot distinguish two format interpretations;
- new behavior would require opening a boundary not admitted by current pass.

Stopping at a truthful boundary is progress. Hiding ambiguity is technical debt with better branding.

---

# 23. Review rule for large decoder work

Never implement the entire network decoder in one pass.

Recommended granularity:

```text
bit primitive
→ first envelope
→ spawn branch
→ property envelope
→ one attribute family
→ additional attribute families
→ one full actor update
→ actor lifecycle table
→ one full frame
→ frame iteration
```

Each stage receives differential evidence before/with admission.

---

# 24. Long-term semantic rule

Binary decoding and semantic interpretation remain separate.

Example layers:

```text
wire bits
→ typed network attribute value
→ actor property state
→ semantic Rocket League entity state
→ canonical raw state
→ event
→ slice
→ skill
```

Do not jump from a decoded property directly to a skill label without the intermediate contracts.

---

# 25. Definition of protocol compliance

A pass is protocol-compliant if:

- its scope and stop boundary were stated before implementation;
- repository/oracle/corpus identity was pinned;
- evidence and implementation claims were separated;
- native commands were fail-fast;
- source diff matched allowed files;
- clean exact-SHA validation passed;
- publication was force-free;
- exact published main readback passed;
- continuity was synced afterward.

Anything less must be reported as a deviation, not quietly normalized.
