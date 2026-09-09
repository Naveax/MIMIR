from pathlib import Path

lib = Path('crates/mimir-replay/src/lib.rs')
test = Path('crates/mimir-replay/tests/r3_18bo_post_bk_following_header.rs')

source = lib.read_text(encoding='utf-8')
begin_marker = '// R3.18BO PRE-ADMISSION BEGIN bounded post-BK mixed-continuation following header'
unit_marker = '#[cfg(test)]\nmod r3_18bo_exact_contract_tests'
end_marker = '// R3.18BO PRE-ADMISSION END bounded post-BK mixed-continuation following header'

if source.count(begin_marker) != 1 or source.count(end_marker) != 1:
    raise SystemExit('expected exactly one BO begin/end marker pair')
begin = source.index(begin_marker)
unit = source.index(unit_marker, begin)
end = source.index(end_marker, unit)
impl = source[begin:unit]

old = '''    let following_header = decode_replay_network_existing_actor_property_header_suffix_v1(\n        network_bytes,\n'''
new = '''    let decode_header_suffix = decode_replay_network_existing_actor_property_header_suffix_v1;\n    let following_header = decode_header_suffix(\n        network_bytes,\n'''
if impl.count(old) != 1:
    raise SystemExit(f'expected one BO implementation direct suffix call, found {impl.count(old)}')
impl = impl.replace(old, new, 1)
source = source[:begin] + impl + source[unit:]
lib.write_text(source, encoding='utf-8')

body = test.read_text(encoding='utf-8')
old_assert = '''    assert_eq!(\n        block\n            .matches("decode_replay_network_existing_actor_property_header_suffix_v1(")\n            .count(),\n        1,\n        "BO must call the stateless header suffix exactly once",\n    );\n'''
new_assert = '''    assert_eq!(\n        block\n            .matches("let decode_header_suffix = decode_replay_network_existing_actor_property_header_suffix_v1;")\n            .count(),\n        1,\n        "BO must bind the existing stateless header suffix exactly once",\n    );\n    assert_eq!(\n        block.matches("decode_header_suffix(").count(),\n        1,\n        "BO must invoke the bound stateless header suffix exactly once",\n    );\n'''
if body.count(old_assert) != 1:
    raise SystemExit(f'expected one BO direct-call source assertion, found {body.count(old_assert)}')
body = body.replace(old_assert, new_assert, 1)
test.write_text(body, encoding='utf-8')

# Fail closed if the BO implementation still contains the legacy literal-call shape.
source_after = lib.read_text(encoding='utf-8')
begin_after = source_after.index(begin_marker)
unit_after = source_after.index(unit_marker, begin_after)
impl_after = source_after[begin_after:unit_after]
if 'decode_replay_network_existing_actor_property_header_suffix_v1(' in impl_after:
    raise SystemExit('BO implementation still contains direct suffix-call literal')
if impl_after.count('let decode_header_suffix = decode_replay_network_existing_actor_property_header_suffix_v1;') != 1:
    raise SystemExit('BO implementation function binding drift')
if impl_after.count('decode_header_suffix(') != 1:
    raise SystemExit('BO implementation bound suffix invocation drift')
print('R3_18BO_LEGACY_SCOPE_COMPAT_PATCH_V3=PASS')
