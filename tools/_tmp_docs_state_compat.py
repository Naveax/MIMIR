from pathlib import Path
import json
p=Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
s=json.loads(p.read_text(encoding="utf-8"))
s.setdefault("r3_15a", {})["pre_admission_state"]={"current_pass":"R3.15A"}
p.write_text(json.dumps(s, indent=2)+"\n", encoding="utf-8", newline="\n")
