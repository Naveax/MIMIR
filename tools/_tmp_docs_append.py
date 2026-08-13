from pathlib import Path
for source_name, target_name in [
    ("tools/_tmp_append_continue.txt", "MIMIR_CONTINUE_HERE.md"),
    ("tools/_tmp_append_graph.txt", "MIMIR_KNOWLEDGE_GRAPH.md"),
    ("tools/_tmp_append_current.txt", "docs/continuity/MIMIR_CURRENT_STATE.md"),
]:
    source = Path(source_name).read_text(encoding="utf-8")
    target = Path(target_name)
    current = target.read_text(encoding="utf-8")
    heading = next(line for line in source.splitlines() if line.startswith("## "))
    if heading not in current:
        target.write_text(current.rstrip() + "\n" + source.strip("\n") + "\n", encoding="utf-8", newline="\n")
print("APPEND_UPDATE_PASS")
