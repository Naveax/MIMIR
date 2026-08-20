from pathlib import Path
import sys

root = Path(sys.argv[1])
frame = root / "src/network/frame_decoder.rs"
s = frame.read_text(encoding="utf-8")

# Evidence-only: start from the historically admitted R3.18C observation seam,
# rename it for AF, then retarget the observation to the property-control bit
# after the published R3.18AD ordinal-3 payload. No next stream/header/payload
# is decoded by this instrumentation.
s = s.replace("R3_18C", "R3_18AF").replace("r3_18c", "r3_18af")

label_marker = '''fn r3_18af_label() -> String {
    std::env::var("MIMIR_R3_18AF_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\\t', "_")
        .replace('\\r', "_")
        .replace('\\n', "_")
}
'''
if s.count(label_marker) != 1:
    raise SystemExit("R3.18AF label helper shape mismatch")
helpers = '''fn r3_18af_target_frame() -> usize {
    std::env::var("MIMIR_R3_18AF_TARGET_FRAME")
        .expect("R3.18AF target frame missing")
        .parse()
        .expect("R3.18AF target frame invalid")
}

fn r3_18af_target_actor_ordinal() -> usize {
    std::env::var("MIMIR_R3_18AF_TARGET_ACTOR_ORDINAL")
        .expect("R3.18AF target actor ordinal missing")
        .parse()
        .expect("R3.18AF target actor ordinal invalid")
}

'''
s = s.replace(label_marker, helpers + label_marker, 1)

old = "                        if r3_18af_property_ordinal == 1 {\n"
new = '''                        if r3_18af_property_ordinal == 4
                            && frame_index == r3_18af_target_frame()
                            && r3_18af_current_actor_ordinal == r3_18af_target_actor_ordinal()
                        {
'''
if s.count(old) != 1:
    raise SystemExit(f"R3.18AF ordinal condition count={s.count(old)}")
s = s.replace(old, new, 1)

literal = "property_ordinal=0\\tproperty_present_start_bit="
if s.count(literal) != 1:
    raise SystemExit("R3.18AF property ordinal literal shape mismatch")
s = s.replace(literal, "property_ordinal=4\\tproperty_present_start_bit=", 1)
frame.write_text(s, encoding="utf-8", newline="\n")

base_example = root / "examples/r3_18c_probe.rs"
out_example = root / "examples/r3_18af_probe.rs"
if not base_example.exists():
    raise SystemExit("R3.18C base probe missing")
text = base_example.read_text(encoding="utf-8")
text = text.replace("R3_18C", "R3_18AF").replace("r3_18c", "r3_18af")
out_example.write_text(text, encoding="utf-8", newline="\n")
base_example.unlink()

print("R3_18AF_BOXCARS_EXTENSION=PASS property_ordinal=4 target_filter=frame+actor")
