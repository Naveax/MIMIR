import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW = ROOT / "docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json"
LIB = ROOT / "crates/mimir-replay/src/lib.rs"
GROUPS = ROOT / "crates/mimir-replay/src/k3_admitted_groups.rs"
TEST = ROOT / "crates/mimir-replay/tests/r3_17k_k3_attribute_decoder.rs"
IMPL = ROOT / "tools/_tmp_r317k_k3_impl.rs.txt"
TEST_TEMPLATE = ROOT / "tools/_tmp_r317k_test_template.rs.txt"

data = json.loads(ALLOW.read_text(encoding="utf-8"))
allowed = data["allowed"]
location = [int(v) for v in allowed["location_codes"]]
rigid = [int(v) for v in allowed["rigid_body_codes"]]
pickup = [int(v) for v in allowed["pickup_new_codes"]]
boost = [int(v) for v in allowed["replicated_boost_codes"]]

assert len(location) == 11 and len(set(location)) == 11 and location == sorted(location)
assert len(rigid) == 1934 and len(set(rigid)) == 1934 and rigid == sorted(rigid)
assert len(pickup) == 4 and len(set(pickup)) == 4 and pickup == sorted(pickup)
assert len(boost) == 1 and len(set(boost)) == 1 and boost == sorted(boost)
assert data["context"] == {"net_version": 10, "version_major": 868, "version_minor": 32}

def rust_array(name, values, visibility=""):
    prefix = f"{visibility} " if visibility else ""
    lines = [f"{prefix}const {name}: &[u32] = &["]
    for i in range(0, len(values), 12):
        lines.append("    " + ", ".join(str(v) for v in values[i:i + 12]) + ",")
    lines.append("];\n")
    return "\n".join(lines)

groups = """// @generated from docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json.
// Canonical allowlist SHA-256:
// 9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
// Widening requires a new evidence/contract pass.

"""
groups += rust_array("LOCATION_CODES", location, "pub(crate)")
groups += rust_array("RIGID_BODY_CODES", rigid, "pub(crate)")
groups += rust_array("PICKUP_NEW_CODES", pickup, "pub(crate)")
groups += rust_array("REPLICATED_BOOST_CODES", boost, "pub(crate)")
groups += """pub(crate) fn location_contains(code: u32) -> bool {
    LOCATION_CODES.binary_search(&code).is_ok()
}

pub(crate) fn rigid_body_contains(code: u32) -> bool {
    RIGID_BODY_CODES.binary_search(&code).is_ok()
}

pub(crate) fn pickup_new_contains(code: u32) -> bool {
    PICKUP_NEW_CODES.binary_search(&code).is_ok()
}

pub(crate) fn replicated_boost_contains(code: u32) -> bool {
    REPLICATED_BOOST_CODES.binary_search(&code).is_ok()
}
"""
GROUPS.write_text(groups, encoding="utf-8", newline="\n")

lib = LIB.read_text(encoding="utf-8")
module_marker = "use std::path::PathBuf;\n"
insert_marker = "/// This result is deliberately one-value only. `stop_bit` is exactly the first bit\n"
assert module_marker in lib and "mod k3_admitted_groups;" not in lib
assert insert_marker in lib and "pub struct ReplayNetworkK3DecodeContextV1" not in lib
lib = lib.replace(module_marker, module_marker + "\nmod k3_admitted_groups;\n", 1)
lib = lib.replace(insert_marker, IMPL.read_text(encoding="utf-8") + "\n\n" + insert_marker, 1)
LIB.write_text(lib, encoding="utf-8", newline="\n")

template = TEST_TEMPLATE.read_text(encoding="utf-8")
for marker, name, values in [
    ("@@LOCATION_CODES@@", "LOCATION_CODES", location),
    ("@@RIGID_BODY_CODES@@", "RIGID_BODY_CODES", rigid),
    ("@@PICKUP_NEW_CODES@@", "PICKUP_NEW_CODES", pickup),
    ("@@REPLICATED_BOOST_CODES@@", "REPLICATED_BOOST_CODES", boost),
]:
    assert marker in template
    template = template.replace(marker, rust_array(name, values).rstrip(), 1)
TEST.write_text(template, encoding="utf-8", newline="\n")

print(f"generated groups: {len(location) + len(rigid) + len(pickup) + len(boost)}")
print(GROUPS.relative_to(ROOT))
print(TEST.relative_to(ROOT))
print(LIB.relative_to(ROOT))
