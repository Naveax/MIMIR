from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

IDENTITY_NAME = "r3_17a_replay_identity.tsv"
WITNESS_NAME = "r3_17a_scalar_witnesses.jsonl"
IDENTITY_SHA256 = "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf"
WITNESS_SHA256 = "b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9"
EXPECTED_TAGS = {"Boolean", "Byte", "Enum", "Float", "Int", "Int64"}

ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T[^ ]+Z ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_log_line(line: str) -> str:
    line = ANSI.sub("", line)
    return TIMESTAMP.sub("", line, count=1)


def extract_file(lines: list[str], name: str) -> bytes:
    begin = f"R3_17A_FILE_BEGIN\t{name}"
    end = f"R3_17A_FILE_END\t{name}"
    begin_indexes = [i for i, line in enumerate(lines) if line == begin]
    if len(begin_indexes) != 1:
        raise SystemExit(f"expected one {begin!r}, found {len(begin_indexes)}")
    start = begin_indexes[0] + 1
    try:
        finish = lines.index(end, start)
    except ValueError as exc:
        raise SystemExit(f"missing {end!r}") from exc
    payload_lines = lines[start:finish]
    return ("\n".join(payload_lines) + "\n").encode("utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: _tmp_r317d_extract.py <r317a-job-log>")
    log_path = Path(sys.argv[1])
    raw = log_path.read_text(encoding="utf-8-sig", errors="strict")
    lines = [normalize_log_line(line.rstrip("\r")) for line in raw.splitlines()]

    target = Path("target")
    target.mkdir(parents=True, exist_ok=True)
    identity_path = target / "r317d_replay_identity.tsv"
    witness_jsonl_path = target / "r317d_scalar_witnesses.jsonl"
    witness_tsv_path = target / "r317d_scalar_witnesses.tsv"

    identity_bytes = extract_file(lines, IDENTITY_NAME)
    witness_bytes = extract_file(lines, WITNESS_NAME)
    identity_path.write_bytes(identity_bytes)
    witness_jsonl_path.write_bytes(witness_bytes)

    actual_identity_sha = sha256_bytes(identity_bytes)
    actual_witness_sha = sha256_bytes(witness_bytes)
    if actual_identity_sha != IDENTITY_SHA256:
        raise SystemExit(
            f"identity SHA mismatch: {actual_identity_sha} != {IDENTITY_SHA256}"
        )
    if actual_witness_sha != WITNESS_SHA256:
        raise SystemExit(
            f"witness SHA mismatch: {actual_witness_sha} != {WITNESS_SHA256}"
        )

    identities: dict[str, str] = {}
    for line in identity_bytes.decode("utf-8").splitlines():
        fields = line.split("\t")
        if len(fields) != 3 or fields[2] != "PASS":
            raise SystemExit(f"malformed identity row: {line!r}")
        rel, expected_sha, _ = fields
        if rel in identities:
            raise SystemExit(f"duplicate replay identity: {rel}")
        identities[rel] = expected_sha.lower()
    if len(identities) != 47:
        raise SystemExit(f"expected 47 replay identities, got {len(identities)}")

    for rel, expected_sha in identities.items():
        replay = Path(rel)
        if not replay.is_file():
            raise SystemExit(f"missing replay: {rel}")
        actual = sha256_file(replay)
        if actual != expected_sha:
            raise SystemExit(f"replay SHA mismatch for {rel}: {actual} != {expected_sha}")

    witnesses: list[dict[str, object]] = []
    for line in witness_bytes.decode("utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        witnesses.append(row)
    if len(witnesses) != 96:
        raise SystemExit(f"expected 96 immutable witnesses, got {len(witnesses)}")

    counts = Counter(str(row.get("attribute_tag")) for row in witnesses)
    if set(counts) != EXPECTED_TAGS:
        raise SystemExit(f"unexpected witness tags: {dict(counts)}")
    for tag in sorted(EXPECTED_TAGS):
        if counts[tag] != 16:
            raise SystemExit(f"expected 16 {tag} witnesses, got {counts[tag]}")

    tsv_lines: list[str] = []
    for row in witnesses:
        rel = str(row["relative_path"])
        if rel not in identities:
            raise SystemExit(f"witness references replay outside identity set: {rel}")
        tag = str(row["attribute_tag"])
        start = int(row["payload_start_bit"])
        end = int(row["payload_end_bit"])
        width = int(row["payload_width"])
        next_cursor = int(row["next_cursor_bit"])
        if end != start + width:
            raise SystemExit(f"witness span mismatch: {rel} {tag} {start}+{width}!={end}")
        if next_cursor != end:
            raise SystemExit(f"witness cursor mismatch: {rel} {tag} {next_cursor}!={end}")
        if tag == "Float":
            expected = str(int(row["float_raw_u32"]))
        else:
            expected = str(int(row["numeric_value"]))
        tsv_lines.append(
            "\t".join(
                [rel, tag, str(start), str(end), str(width), str(next_cursor), expected]
            )
        )

    witness_tsv_path.write_text("\n".join(tsv_lines) + "\n", encoding="utf-8", newline="\n")
    print(f"R3_17D_IDENTITY_SHA256={actual_identity_sha}")
    print(f"R3_17D_WITNESS_SHA256={actual_witness_sha}")
    print("R3_17D_REPLAY_IDENTITIES=47")
    print("R3_17D_WITNESSES=96")
    for tag in sorted(EXPECTED_TAGS):
        print(f"R3_17D_TAG={tag} witnesses={counts[tag]}")
    print("R3_17D_RECEIPT_EXTRACTION=PASS")


if __name__ == "__main__":
    main()
