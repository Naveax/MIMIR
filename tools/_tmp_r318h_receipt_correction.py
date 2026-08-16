#!/usr/bin/env python3
import json
from pathlib import Path

MAIN = "3e1fc68eea41378bac07992b5ccfc05485edd4c6"
PROD = "2b608aafae97b10ecbc884f99e4bd4a73abf7a5c"
H_HEAD = "1db03fddabf84bfa189f983fa4a3b9110d105442"
H_RUN = 31960174729
H_JOB = 95196833572
H_ARTIFACT = 9267045757
OLD_API_DIGEST = "sha256:340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645"
NEW_API_DIGEST = "sha256:340f75e22875cb5b00d66f2b4b05bbd6aa9c1a64625d79d0fb5bd0dcc104bb79"
NEW_API_SIZE = 18658
DOWNLOADED_ZIP_SHA256 = "a0101720526e633974390dda46786fc471baa7679f387b7e03d97b5bcf7bcb55"
RECEIPT_FILE_SHA256 = "5a381630b2fc01bdc41babbb1aafe6542ff4bebbf5a99a50618214d546008b2b"
R3_18I_V1_HEAD = "9c2bc511fd20a6ef194fa3ecdce3ebb1ebf5bd3a"
R3_18I_V1_RUN = 31963757848
R3_18I_V1_JOB = 95205621914

HASH_REPLACEMENTS = {
    "38ff92a2448883802b73ea4e2ee0a65f18b83beb782d8f8c87451e2295f37fb8": "b85b1324cca458aa68a7433484831371097492388657401776329801d8b31ab1",
    "97767f90f5f9d46afcb68f568cf28d021f2081ddbf62bb5f2536d8d7d1bf569e": "9c8ace30317132246911e5406cc425af862b61de8a59fe270c3f91a1fbbc7690",
    "de4ca9d70fb7f56aec1c279473c3289b236cfa48e3a17f1faec8942ac3548d10": "88767c2b2087cec0313d10df0d4354c13928f1f8596c4d7e2041f5d4eeefac3",
    "4d0273b85c5af2ae2e2b1fd7b88fd5d876c210d1a20f4cdd544601d649c053c9": "272854040775158cd948dd313dcec5da7cdf6a238050e03b7fc20b8434f8962e",
    "4357bc88426ac50da065875f56bc2f806158080767292c6210623091f6fdc31b": "6ff5e750569b4343518cb9c3fd0d8119f610d515b15434732097176482c8bbbc",
}

CANONICAL = [
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_R3_18H_DECISION.md",
    "docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md",
]


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_all_receipt_values(text):
    text = text.replace(OLD_API_DIGEST, NEW_API_DIGEST)
    for old, new in HASH_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def insert_once(text, marker, block, label):
    if block.strip() in text:
        return text
    if text.count(marker) != 1:
        raise SystemExit(f"{label}: expected one marker, got {text.count(marker)}")
    return text.replace(marker, block + marker, 1)


# 1) Master handbook: repair receipt and leave a durable audit note.
p = CANONICAL[0]
t = replace_all_receipt_values(read(p))
t = t.replace("artifact: 9267045757 / size 12070 bytes", "artifact: 9267045757 / size 18658 bytes")
t = t.replace("artifact: 9267045757\nartifact digest:", "artifact: 9267045757 / size 18658 bytes\nartifact digest:")
block = f'''R3_18H_RECEIPT_CORRECTION:\n  status: DOCUMENTARY CORRECTION ONLY; R3.18H Outcome A remains admitted\n  detected by: R3.18I v1 authority freeze before payload evidence\n  R3.18I v1 non-authority head/run/job: {R3_18I_V1_HEAD} / {R3_18I_V1_RUN} / {R3_18I_V1_JOB} FAILED-BEFORE-EVIDENCE\n  live artifact API metadata: id {H_ARTIFACT} / {NEW_API_SIZE} bytes / {NEW_API_DIGEST} / expired=false at verification\n  downloaded ZIP SHA256: {DOWNLOADED_ZIP_SHA256} (local downloaded ZIP bytes; deliberately distinct from GitHub API artifact digest)\n  final H job receipt and live artifact agree on all seven inner evidence hashes\n  receipt manifest file SHA256: {RECEIPT_FILE_SHA256}\n  semantic aggregate unchanged: Outcome A / 94/94 / 47+47 / Int46+String1 / 32 truncation / mismatch 0 / payload+third 0+0 / mutation 0/0/0/0/0\n  production authority unchanged: {PROD}\n\n'''
t = insert_once(t, "R3_17E_EVIDENCE_CLOSURE:\n", block, "handbook correction insertion")
write(p, t)

# 2) Knowledge graph: repair digest and record why R3.18I v1 stopped.
p = CANONICAL[1]
t = replace_all_receipt_values(read(p))
needle = "      94/94 exact = 47 terminator + 47 continuation / Int=46 String=1 / 32 truncation / 47 no-lookup / mismatch 0 / second payload + third property 0+0\n"
addition = needle + f"      receipt correction: live artifact {H_ARTIFACT} / {NEW_API_SIZE} bytes / {NEW_API_DIGEST}; final job receipt == live seven inner hashes; R3.18I v1 {R3_18I_V1_RUN}/{R3_18I_V1_JOB} stopped before evidence on stale continuity receipt\n"
if "receipt correction: live artifact 9267045757" not in t:
    if t.count(needle) != 1:
        raise SystemExit("kg correction anchor mismatch")
    t = t.replace(needle, addition, 1)
write(p, t)

# 3) Machine-readable continuity state: recursive stale-string repair + explicit correction record.
p = CANONICAL[2]
d = json.loads(read(p))

def walk(v):
    if isinstance(v, dict):
        return {k: walk(x) for k, x in v.items()}
    if isinstance(v, list):
        return [walk(x) for x in v]
    if isinstance(v, str):
        return replace_all_receipt_values(v)
    return v

d = walk(d)
r = d.get("r3_18h")
if isinstance(r, dict):
    for k in list(r):
        lk = k.lower()
        if "artifact" in lk and "size" in lk and r[k] == 12070:
            r[k] = NEW_API_SIZE
        if "artifact" in lk and "digest" in lk:
            r[k] = NEW_API_DIGEST

d["r3_18h_receipt_correction"] = {
    "status": "documentary correction only; semantic Outcome A unchanged",
    "detected_by": "R3.18I v1 authority freeze before payload evidence",
    "r3_18i_v1_non_authority_head": R3_18I_V1_HEAD,
    "r3_18i_v1_run": R3_18I_V1_RUN,
    "r3_18i_v1_job": R3_18I_V1_JOB,
    "r3_18i_v1_result": "FAILED-BEFORE-EVIDENCE",
    "artifact_id": H_ARTIFACT,
    "artifact_size_bytes": NEW_API_SIZE,
    "artifact_api_digest": NEW_API_DIGEST,
    "artifact_expired_at_verification": False,
    "downloaded_zip_sha256": DOWNLOADED_ZIP_SHA256,
    "receipt_manifest_sha256": RECEIPT_FILE_SHA256,
    "final_job_receipt_matches_live_inner_hashes": True,
    "source_scope_sha256": HASH_REPLACEMENTS["38ff92a2448883802b73ea4e2ee0a65f18b83beb782d8f8c87451e2295f37fb8"],
    "replay_identity_sha256": "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf",
    "frozen_witnesses_sha256": "99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7",
    "oracle_regeneration_sha256": HASH_REPLACEMENTS["97767f90f5f9d46afcb68f568cf28d021f2081ddbf62bb5f2536d8d7d1bf569e"],
    "comparison_sha256": HASH_REPLACEMENTS["de4ca9d70fb7f56aec1c279473c3289b236cfa48e3a17f1faec8942ac3548d10"],
    "negative_controls_sha256": HASH_REPLACEMENTS["4d0273b85c5af2ae2e2b1fd7b88fd5d876c210d1a20f4cdd544601d649c053c9"],
    "aggregate_sha256": HASH_REPLACEMENTS["4357bc88426ac50da065875f56bc2f806158080767292c6210623091f6fdc31b"],
    "production_authority_unchanged": PROD,
}
write(p, json.dumps(d, ensure_ascii=False, indent=2) + "\n")

# 4) Human current state.
p = CANONICAL[3]
t = replace_all_receipt_values(read(p))
t = t.replace("artifact                            9267045757 / 12070 bytes", "artifact                            9267045757 / 18658 bytes")
marker = "## 3. R3.18I exact next pass\n"
block = f'''### R3.18H receipt correction\n\nThe first R3.18I evidence attempt (`{R3_18I_V1_HEAD}`, run/job `{R3_18I_V1_RUN} / {R3_18I_V1_JOB}`) stopped at authority freeze before payload evidence because the prior continuity record carried a stale R3.18H artifact receipt. Fresh GitHub API metadata reports artifact `{H_ARTIFACT}` as `{NEW_API_SIZE}` bytes with digest `{NEW_API_DIGEST}`. The final R3.18H job receipt and the currently downloadable artifact agree on all seven inner evidence hashes, and the frozen replay/witness identities plus semantic aggregate are unchanged. Downloaded ZIP SHA256 `{DOWNLOADED_ZIP_SHA256}` is recorded separately from the GitHub API artifact digest. This repairs documentation only; R3.18H Outcome A and production authority remain unchanged.\n\n'''
t = insert_once(t, marker, block, "current state correction insertion")
write(p, t)

# 5) R3.18H decision: exact corrected receipt.
p = CANONICAL[4]
t = replace_all_receipt_values(read(p))
t = t.replace("artifact size                       12070 bytes", "artifact size                       18658 bytes")
marker = "## Hard stop\n"
block = f'''## Receipt correction\n\nThe original continuity publication recorded a stale outer artifact receipt and stale hashes for five regenerated evidence files. R3.18I v1 (`{R3_18I_V1_HEAD}`, `{R3_18I_V1_RUN} / {R3_18I_V1_JOB}`) detected that mismatch at authority freeze and stopped **before any payload evidence**. Fresh GitHub artifact metadata and the final R3.18H job receipt now agree with the downloaded artifact: API digest `{NEW_API_DIGEST}`, size `{NEW_API_SIZE}` bytes, and all seven inner evidence hashes listed above. The downloaded ZIP bytes hash to `{DOWNLOADED_ZIP_SHA256}`; that local ZIP hash is intentionally recorded separately from GitHub's API artifact digest. Receipt manifest file SHA256 is `{RECEIPT_FILE_SHA256}`.\n\nThis is a documentary correction only. Frozen replay identity, frozen witness identity, Outcome A aggregate, zero mismatch, zero second-payload/third-property consumption, zero production mutation and production authority `{PROD}` are unchanged.\n\n'''
t = insert_once(t, marker, block, "decision correction insertion")
write(p, t)

# 6) R3.18I spec: correct prerequisite receipt and retain the failed v1 as non-authority trace.
p = CANONICAL[5]
t = replace_all_receipt_values(read(p))
t = t.replace(
    f"R3.18H artifact                     {H_ARTIFACT} / {NEW_API_DIGEST}",
    f"R3.18H artifact                     {H_ARTIFACT} / {NEW_API_SIZE} bytes / {NEW_API_DIGEST}",
)
marker = "## 3. Exact source lane\n"
block = f'''### Receipt-correction prerequisite\n\nR3.18I v1 authority head `{R3_18I_V1_HEAD}` / run-job `{R3_18I_V1_RUN} / {R3_18I_V1_JOB}` is a **non-authority failed-before-evidence trace**. It correctly rejected the stale R3.18H continuity receipt before oracle regeneration or native payload work. R3.18I may resume only from continuity that records live artifact `{H_ARTIFACT}` as `{NEW_API_SIZE}` bytes / `{NEW_API_DIGEST}` and the final-job/live-artifact inner hashes. Downloaded ZIP SHA256 `{DOWNLOADED_ZIP_SHA256}` is not interchangeable with the API digest.\n\n'''
t = insert_once(t, marker, block, "spec correction insertion")
write(p, t)

# Global fail-closed checks.
for p in CANONICAL:
    t = read(p)
    if OLD_API_DIGEST in t:
        raise SystemExit(f"stale API digest remains in {p}")
    for old in HASH_REPLACEMENTS:
        if old in t:
            raise SystemExit(f"stale inner receipt hash remains in {p}: {old}")
    if NEW_API_DIGEST not in t and p != "docs/continuity/MIMIR_CONTINUITY_STATE.json":
        raise SystemExit(f"new live API digest missing from {p}")

print("R3_18H_RECEIPT_CORRECTION_GENERATOR=PASS")
