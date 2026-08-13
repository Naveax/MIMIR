# Historical-to-Current MIMIR Mapping

This document maps discovered ChatGPT-storage material into the current Rust architecture.

| Historical source | Historical capability/idea | Current/future MIMIR mapping | Status |
|---|---|---|---|
| RL Replay Coach V0.2 | header/body/footer parse | `mimir-replay` structural parsing | current Rust has newer native structural layers |
| RL Replay Coach events JSONL | fixed event windows | Replay Slice Engine + Control-Onset Rewind | migration candidate |
| V0.2 test fixture | structural regression | extra parser-format fixture lane | candidate; 2v2, not 1v1 tactical benchmark |
| V0.2 heuristic adapter | ETA/goal-angle heuristic baseline | scorer baseline | future benchmark |
| physics-derived settings JSON | frame/physics output | native raw-state differential oracle | provenance recovery required |
| Master Design Spec | anchor/rewind/counterfactual/teacher | long-term core architecture | target design |
| Master Blueprint | Skill Forge/rare skills/closed loop | skill/teacher/curriculum roadmap | target design |
| mimir_sistem_tasarimi | position library/benchmark | corpus intelligence/query layer | target design |
| gabriel_sistem_tasarimi | Scout/Player War Map | consumer/query contracts | target design |
| NX/Fast384 docs | observation/curriculum consumers | adapters only | consumer evidence |

## Rule

No historical item becomes current production capability merely by being archived here.
Promotion requires a dedicated evidence/admission/implementation/audit pass.
