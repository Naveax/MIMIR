from pathlib import Path

OLD="5472413a9c9cafcf309293daa490acc5188c88d6"
NEW="086ec251aea4eea9881cfc224bfac2d09596269f"
FILES=[
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_R3_17N_DECISION.md",
    "docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md",
]
changed=0
for name in FILES:
    p=Path(name)
    text=p.read_text(encoding="utf-8")
    n=text.count(OLD)
    if n:
        text=text.replace(OLD,NEW)
        p.write_text(text,encoding="utf-8",newline="\n")
        changed+=n
if changed<3:
    raise SystemExit(f"authority replacement unexpectedly low: {changed}")
print(f"R3_17N_AUTHORITY_FIX=PASS replacements={changed}")
