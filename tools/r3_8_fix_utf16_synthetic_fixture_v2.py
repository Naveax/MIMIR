from pathlib import Path

path = Path("crates/mimir-replay/src/lib.rs")
text = path.read_text(encoding="utf-8")
anchor = "fn minimal_footer_lookup_materializer_rejects_utf16_object_text()"
start = text.find(anchor)
if start < 0:
    raise SystemExit("R3.8 UTF-16 test anchor not found")
end = text.find("\n    #[test]", start)
if end < 0:
    raise SystemExit("R3.8 UTF-16 test end marker not found")
block = text[start:end]
old = ".copy_from_slice(&(-2i32).to_le_bytes());"
if block.count(old) != 1:
    raise SystemExit(f"expected one -2 synthetic UTF-16 length in target test, found {block.count(old)}")
new = "// Core.Object + trailing NUL occupies 12 bytes; -6 keeps the scaffold byte width at 12.\n        content[object_text_offset..object_text_offset + 4]\n            .copy_from_slice(&(-6i32).to_le_bytes());"
old_full = "content[object_text_offset..object_text_offset + 4].copy_from_slice(&(-2i32).to_le_bytes());"
if old_full not in block:
    raise SystemExit("formatted target assignment not found")
block = block.replace(old_full, new, 1)
text = text[:start] + block + text[end:]
path.write_text(text, encoding="utf-8")
print("PASS: corrected R3.8 UTF-16 synthetic length to -6 within target test only")
