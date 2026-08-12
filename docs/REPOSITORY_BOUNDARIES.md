# Repository Boundaries

Audit snapshot: 2026-08-12.

MIMIR is an independent Rust workspace.

The local Rocket League project root also contains sibling projects such as:

- RocketSim
- NX-HyperBot
- Gabriel
- RLArenaCollisionDumper

The audited MIMIR source tree does not currently contain a real path/code dependency on NX-HyperBot, Gabriel, or RLArenaCollisionDumper.

RocketSim is referenced in planning/status documentation as a future or unimplemented simulation backend, but it is not currently bundled or linked as a required dependency. `mimir-sim-bridge` remains inside the MIMIR workspace and should not be treated as proof of a live RocketSim backend.

Do not vendor sibling projects into MIMIR merely because they exist beside it on one developer machine.

If a future integration becomes real, add it deliberately through a versioned adapter/dependency boundary and document its exact provenance/version.