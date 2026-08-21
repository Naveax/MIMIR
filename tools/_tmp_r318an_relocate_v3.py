from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "crates/mimir-replay/src/lib.rs"
TEST = ROOT / "crates/mimir-replay/tests/r3_18an_post_ak_payload.rs"

BEGIN = "// R3.18AN PRE-ADMISSION BEGIN bounded post-AK payload composition"
END = "// R3.18AN PRE-ADMISSION END bounded post-AK payload composition"
SAFE_MARKER = "/// R3.18J bounded second-property payload value."
AK_END = "// R3.18AK END bounded post-AG following-header composition"
TEST_MODULE = '#[cfg(test)]\nmod tests {'
SOURCE_SCOPE_TEST = "r3_18an_source_scope_is_one_ak_header_one_int_scalar_and_no_next_control_or_loop"

text = LIB.read_text(encoding="utf-8")
for marker in (BEGIN, END, SAFE_MARKER, AK_END, TEST_MODULE):
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"expected exactly one {marker!r}, found {count}")

begin = text.index(BEGIN)
end = text.index(END, begin) + len(END)
block = text[begin:end]

ak_end = text.index(AK_END)
test_module = text.index(TEST_MODULE)
safe = text.index(SAFE_MARKER)
if not (ak_end < begin < test_module < safe):
    raise SystemExit(
        f"unexpected pre-relocation order ak_end={ak_end} begin={begin} test_module={test_module} safe={safe}"
    )

# Remove the generated AN block plus only its directly-adjacent blank lines.
left = text[:begin].rstrip("\n")
right = text[end:].lstrip("\n")
text = left + "\n\n" + right

safe = text.index(SAFE_MARKER)
text = text[:safe].rstrip("\n") + "\n\n" + block.strip("\n") + "\n\n" + text[safe:]

# Post-relocation structural proof: AK ends before the internal test module, while AN lives
# after that module and immediately before the first post-test R3.18J production family.
ak_end = text.index(AK_END)
test_module = text.index(TEST_MODULE)
begin = text.index(BEGIN)
end = text.index(END, begin) + len(END)
safe = text.index(SAFE_MARKER)
if not (ak_end < test_module < begin < end < safe):
    raise SystemExit(
        f"unexpected post-relocation order ak_end={ak_end} test_module={test_module} begin={begin} end={end} safe={safe}"
    )
if text.count(BEGIN) != 1 or text.count(END) != 1:
    raise SystemExit("relocation duplicated or lost AN block")

LIB.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")

test_text = TEST.read_text(encoding="utf-8")
if SOURCE_SCOPE_TEST in test_text:
    raise SystemExit("AN source-scope test already present")

append = r'''

#[test]
fn r3_18an_source_scope_is_one_ak_header_one_int_scalar_and_no_next_control_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin = source
        .find("// R3.18AN PRE-ADMISSION BEGIN bounded post-AK payload composition")
        .expect("R3.18AN begin marker");
    let end_marker = "// R3.18AN PRE-ADMISSION END bounded post-AK payload composition";
    let end = source[begin..]
        .find(end_marker)
        .map(|offset| begin + offset + end_marker.len())
        .expect("R3.18AN end marker");
    let block = &source[begin..end];

    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(")
            .count(),
        1
    );
    assert_eq!(
        block
            .matches("decode_replay_network_primitive_scalar_v1(")
            .count(),
        1
    );
    assert!(!block.contains("cursor.read_bit()"));
    assert!(!block.contains("decode_replay_network_k2_v1("));
    assert!(!block.contains("decode_replay_network_k3_v1("));
    assert!(!block.contains("\n    while "));
    assert!(!block.contains("\n    for "));
}
'''
TEST.write_text(test_text.rstrip() + append + "\n", encoding="utf-8", newline="\n")

print("R3_18AN_RELOCATION_V3=PASS safe_slot=before_r3_18j source_scope_test=1")
