from pathlib import Path
import sys

root = Path(sys.argv[1])
frame = root / "src/network/frame_decoder.rs"
s = frame.read_text(encoding="utf-8")

# Evidence-only. Start from the historically admitted R3.18C observation seam,
# but target the exact frozen R3.18AN.stop_bit rather than guessing a property
# ordinal. The observation is additionally pinned to the frozen frame and actor
# ordinal. No following stream/header/payload or second control is decoded.
s = s.replace("R3_18C", "R3_18AP").replace("r3_18c", "r3_18ap")

label_marker = '''fn r3_18ap_label() -> String {
    std::env::var("MIMIR_R3_18AP_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\\t', "_")
        .replace('\\r', "_")
        .replace('\\n', "_")
}
'''
if s.count(label_marker) != 1:
    raise SystemExit("R3.18AP label helper shape mismatch")
helpers = '''fn r3_18ap_target_frame() -> usize {
    std::env::var("MIMIR_R3_18AP_TARGET_FRAME")
        .expect("R3.18AP target frame missing")
        .parse()
        .expect("R3.18AP target frame invalid")
}

fn r3_18ap_target_actor_ordinal() -> usize {
    std::env::var("MIMIR_R3_18AP_TARGET_ACTOR_ORDINAL")
        .expect("R3.18AP target actor ordinal missing")
        .parse()
        .expect("R3.18AP target actor ordinal invalid")
}

fn r3_18ap_target_control_start() -> usize {
    std::env::var("MIMIR_R3_18AP_TARGET_CONTROL_START")
        .expect("R3.18AP target control start missing")
        .parse()
        .expect("R3.18AP target control start invalid")
}

'''
s = s.replace(label_marker, helpers + label_marker, 1)

old = "                        if r3_18ap_property_ordinal == 1 {\n"
new = '''                        if frame_index == r3_18ap_target_frame()
                            && r3_18ap_current_actor_ordinal == r3_18ap_target_actor_ordinal()
                            && r3_18ap_property_present_start_bit == r3_18ap_target_control_start()
                        {
'''
if s.count(old) != 1:
    raise SystemExit(f"R3.18AP observation condition count={s.count(old)}")
s = s.replace(old, new, 1)

literal = "property_ordinal=0\\tproperty_present_start_bit="
if s.count(literal) != 1:
    raise SystemExit("R3.18AP property ordinal log literal shape mismatch")
s = s.replace(literal, "property_ordinal=target\\tproperty_present_start_bit=", 1)
frame.write_text(s, encoding="utf-8", newline="\n")

base_example = root / "examples/r3_18c_probe.rs"
out_example = root / "examples/r3_18ap_probe.rs"
if not base_example.exists():
    raise SystemExit("R3.18C base probe missing")
text = base_example.read_text(encoding="utf-8")
text = text.replace("R3_18C", "R3_18AP").replace("r3_18c", "r3_18ap")
out_example.write_text(text, encoding="utf-8", newline="\n")
base_example.unlink()

print("R3_18AP_BOXCARS_EXTENSION=PASS target=frame+actor+exact_control_start")
