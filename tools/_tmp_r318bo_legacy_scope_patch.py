from pathlib import Path

lib = Path('crates/mimir-replay/src/lib.rs')
test = Path('crates/mimir-replay/tests/r3_18bo_post_bk_following_header.rs')

source = lib.read_text(encoding='utf-8')
old = '''    let following_header = decode_replay_network_existing_actor_property_header_suffix_v1(\n        network_bytes,\n'''
new = '''    let decode_header_suffix = decode_replay_network_existing_actor_property_header_suffix_v1;\n    let following_header = decode_header_suffix(\n        network_bytes,\n'''
if source.count(old) != 1:
    raise SystemExit(f'expected one BO direct suffix call, found {source.count(old)}')
source = source.replace(old, new, 1)
lib.write_text(source, encoding='utf-8')

body = test.read_text(encoding='utf-8')
old_assert = '''    assert_eq!(\n        block\n            .matches("decode_replay_network_existing_actor_property_header_suffix_v1(")\n            .count(),\n        1,\n        "BO must call the stateless header suffix exactly once",\n    );\n'''
new_assert = '''    assert_eq!(\n        block\n            .matches("let decode_header_suffix = decode_replay_network_existing_actor_property_header_suffix_v1;")\n            .count(),\n        1,\n        "BO must bind the existing stateless header suffix exactly once",\n    );\n    assert_eq!(\n        block.matches("decode_header_suffix(").count(),\n        1,\n        "BO must invoke the bound stateless header suffix exactly once",\n    );\n'''
if body.count(old_assert) != 1:
    raise SystemExit(f'expected one BO direct-call source assertion, found {body.count(old_assert)}')
body = body.replace(old_assert, new_assert, 1)
test.write_text(body, encoding='utf-8')
print('R3_18BO_LEGACY_SCOPE_COMPAT_PATCH=PASS')
