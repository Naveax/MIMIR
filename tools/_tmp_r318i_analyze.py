import subprocess

V1 = "9c2bc511fd20a6ef194fa3ecdce3ebb1ebf5bd3a"
source = subprocess.check_output(
    ["git", "show", f"{V1}:tools/_tmp_r318i_analyze.py"],
    text=True,
)
old = '''        if cls == "terminator":
            if label in payloads:
                raise SystemExit(f"terminator unexpectedly has payload row: {label}")
            output.append'''
new = '''        if cls == "terminator":
            output.append'''
count = source.count(old)
if count != 1:
    raise SystemExit(f"R3.18I v3 analyzer join-key patch count={count}")
source = source.replace(old, new, 1)
if "terminator unexpectedly has payload row" in source:
    raise SystemExit("R3.18I v3 stale terminator/label collision guard remains")
print("R3_18I_V3_ANALYZER_JOIN_KEY_PATCH=PASS replacements=1")
namespace = {
    "__name__": "__main__",
    "__file__": f"{V1}:tools/_tmp_r318i_analyze.py[v3-patched]",
}
exec(compile(source, namespace["__file__"], "exec"), namespace)
