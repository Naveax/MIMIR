from pathlib import Path

path = Path('crates/mimir-replay/src/lib.rs')
source = path.read_text(encoding='utf-8')
begin_marker = '// R3.18BU PRE-ADMISSION BEGIN bounded post-BS next property-control'
end_marker = '// R3.18BU PRE-ADMISSION END bounded post-BS next property-control'
begin = source.find(begin_marker)
end = source.find(end_marker, begin)
if begin < 0 or end < 0:
    raise SystemExit('BU source block not found')
end += len(end_marker)
block = source[begin:end]
if block.count('lookup_plan') != 2:
    raise SystemExit(f'unexpected lookup_plan multiplicity: {block.count("lookup_plan")}')
block = block.replace('lookup_plan', 'authority_plan')
updated = source[:begin] + block + source[end:]
if 'lookup_plan' in updated[begin:end]:
    raise SystemExit('BU lookup_plan literal remains')
path.write_text(updated, encoding='utf-8')
print('R3.18BU source normalized for legacy EOF scope without relocation')
