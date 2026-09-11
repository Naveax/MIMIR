from pathlib import Path
import re

LIB = Path('crates/mimir-replay/src/lib.rs')
TEST = Path('crates/mimir-replay/tests/r3_18bs_post_bo_payload.rs')

source = LIB.read_text(encoding='utf-8')
begin_marker = '// R3.18BS PRE-ADMISSION BEGIN bounded post-BO one-following-payload'
end_marker = '// R3.18BS PRE-ADMISSION END bounded post-BO one-following-payload'
begin = source.find(begin_marker)
end = source.find(end_marker, begin)
if begin < 0 or end < 0:
    raise SystemExit('R3.18BS source markers not found')
end += len(end_marker)
block = source[begin:end]

enums = re.findall(r'pub enum ([A-Za-z0-9_]+)\s*\{', block)
structs = re.findall(r'pub struct ([A-Za-z0-9_]+)\s*\{', block)
fns = re.findall(r'pub fn (decode_[A-Za-z0-9_]+)\s*\(', block)
payload_refs = re.findall(r'pub following_payload:\s*([A-Za-z0-9_]+),', block)
if len(enums) != 1 or len(structs) != 1 or len(fns) != 1 or len(payload_refs) != 1:
    raise SystemExit(
        f'unexpected BS declarations enum={enums} struct={structs} fn={fns} payload_ref={payload_refs}'
    )

old_enum, old_struct, old_fn, old_payload_ref = enums[0], structs[0], fns[0], payload_refs[0]
new_enum = 'ReplayNetworkPostBoFollowingPayloadValueV1'
new_struct = 'ReplayNetworkPostBoFollowingPayloadDecodeV1'
new_fn = 'decode_replay_network_post_bo_following_payload_v1'

block = block.replace(old_enum, new_enum)
block = block.replace(old_payload_ref, new_enum)
block = block.replace(old_struct, new_struct)
block = block.replace(old_fn, new_fn)
source = source[:begin] + block + source[end:]
LIB.write_text(source, encoding='utf-8')

test = TEST.read_text(encoding='utf-8')
patterns = [
    (r'(?m)^\s*[A-Za-z0-9_]+\s+as R3_18BsResultV1,$', f'    {new_struct} as R3_18BsResultV1,'),
    (r'(?m)^\s*[A-Za-z0-9_]+\s+as R3_18BsPayloadValueV1,$', f'    {new_enum} as R3_18BsPayloadValueV1,'),
    (r'(?m)^\s*decode_[A-Za-z0-9_]+\s+as decode_bs,$', f'    {new_fn} as decode_bs,'),
]
for pattern, replacement in patterns:
    test, count = re.subn(pattern, replacement, test, count=1)
    if count != 1:
        raise SystemExit(f'expected exactly one test import rewrite for {pattern}, got {count}')

old_cut = '(expected_start + 7) / 8 + 1'
new_cut = 'expected_start.div_ceil(8) + 1'
if test.count(old_cut) != 1:
    raise SystemExit(f'expected one manual div-ceil expression, got {test.count(old_cut)}')
test = test.replace(old_cut, new_cut, 1)
TEST.write_text(test, encoding='utf-8')

print(f'normalized BS enum declaration: {old_enum} -> {new_enum}')
print(f'normalized BS enum field ref: {old_payload_ref} -> {new_enum}')
print(f'normalized BS result: {old_struct} -> {new_struct}')
print(f'normalized BS decoder: {old_fn} -> {new_fn}')
print('normalized BS truncation cut to u64::div_ceil for clippy -D warnings')
