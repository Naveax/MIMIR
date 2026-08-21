from pathlib import Path

lib_path = Path("crates/mimir-replay/src/lib.rs")
test_path = Path("crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs")
source = lib_path.read_text(encoding="utf-8")
start_marker = "// R3.18AK BEGIN bounded post-AG following-header composition"
end_marker = "// R3.18AK END bounded post-AG following-header composition"
target = "#[cfg(test)]\nmod tests {"
if source.count(start_marker) != 1 or source.count(end_marker) != 1:
    raise SystemExit("expected exactly one generated AK block")
start = source.index(start_marker)
end = source.index(end_marker, start) + len(end_marker)
block = source[start:end].rstrip() + "\n\n"
source = (source[:start].rstrip() + "\n\n" + source[end:].lstrip("\n"))
if source.count(target) != 1:
    raise SystemExit(f"expected one internal-test target, got {source.count(target)}")
source = source.replace(target, block + target, 1)
lib_path.write_text(source, encoding="utf-8", newline="\n")

test = test_path.read_text(encoding="utf-8")
old = 'let end = tail.find("/// The published R3.18W true-only control is recomputed from the supplied R3.18T prior and used").expect("R3.18AA boundary after R3.18AK");'
new = 'let end = tail.find("#[cfg(test)]\\nmod tests {").expect("internal test-module boundary after R3.18AK");'
if test.count(old) != 1:
    raise SystemExit("expected one AK source-scope end marker")
test = test.replace(old, new, 1)
test_path.write_text(test, encoding="utf-8", newline="\n")
print("PASS relocated R3.18AK block after all prior production scope markers")
