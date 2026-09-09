from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


def die(msg: str) -> None:
    raise SystemExit(f"R3.18BP compare failed: {msg}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def i(row: dict[str, str], key: str) -> int:
    try:
        return int(row[key])
    except Exception as exc:
        die(f"invalid integer {key}={row.get(key)!r}: {exc}")


def b01(row: dict[str, str], key: str) -> bool:
    value = row[key]
    if value == "0":
        return False
    if value == "1":
        return True
    die(f"invalid boolean {key}={value!r}")


def exact_context_from_probe(row: dict[str, str]) -> tuple[int, int, int, str, int, int, int, bool]:
    return (
        i(row, "stream_id_bound"),
        i(row, "prop_id_bits"),
        i(row, "property_object_index"),
        row["attribute_tag"],
        i(row, "version_major"),
        i(row, "version_minor"),
        i(row, "net_version"),
        b01(row, "is_rl_223"),
    )


def exact_context_from_contract(row: dict[str, object]) -> tuple[int, int, int, str, int, int, int, bool]:
    return (
        int(row["stream_id_bound"]),
        int(row["prop_id_bits"]),
        int(row["property_object_index"]),
        str(row["attribute_tag"]),
        int(row["version_major"]),
        int(row["version_minor"]),
        int(row["net_version"]),
        bool(row["is_rl_223"]),
    )


def exact_context_from_bm(row: dict[str, object]) -> tuple[int, int, int, str, int, int, int, bool]:
    return (
        int(row["stream_id_bound"]),
        int(row["prop_id_bits"]),
        int(row["resolved_property_object_index"]),
        str(row["resolved_attribute_tag"]),
        int(row["version_major"]),
        int(row["version_minor"]),
        int(row["net_version"]),
        bool(row["is_rl_223"]),
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if len(sys.argv) != 6:
        die("usage: compare.py PROBE_TSV BM_CONTROL_TSV BM_HEADER_JSON BN_CONTRACT_JSON OUT_DIR")
    probe_path, bm_control_path, bm_header_path, bn_contract_path, out_dir = map(Path, sys.argv[1:])
    out_dir.mkdir(parents=True, exist_ok=True)

    probe = read_tsv(probe_path)
    controls = read_tsv(bm_control_path)
    bm_doc = json.loads(bm_header_path.read_text(encoding="utf-8"))
    contract = json.loads(bn_contract_path.read_text(encoding="utf-8"))
    bm_headers = bm_doc.get("rows")
    if not isinstance(bm_headers, list):
        die("BM header rows missing")
    admitted = contract.get("admitted_contexts")
    if not isinstance(admitted, list):
        die("BN admitted_contexts missing")

    if len(probe) != 3 or len(controls) != 3 or len(bm_headers) != 2 or len(admitted) != 2:
        die(f"cardinality drift probe={len(probe)} controls={len(controls)} headers={len(bm_headers)} contract={len(admitted)}")

    probe_by_label = {row["label"]: row for row in probe}
    control_by_label = {row["label"]: row for row in controls}
    bm_by_label = {str(row["label"]): row for row in bm_headers}
    if len(probe_by_label) != 3 or len(control_by_label) != 3 or len(bm_by_label) != 2:
        die("duplicate labels")
    if set(probe_by_label) != set(control_by_label):
        die("witness label reselection")

    false_count = 0
    true_count = 0
    mismatch = 0
    contexts: Counter[tuple[int, int, int, str, int, int, int, bool]] = Counter()
    tags: Counter[str] = Counter()
    ordinals: Counter[int] = Counter()
    result_rows: list[dict[str, object]] = []

    for label in sorted(control_by_label):
        c = control_by_label[label]
        p = probe_by_label[label]
        expected_present = c["next_property_present"] == "1"
        checks = {
            "frame_index": i(p, "frame_index") == int(c["frame_index"]),
            "actor_ordinal": i(p, "actor_ordinal") == int(c["actor_ordinal"]),
            "actor_context_object_id": i(p, "actor_context_object_id") == int(c["actor_context_object_id"]),
            "payload_end": i(p, "bk_payload_end_bit") == int(c["payload_end_bit"]),
            "control_start": i(p, "bk_control_start_bit") == int(c["next_property_present_start_bit"]),
            "control_end": i(p, "bk_control_end_bit") == int(c["next_property_present_end_bit"]),
            "control_value": b01(p, "bk_property_present") == expected_present,
            "bk_stop": i(p, "bk_stop_bit") == int(c["next_property_present_end_bit"]),
            "header_presence": b01(p, "header_present") == expected_present,
        }
        if not all(checks.values()):
            mismatch += 1
            die(f"control/witness mismatch {label}: {checks}")

        if not expected_present:
            false_count += 1
            if label != "external_fixtures/sample_003.replay":
                die(f"unexpected false terminator {label}")
            if i(p, "bo_stop_bit") != i(p, "bk_stop_bit"):
                die("false terminator stop drift")
            optionals = [
                "header_actor_object_index", "header_property_present_start_bit", "header_property_present_end_bit",
                "stream_id_start_bit", "stream_id", "stream_id_bound", "prop_id_bits", "property_object_index",
                "attribute_tag", "payload_start_bit", "header_stop_bit",
            ]
            if any(p[key] != "-" for key in optionals):
                die("false terminator synthesized header fields")
            result_rows.append({"label": label, "classification": "false_terminator", "bo_stop_bit": i(p, "bo_stop_bit")})
            continue

        true_count += 1
        bm = bm_by_label.get(label)
        if bm is None:
            die(f"true row absent from BM header authority: {label}")
        exact_pairs = {
            "property_present_start_bit": i(p, "header_property_present_start_bit") == int(bm["property_present_start_bit"]),
            "property_present_end_bit": i(p, "header_property_present_end_bit") == int(bm["property_present_end_bit"]),
            "stream_id_start_bit": i(p, "stream_id_start_bit") == int(bm["stream_id_start_bit"]),
            "stream_id": i(p, "stream_id") == int(bm["stream_id"]),
            "stream_id_bound": i(p, "stream_id_bound") == int(bm["stream_id_bound"]),
            "prop_id_bits": i(p, "prop_id_bits") == int(bm["prop_id_bits"]),
            "property_object_index": i(p, "property_object_index") == int(bm["resolved_property_object_index"]),
            "attribute_tag": p["attribute_tag"] == str(bm["resolved_attribute_tag"]),
            "payload_start_bit": i(p, "payload_start_bit") == int(bm["payload_start_bit"]),
            "header_stop_bit": i(p, "header_stop_bit") == int(bm["header_stop_bit"]),
            "bo_stop_bit": i(p, "bo_stop_bit") == int(bm["payload_start_bit"]),
            "version_major": i(p, "version_major") == int(bm["version_major"]),
            "version_minor": i(p, "version_minor") == int(bm["version_minor"]),
            "net_version": i(p, "net_version") == int(bm["net_version"]),
            "is_rl_223": b01(p, "is_rl_223") == bool(bm["is_rl_223"]),
            "actor_context_object_id": i(p, "actor_context_object_id") == int(bm["actor_context_object_id"]),
            "actor_ordinal": i(p, "actor_ordinal") == int(bm["actor_ordinal"]),
            "frame_index": i(p, "frame_index") == int(bm["frame_index"]),
        }
        if not all(exact_pairs.values()):
            mismatch += 1
            die(f"BM header mismatch {label}: {exact_pairs}")

        context = exact_context_from_probe(p)
        bm_context = exact_context_from_bm(bm)
        if context != bm_context:
            die(f"context mismatch against BM {label}: {context} != {bm_context}")
        contexts[context] += 1
        tags[p["attribute_tag"]] += 1
        ordinals[int(bm["property_ordinal"])] += 1
        result_rows.append({
            "label": label,
            "classification": "true_header",
            "context": list(context),
            "property_ordinal": int(bm["property_ordinal"]),
            "bo_stop_bit": i(p, "bo_stop_bit"),
            "payload_start_bit": i(p, "payload_start_bit"),
        })

    contract_counter: Counter[tuple[int, int, int, str, int, int, int, bool]] = Counter()
    for row in admitted:
        ctx = exact_context_from_contract(row)
        contract_counter[ctx] += int(row.get("observed_count", 1))
    if contexts != contract_counter:
        die(f"BN exact membership/multiplicity mismatch probe={contexts} contract={contract_counter}")

    if false_count != 1 or true_count != 2 or tags != Counter({"Boolean": 1, "ActiveActor": 1}) or ordinals != Counter({7: 2}):
        die(f"aggregate drift false={false_count} true={true_count} tags={tags} ordinals={ordinals}")
    if mismatch != 0:
        die(f"mismatch count {mismatch}")

    summary = {
        "rows": 3,
        "false_terminators": false_count,
        "true_headers": true_count,
        "exact_bn_contexts": len(contexts),
        "bn_multiplicity_sum": sum(contexts.values()),
        "tags": dict(sorted(tags.items())),
        "property_ordinals": {str(k): v for k, v in sorted(ordinals.items())},
        "published_bo_mismatch": 0,
        "witness_reselection": 0,
        "following_payload_bits_consumed": 0,
        "second_later_control_bits_consumed": 0,
    }
    (out_dir / "r3_18bp_rows.json").write_text(json.dumps(result_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "r3_18bp_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    aggregate = (
        "R3_18BP_OUTCOME=A\n"
        "R3_18BP_EVIDENCE=PASS\n"
        "R3_18BP_ROWS=3/3\n"
        "R3_18BP_FALSE_TERMINATORS=1/1\n"
        "R3_18BP_TRUE_HEADERS=2/2\n"
        "R3_18BP_EXACT_BN_CONTEXTS=2/2\n"
        "R3_18BP_BN_MULTIPLICITY=2\n"
        "R3_18BP_TAGS=Boolean:1,ActiveActor:1\n"
        "R3_18BP_PROPERTY_ORDINAL_7=2/2\n"
        "R3_18BP_PUBLISHED_BO_MISMATCH=0\n"
        "R3_18BP_WITNESS_RESELECTION=0\n"
        "R3_18BP_FOLLOWING_PAYLOAD_BITS_CONSUMED=0\n"
        "R3_18BP_SECOND_LATER_CONTROL_BITS_CONSUMED=0\n"
    )
    (out_dir / "r3_18bp_aggregate.txt").write_text(aggregate, encoding="utf-8")
    print("R3_18BP_COMPARE=PASS")
    print(json.dumps(summary, sort_keys=True))
    print(f"R3_18BP_PROBE_SHA256={sha256(probe_path)}")


if __name__ == "__main__":
    main()
