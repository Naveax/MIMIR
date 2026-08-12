from pathlib import Path

path = Path("crates/mimir-replay/src/lib.rs")
text = path.read_text(encoding="utf-8")
old = '''    fn minimal_footer_lookup_materializer_rejects_utf16_object_text() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        content[object_text_offset..object_text_offset + 4]
            .copy_from_slice(&(-2i32).to_le_bytes());
'''
new = '''    fn minimal_footer_lookup_materializer_rejects_utf16_object_text() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        // Core.Object + trailing NUL occupies 12 bytes. A negative Unreal length of -6
        // keeps the structural byte width at 12, so the scaffold remains valid while the
        // lookup materializer can reject UTF-16 at its own semantic boundary.
        content[object_text_offset..object_text_offset + 4]
            .copy_from_slice(&(-6i32).to_le_bytes());
'''
if text.count(old) != 1:
    raise SystemExit(f"expected exactly one R3.8 UTF-16 fixture block, found {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PASS: corrected R3.8 UTF-16 synthetic fixture without changing parser behavior")
