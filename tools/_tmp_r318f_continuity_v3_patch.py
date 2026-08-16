from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: patcher SOURCE DEST')

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
s = src.read_text(encoding='utf-8')


def replace(old: str, new: str, minimum: int = 1) -> None:
    global s
    count = s.count(old)
    if count < minimum:
        raise SystemExit(f'missing replacement anchor ({count} < {minimum}): {old[:120]!r}')
    s = s.replace(old, new)

# Correct immutable R3.18F authority receipts from the fresh run/artifact readback.
replace("EVIDENCE_TREE = '4058b67d72219cbbf0534c6002049202fab487f3'", "EVIDENCE_TREE = '4058b67da82e9fbfcc078e975b26d186ec68e6f0'")
replace('ARTIFACT_ID = 9266197133', 'ARTIFACT_ID = 9264673141')
replace("ARTIFACT_DIGEST = '641a62c1467d7bc56d6b3fd1c9377276a6eec0ab02666c062623afa3955114f3'", "ARTIFACT_DIGEST = 'e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361'")
replace('a6e14057249bccc3643f519774731cb5d03ed1aad6e7337009715601b95d3a7e', '492f63c3cfcb27967426816f97858c8f4ad1d9ebb6ce40719f6d829ff3f0ea55')
replace('79c80c104556e8338a7f3fb943194149743650996c988a2a9136ef5cfa7567b6', 'ba0f63ca5cd09ff48e7f70141f6cc78dacc2307502af6c1e09a9695b2ba52e97')
replace('92c83039872436f3165bcb32b8b6914f6aefdbd0aa03b030235a8c4979ee3301', '99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7')
replace('e19384c00d4ec6650b8781319c3133709375715317406b5745222941423824d7', 'bd6c4d25b02533626485e4fdb000034a39e7c2b5f559d8a09a8a4eb5e5ca80d4')
replace('f4b05f9fe6ca6e081fbffaba431efefc20e14a9e99b9dc5f654016842dec0de5', '53f4a9aefbfcc3d02e5a1501d2849455052c01612ddd299e795e89ad2938ddcd')
replace('9919aa8bfb5e70a48344442bb40c0de7c89ea41f92bc532afa5343b3c469a9b9', '57c90cb3617461aea1a078a7b0f72ae301fd35fc9d7c4f9fe56de6d7633a4a04')

# Correct the final aggregate facts. The old V1 generator was built from a stale summary.
replace('Byte=12 / Enum=1 / Float=4 / Int=28 / Int64=2', 'Int=46 / String=1')
replace("{'Byte': 12, 'Enum': 1, 'Float': 4, 'Int': 28, 'Int64': 2}", "{'Int': 46, 'String': 1}")
replace('Byte=12, Enum=1, Float=4, Int=28 and Int64=2', 'Int=46 and String=1')
replace('Byte   12\nEnum    1\nFloat   4\nInt    28\nInt64   2', 'Int     46\nString   1')
replace('26 real truncation negatives', '32 real truncation negatives')
replace('26 truncation negatives', '32 truncation negatives')
replace('real second-header truncation negatives: 26', 'real second-header truncation negatives: 32')
replace("'header_truncation_rows': 26", "'header_truncation_rows': 32")
replace('Twenty-six real continuation rows exercised exact truncation', 'Thirty-two real continuation rows exercised exact truncation')
replace('real header truncation negatives      26', 'real header truncation negatives      32')

# Correct R3.18G admission semantics. It is an observed second-header context allowlist,
# not a K1 payload allowlist. String is a header tag here; no String payload is decoded.
replace(
    'continuation tag admission is limited to Byte/Enum/Float/Int/Int64 as actually observed in R3.18F',
    'continuation second-header tag admission is limited to the exact R3.18F observed set Int/String; this is header resolution only and does not admit either payload family',
)
replace(
    'continuation tag admission is limited to the exact R3.18F observed set: Byte, Enum, Float, Int, Int64\n  Boolean and all compound/non-observed second-header tags fail closed in this new composition even if some lower-level primitive can represent them',
    'continuation second-header tag admission is limited to the exact R3.18F observed set: Int, String\n  any other second-header tag fails closed in this new composition; String resolution does not invoke or admit the String payload decoder',
)
replace(
    'no new tag/shape/context admission beyond Byte/Enum/Float/Int/Int64 for this second-header API',
    'no second-header tag context outside exact R3.18F observed Int/String; no second-payload shape/context admission',
)
replace(
    "'Boolean or compound/non-observed second-header tag admission in the R3.18G composition'",
    "'second-header tag context outside the exact R3.18F observed Int/String set in the R3.18G composition'",
)
replace(
    'The new composition admits only Byte, Enum, Float, Int and Int64 as second-header tags because those are the exact R3.18F observed set.',
    'The new composition admits only Int and String as second-header tags because those are the exact R3.18F observed set. String is resolved only as a header tag; its payload remains opaque and unconsumed.',
)
replace(
    'Boolean or compound/non-observed second-header tags in R3.18G',
    'second-header tag contexts outside exact Int/String in R3.18G',
)
replace(
    'Its continuation tag allowlist is exactly Byte, Enum, Float, Int and Int64. Second payload remains forbidden.',
    'Its continuation header-tag allowlist is exactly Int and String. This does not admit String payload decoding; every second payload remains forbidden.',
)
replace('require resolved tag in {{Byte, Enum, Float, Int, Int64}}', 'require resolved tag in {{Int, String}}')
replace(
    'Therefore this new composition admits only `Byte`, `Enum`, `Float`, `Int`, `Int64` for a present second header. `Boolean`, K2, K3, K4, unknown or otherwise non-observed second-header tags must fail closed before any second payload read. This does not change the lower-level header primitive\'s existing independent capabilities.',
    'Therefore this new composition admits only `Int` and `String` for a present second header, matching the exact R3.18F continuation lane. `String` here is header resolution only: the K2 String payload decoder is not called or admitted. Any other second-header tag fails closed before any second payload read. This does not change the lower-level header primitive\'s existing independent capabilities.',
)
replace(
    'present second header resolving to a tag outside Byte/Enum/Float/Int/Int64;',
    'present second header resolving to a tag outside the exact R3.18F Int/String header set;',
)
replace(
    'continuation Byte                                              positive\ncontinuation Enum                                              positive\ncontinuation Float                                             positive\ncontinuation Int                                               positive\ncontinuation Int64                                             positive',
    'continuation Int                                               positive\ncontinuation String header                                     positive / payload unconsumed',
)
replace(
    'Boolean second header                                          reject before payload\ncompound/non-observed second header                            reject before payload',
    'tag outside exact Int/String second-header set                 reject before payload',
)
replace('explicit five-tag allowlist;', 'explicit exact Int/String second-header allowlist;')
replace(
    'Boolean or compound/non-observed second-header tag widening;',
    'second-header tag context outside exact R3.18F Int/String widening;',
)
replace(
    'only Byte/Enum/Float/Int/Int64; second payload and third property forbidden',
    'only exact observed Int/String headers; second payload and third property forbidden',
)

# In the machine-readable stop boundary, describe the exact observed header context rather than
# the stale generic/non-observed wording.
replace(
    'No second payload, third property, repeated loop, non-observed second tag, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening.',
    'No second payload, third property, repeated loop, second-header tag outside exact Int/String, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening.',
)

# Ensure no stale authority/policy fragments survive in the patched generator.
for forbidden in [
    '4058b67d72219cbbf0534c6002049202fab487f3',
    '9266197133',
    '641a62c1467d7bc56d6b3fd1c9377276a6eec0ab02666c062623afa3955114f3',
    'Byte=12',
    'Enum=1',
    'Int64=2',
    '26 real truncation negatives',
    'explicit five-tag allowlist',
    'require resolved tag in {{Byte, Enum, Float, Int, Int64}}',
]:
    if forbidden in s:
        raise SystemExit(f'stale R3.18F fragment survived: {forbidden}')

# Positive V3 anchors.
for required in [
    "EVIDENCE_TREE = '4058b67da82e9fbfcc078e975b26d186ec68e6f0'",
    'ARTIFACT_ID = 9264673141',
    "'continuation_attribute_tag_counts': {'Int': 46, 'String': 1}",
    "'header_truncation_rows': 32",
    'require resolved tag in {{Int, String}}',
    'String resolution does not invoke or admit the String payload decoder',
]:
    if required not in s:
        raise SystemExit(f'corrected R3.18F anchor missing: {required}')

dst.write_text(s, encoding='utf-8', newline='\n')
print('R3_18F_CONTINUITY_V3_PATCH=PASS')
