from pathlib import Path
import re

lib_path = Path("crates/mimir-replay/src/lib.rs")
test_path = Path("crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs")

lib = lib_path.read_text(encoding="utf-8")
old_sig = '''    an_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,\n    au_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,\n    ay_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,\n'''
new_sig = '''    an_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,\n    ay_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,\n'''
if lib.count(old_sig) != 1:
    raise SystemExit(f"expected one BA signature arity block, got {lib.count(old_sig)}")
lib = lib.replace(old_sig, new_sig, 1)

old_call = '''            context,\n            an_prior,\n            au_prior,\n        )?;'''
new_call = '''            context,\n            an_prior,\n            &ay_prior.header_composition,\n        )?;'''
if lib.count(old_call) != 1:
    raise SystemExit(f"expected one AY recompute call tail, got {lib.count(old_call)}")
lib = lib.replace(old_call, new_call, 1)

old_if = '''    if ay_prior.header_composition != *au_prior\n        || ay_prior.header_composition.stop_bit != payload.payload_start_bit'''
new_if = '''    if ay_prior.header_composition.stop_bit != payload.payload_start_bit'''
if lib.count(old_if) != 1:
    raise SystemExit(f"expected one redundant AU equality check, got {lib.count(old_if)}")
lib = lib.replace(old_if, new_if, 1)
lib_path.write_text(lib, encoding="utf-8", newline="\n")

test = test_path.read_text(encoding="utf-8")
test = test.replace("&an, &au, &", "&an, &")
pattern = re.compile(r'(&an,\n)([ \t]*)&au,\n\2&')
previous = None
while previous != test:
    previous = test
    test = pattern.sub(r'\1\2&', test)
if "decode_ba" not in test:
    raise SystemExit("BA test unexpectedly missing decode_ba")
if re.search(r'decode_ba\([^;]*?&an,\s*&au,', test, re.S):
    raise SystemExit("an explicit AU argument remains in a BA call")
test_path.write_text(test, encoding="utf-8", newline="\n")
