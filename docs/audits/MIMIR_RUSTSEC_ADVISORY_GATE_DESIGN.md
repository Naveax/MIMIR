# MIMIR Rust Dependency Advisory Gate Design

Status: noncanonical security/reproducibility design. This document defines a future implementation contract; it does not itself add or execute a vulnerability scanner.

Fresh design base: `fec9dca3cb8366108245788fc9a2b24a0c99fe94` / tree `3bf5f68ec7df5565f78f89fd4bc2254f2a64e010`.

## Purpose

MIMIR commits `Cargo.lock` and uses Dependabot, but update automation is not equivalent to an exact resolved-lock advisory gate. The future gate should audit the committed `Cargo.lock` against RustSec without adding an unpinned third-party GitHub Action or installing an unspecified latest scanner on every normal CI run.

## Selected v1 policy

1. **Authoritative dependency input:** repository-root `Cargo.lock`.
2. **Scanner:** `cargo-audit` version `0.22.2`, explicitly pinned by version in the implementation. Do not use an unconstrained `cargo install cargo-audit` as the permanent gate.
3. **Rust compatibility:** the selected scanner supports a Rust floor below MIMIR's declared Rust 1.85 floor, so scanner/toolchain compatibility is not a reason to widen MIMIR's MSRV.
4. **Execution lane:** separate scheduled/manual security workflow, not an extra install/network step in every ordinary PR CI run.
5. **Default cadence:** weekly scheduled audit plus `workflow_dispatch` for explicit verification. A future workflow may also use a narrow `Cargo.lock` pull-request trigger only if that does not duplicate another equivalent active audit.
6. **Permissions:** read-only repository contents. No write permission is needed merely to audit.
7. **Failure policy:** a confirmed RustSec vulnerability match in the resolved lockfile fails the advisory job. Informational/yanked/unmaintained findings must not silently become vulnerability-equivalent blockers unless separately admitted.
8. **Database freshness:** the run must record the RustSec database revision or equivalent source receipt used for the result. A security audit with unknown advisory-data freshness is not durable evidence.
9. **No automatic fix:** the gate runs audit only. It must not invoke `cargo audit fix`, mutate manifests/lockfiles, merge Dependabot PRs, or rewrite dependencies.
10. **No polling reruns:** failed or queued advisory runs follow the repository-wide single-equivalent-run rule.

## Accepted-advisory exception contract

An advisory may be temporarily ignored only through an explicit repository-tracked exception containing:

- exact RustSec advisory ID;
- affected crate and resolved version;
- technical reason the exception is temporarily accepted;
- owner;
- creation date;
- expiry/review date;
- remediation path or blocking dependency/upstream reference.

Exceptions must be advisory-ID-specific. Wildcard ignores and permanent undocumented suppressions are not admitted.

An expired exception must fail closed until reviewed or removed.

## Supply-chain boundary

The permanent implementation must avoid an unpinned external Action. Preferred implementation shape:

- GitHub-hosted runner;
- repository-selected Rust toolchain;
- explicit `cargo-audit` version `0.22.2`;
- scanner installation or cached binary provenance documented in the workflow;
- explicit audit of repository-root `Cargo.lock`;
- output records scanner version plus advisory database revision/receipt.

If a prebuilt binary or installation cache is later used, its provenance/hash policy must be defined rather than silently trusting mutable cache contents.

## Network and determinism

RustSec data changes over time by design, so advisory results are time-sensitive rather than bit-for-bit timeless. Deterministic evidence therefore means recording enough authority to reproduce the decision context:

- repository commit SHA;
- exact `Cargo.lock` hash;
- exact scanner version;
- RustSec advisory database revision/receipt;
- audit exit status and finding IDs.

The gate must not claim that a past green result proves the lockfile is vulnerability-free forever.

## Relationship to Dependabot

Dependabot and the RustSec gate are complementary:

- Dependabot proposes dependency/security updates.
- RustSec checks the exact dependency set resolved in `Cargo.lock`.

One does not replace the other.

## Initial rollout decision

The first implementation should land as a **separate scheduled/manual security workflow** and be validated independently from canonical R3.18. Once stable, whether `Cargo.lock`-changing PRs must also block on it can be decided from actual run reliability and latency rather than assumed in advance.

## Non-goals

This design does not:

- upgrade any dependency;
- alter `Cargo.lock`;
- change canonical replay/parser/continuity behavior;
- add `cargo-deny`, SBOM generation, license policy, binary reachability analysis, or automatic remediation;
- claim that absence of a RustSec advisory proves absence of all vulnerabilities.

## Implementation acceptance checklist

A future implementation candidate is acceptable only if it proves:

1. scanner version is exact and visible in logs;
2. root `Cargo.lock` is the audited input;
3. permissions are read-only;
4. equivalent runs are not duplicated;
5. a synthetic/known advisory-positive fixture or bounded test demonstrates the failure path without mutating production dependencies;
6. a normal clean lockfile run succeeds;
7. advisory database revision/freshness receipt is captured;
8. explicit temporary exceptions are validated for advisory ID and expiry;
9. no manifest/lockfile write occurs;
10. canonical R3.18 and ordinary repository verification semantics remain unchanged.
