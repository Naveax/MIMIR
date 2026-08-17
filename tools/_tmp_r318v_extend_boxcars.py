from pathlib import Path
import sys

root = Path(sys.argv[1])
frame = root / "src/network/frame_decoder.rs"
s = frame.read_text(encoding="utf-8")

# Start from the historically admitted R3.18C observation seam, but retarget it
# to the property-control bit after the third decoded property (the published
# R3.18T following payload). This is evidence-only instrumentation.
s = s.replace("R3_18C", "R3_18V").replace("r3_18c", "r3_18v")

label_marker = '''fn r3_18v_label() -> String {
    std::env::var("MIMIR_R3_18V_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\\t', "_")
        .replace('\\r', "_")
        .replace('\\n', "_")
}
'''
if s.count(label_marker) != 1:
    raise SystemExit("R3.18V label helper shape mismatch")
helpers = '''fn r3_18v_target_frame() -> usize {
    std::env::var("MIMIR_R3_18V_TARGET_FRAME")
        .expect("R3.18V target frame missing")
        .parse()
        .expect("R3.18V target frame invalid")
}

fn r3_18v_target_actor_ordinal() -> usize {
    std::env::var("MIMIR_R3_18V_TARGET_ACTOR_ORDINAL")
        .expect("R3.18V target actor ordinal missing")
        .parse()
        .expect("R3.18V target actor ordinal invalid")
}

'''
s = s.replace(label_marker, helpers + label_marker, 1)

old = "                        if r3_18v_property_ordinal == 1 {\n"
new = '''                        if r3_18v_property_ordinal == 3
                            && frame_index == r3_18v_target_frame()
                            && r3_18v_current_actor_ordinal == r3_18v_target_actor_ordinal()
                        {
'''
if s.count(old) != 1:
    raise SystemExit(f"R3.18V ordinal condition count={s.count(old)}")
s = s.replace(old, new, 1)

if s.count("property_ordinal=0\\tproperty_present_start_bit=") != 1:
    raise SystemExit("R3.18V property ordinal literal shape mismatch")
s = s.replace(
    "property_ordinal=0\\tproperty_present_start_bit=",
    "property_ordinal=3\\tproperty_present_start_bit=",
    1,
)
frame.write_text(s, encoding="utf-8", newline="\n")

old_example = root / "examples/r3_18v_probe.rs"
# R3.18C base patch has already been name-transformed above only in frame source;
# rename/transform the example explicitly.
base_example = root / "examples/r3_18c_probe.rs"
if not base_example.exists():
    raise SystemExit("R3.18C base probe missing")
text = base_example.read_text(encoding="utf-8")
text = text.replace("R3_18C", "R3_18V").replace("r3_18c", "r3_18v")
old_example.write_text(text, encoding="utf-8", newline="\n")
base_example.unlink()

print("R3_18V_BOXCARS_EXTENSION=PASS property_ordinal=3 target_filter=frame+actor")
