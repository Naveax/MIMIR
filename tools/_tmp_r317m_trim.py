from pathlib import Path

FILES = [
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_R3_17M_DECISION.md",
    "docs/continuity/MIMIR_R3_17N_EXECUTION_SPEC.md",
]

for name in FILES:
    path = Path(name)
    if not path.is_file():
        raise SystemExit(f"missing generated continuity file: {name}")
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip(" \t") for line in lines) + "\n", encoding="utf-8", newline="\n")

print("R3.17M generated continuity whitespace normalized")
