from pathlib import Path

path = Path('crates/mimir-replay/src/lib.rs')
text = path.read_text(encoding='utf-8')

needle = '''    let channel_width = u32::BITS - max_channels.leading_zeros();
    let channel_bits_u32 = channel_width.saturating_sub(1);
'''
replacement = '''    let is_lan = match_type == "Lan";
    let qword_string_uses_text = replay_network_qword_string_uses_text_v1(build_version);

    let channel_width = u32::BITS - max_channels.leading_zeros();
    let channel_bits_u32 = channel_width.saturating_sub(1);
'''
if text.count(needle) != 1:
    raise SystemExit('R3.13 borrow correction insertion marker drift')
text = text.replace(needle, replacement, 1)

needle = '''        is_lan: match_type == "Lan",
        qword_string_uses_text: replay_network_qword_string_uses_text_v1(build_version),
'''
replacement = '''        is_lan,
        qword_string_uses_text,
'''
if text.count(needle) != 1:
    raise SystemExit('R3.13 borrow correction struct marker drift')
text = text.replace(needle, replacement, 1)

needle = '''    loop {
        let Some(parent) = replay_network_parent_class_v1(&current) else {
            break;
        };
'''
replacement = '''    while let Some(parent) = replay_network_parent_class_v1(&current) {
'''
if text.count(needle) != 1:
    raise SystemExit('R3.13 hierarchy loop correction marker drift')
text = text.replace(needle, replacement, 1)

path.write_text(text, encoding='utf-8')
print('PASS: corrected R3.13 borrow lifetime and hierarchy loop style')
