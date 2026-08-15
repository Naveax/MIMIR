from pathlib import Path

FILES = [
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_R3_17N_DECISION.md",
    "docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md",
]
for name in FILES:
    p=Path(name)
    if not p.is_file(): raise SystemExit(f"missing generated file: {name}")
    lines=p.read_text(encoding="utf-8").splitlines()
    p.write_text("\n".join(line.rstrip(" \t") for line in lines)+"\n",encoding="utf-8",newline="\n")
print("R3_17N_CONTINUITY_WHITESPACE=PASS")
