from pathlib import Path
import runpy

LIB = Path("crates/mimir-replay/src/lib.rs")
TEST = Path("crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs")

# Reuse the already scientifically exercised v1 materializer, then make the
# smallest API correction required by Clippy and the BA authority model.
runpy.run_path(".github/scripts/r318ba_builder.py", run_name="__main__")

lib = LIB.read_text(encoding="utf-8")
begin = "// R3.18BA PRE-ADMISSION BEGIN bounded post-AY mixed following control"
end = "// R3.18BA PRE-ADMISSION END bounded post-AY mixed following control"
if lib.count(begin) != 1 or lib.count(end) != 1:
    raise SystemExit("BA marker authority drift")
prefix, rest = lib.split(begin, 1)
block, suffix = rest.split(end, 1)

au_parameter = "    au_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,\n"
if block.count(au_parameter) != 1:
    raise SystemExit(f"BA au_prior parameter drift: {block.count(au_parameter)}")
block = block.replace(au_parameter, "", 1)

old_recompute = """            an_prior,
            au_prior,
        )?;"""
new_recompute = """            an_prior,
            &ay_prior.header_composition,
        )?;"""
if block.count(old_recompute) != 1:
    raise SystemExit(f"BA AY recompute authority drift: {block.count(old_recompute)}")
block = block.replace(old_recompute, new_recompute, 1)

old_boundary = """    if ay_prior.header_composition != *au_prior
        || ay_prior.header_composition.stop_bit != payload.payload_start_bit"""
new_boundary = """    if ay_prior.header_composition.stop_bit != payload.payload_start_bit"""
if block.count(old_boundary) != 1:
    raise SystemExit(f"BA redundant AU equality drift: {block.count(old_boundary)}")
block = block.replace(old_boundary, new_boundary, 1)

if "au_prior" in block:
    raise SystemExit("BA redundant au_prior authority remained in scoped block")
lib = prefix + begin + block + end + suffix
LIB.write_text(lib, encoding="utf-8", newline="\n")

test = TEST.read_text(encoding="utf-8")
decode_calls = test.count("decode_ba(")
redundant_calls = test.count(", &au, &")
if decode_calls == 0 or redundant_calls != decode_calls:
    raise SystemExit(
        f"BA focused-call authority drift: decode_calls={decode_calls} redundant_calls={redundant_calls}"
    )
test = test.replace(", &au, &", ", &")
if test.count(", &au, &") != 0 or test.count("decode_ba(") != decode_calls:
    raise SystemExit("BA focused-call normalization drift")
TEST.write_text(test, encoding="utf-8", newline="\n")

print(f"R3.18BA API normalized to seven arguments; focused decode calls={decode_calls}")
