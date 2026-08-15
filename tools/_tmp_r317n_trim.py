from pathlib import Path

path = Path("docs/continuity/MIMIR_R3_17N_CONTRACT.md")
if not path.is_file():
    raise SystemExit("missing generated R3.17N contract")
lines = path.read_text(encoding="utf-8").splitlines()
path.write_text("\n".join(line.rstrip(" \t") for line in lines) + "\n", encoding="utf-8", newline="\n")
print("R3_17N_CONTRACT_WHITESPACE=PASS")
