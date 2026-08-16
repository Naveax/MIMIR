from pathlib import Path
import sys

root = Path(sys.argv[1])
frame = root / "src/network/frame_decoder.rs"
s = frame.read_text(encoding="utf-8")

# R3.18C provides the already-proven property-loop observation seam. R3.18L
# retargets that temporary instrumentation from the after-first-property bit to
# the exact after-second-payload bit and filters to one immutable row per replay.
s = s.replace("R3_18C", "R3_18L").replace("r3_18c", "r3_18l")

label_marker = '''fn r3_18l_label() -> String {
    std::env::var("MIMIR_R3_18L_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\\t', "_")
        .replace('\\r', "_")
        .replace('\\n', "_")
}
'''
if s.count(label_marker) != 1:
    raise SystemExit("R3.18L label helper shape mismatch")
target_helpers = '''fn r3_18l_target_frame() -> usize {
    std::env::var("MIMIR_R3_18L_TARGET_FRAME")
        .expect("R3.18L target frame missing")
        .parse()
        .expect("R3.18L target frame invalid")
}

fn r3_18l_target_actor_ordinal() -> usize {
    std::env::var("MIMIR_R3_18L_TARGET_ACTOR_ORDINAL")
        .expect("R3.18L target actor ordinal missing")
        .parse()
        .expect("R3.18L target actor ordinal invalid")
}

'''
s = s.replace(label_marker, target_helpers + label_marker, 1)

old = "                        if r3_18l_property_ordinal == 1 {\n"
new = '''                        if r3_18l_property_ordinal == 2
                            && frame_index == r3_18l_target_frame()
                            && r3_18l_current_actor_ordinal == r3_18l_target_actor_ordinal()
                        {
'''
if s.count(old) != 1:
    raise SystemExit(f"R3.18L ordinal condition count={s.count(old)}")
s = s.replace(old, new, 1)

# Make the temporary log self-describing. The inherited field names named
# next_property_present already describe the bit after the preceding payload;
# only the ordinal literal needs updating.
if s.count("property_ordinal=0\\tproperty_present_start_bit=") != 1:
    raise SystemExit("R3.18L property ordinal literal shape mismatch")
s = s.replace(
    "property_ordinal=0\\tproperty_present_start_bit=",
    "property_ordinal=2\\tproperty_present_start_bit=",
    1,
)
frame.write_text(s, encoding="utf-8", newline="\n")

old_example = root / "examples/r3_18c_probe.rs"
if not old_example.exists():
    raise SystemExit("R3.18C base probe missing")
example_text = old_example.read_text(encoding="utf-8")
example_text = example_text.replace("R3_18C", "R3_18L").replace("r3_18c", "r3_18l")
new_example = root / "examples/r3_18l_probe.rs"
new_example.write_text(example_text, encoding="utf-8", newline="\n")
old_example.unlink()

print("R3_18L_BOXCARS_EXTENSION=PASS ordinal=2 target_filter=frame+actor")
