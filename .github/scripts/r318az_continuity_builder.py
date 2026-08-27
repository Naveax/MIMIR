from pathlib import Path
import subprocess
import textwrap

MAIN_SHA = "d12b7662a61571ecb43109ebbc753b790d37b6ad"
BRANCH = "continuity/r318az-admit-open-r318ba"
WORKFLOW = ".github/workflows/r318az-continuity-builder.yml"
SCRIPT = ".github/scripts/r318az_continuity_builder.py"


def run(*args: str, capture: bool = False) -> str:
    p = subprocess.run(args, check=True, text=True, capture_output=capture)
    return p.stdout.strip() if capture else ""


run("git", "fetch", "origin", "main")
assert run("git", "rev-parse", "origin/main", capture=True) == MAIN_SHA
assert run("git", "rev-parse", "HEAD^", capture=True) == "53c9624b91219a412da7ab96a7581ab1adac84ca"

old = run("git", "show", f"HEAD^:{WORKFLOW}", capture=True)
start_marker = "          python3 <<'PY'\n"
end_marker = "\n          PY\n"
start = old.index(start_marker) + len(start_marker)
end = old.index(end_marker, start)
code = textwrap.dedent(old[start:end])
exec(compile(code, "r318az_embedded_builder.py", "exec"), {})

run("git", "rm", WORKFLOW, SCRIPT)
run("git", "add", "MIMIR_CONTINUE_HERE.md", "MIMIR_KNOWLEDGE_GRAPH.md", "docs/continuity")
run("git", "diff", "--cached", "--check")
run("git", "config", "user.name", "Naveax")
run("git", "config", "user.email", "79841922+Naveax@users.noreply.github.com")
run("git", "commit", "-m", "Admit R3.18AZ and open R3.18BA")

changed = run("git", "diff", "--name-only", MAIN_SHA, "HEAD", capture=True).splitlines()
expected = sorted([
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_BOUNDARY_LOCKS.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",
    "docs/continuity/MIMIR_PROGRESS_LEDGER.md",
    "docs/continuity/MIMIR_R3_18AZ_DECISION.md",
    "docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md",
])
assert sorted(changed) == expected, (sorted(changed), expected)
run("git", "push", "origin", f"HEAD:{BRANCH}")
