from pathlib import Path

path = Path("crates/mimir-replay/src/lib.rs")
text = path.read_text(encoding="utf-8")

old_doc = "///\n\n/// Caller-resolved context for one evidence-admitted K2 payload decode."
new_doc = "/// Caller-resolved context for one evidence-admitted K2 payload decode."
if old_doc not in text:
    raise SystemExit("R3.17G orphan doc-comment pattern not found")
text = text.replace(old_doc, new_doc, 1)

section_start = text.index("fn replay_network_k2_error")
section_end = text.index("/// This result is deliberately one-value only.", section_start)
section = text[section_start:section_end]
if "cursor.bit_position = start;" not in section:
    raise SystemExit("R3.17G rollback assignments not found")
section = section.replace(
    "cursor.bit_position = start;",
    "network_k2_reset_cursor(&mut cursor, start);",
)
helper_marker = "fn replay_network_k2_error(category: &str, detail: impl Into<String>) -> MimirError {"
helper = '''fn network_k2_reset_cursor(cursor: &mut NetworkBitCursor<'_>, start: usize) {\n    cursor.bit_position = start;\n    debug_assert_eq!(cursor.position_bits(), start);\n}\n\n'''
section = section.replace(helper_marker, helper + helper_marker, 1)
text = text[:section_start] + section + text[section_end:]
path.write_text(text, encoding="utf-8", newline="\n")
print("R3.17G clippy fixes applied")
