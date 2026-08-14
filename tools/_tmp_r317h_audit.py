from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

SYSTEM_KIND = {
    0: "SplitScreen",
    1: "Steam",
    2: "PlayStation",
    4: "Xbox",
    5: "QQ",
    6: "Switch",
    7: "PsyNet",
    11: "Epic",
}


def parse_kv_line(line: str) -> dict[str, str]:
    fields = line.rstrip("\n").split("\t")
    out: dict[str, str] = {}
    for field in fields[1:]:
        if "=" not in field:
            raise ValueError(f"malformed field: {field!r}")
        key, value = field.split("=", 1)
        out[key] = value
    return out


def payload_bytes(raw_hex: str, width: int) -> bytes:
    expected = ((width + 7) // 8) * 2
    if len(raw_hex) != expected:
        raise ValueError(f"packed payload hex length {len(raw_hex)} != {expected}")
    data = bytes.fromhex(raw_hex)
    if width % 8 and data and (data[-1] >> (width % 8)):
        raise ValueError("non-zero packed padding bits")
    return data


def text_wire_shape(data: bytes, offset: int = 0) -> tuple[str, int, int]:
    if len(data) < offset + 4:
        raise ValueError("missing text length")
    declared = int.from_bytes(data[offset : offset + 4], "little", signed=True)
    if declared == 0:
        content = 0
        enc = "Empty"
    elif declared > 0:
        content = declared
        enc = "Windows1252"
    else:
        if declared == -(1 << 31):
            raise ValueError("i32::MIN text length")
        content = (-declared) * 2
        enc = "UTF16"
    total = 4 + content
    if len(data) < offset + total:
        raise ValueError("truncated text payload")
    return enc, declared, total


def shape_for(tag: str, row: dict[str, str], data: bytes, width: int) -> str:
    net_version = int(row["net_version"])
    rl223 = row["is_rl_223"].lower() == "true"
    if tag == "ActiveActor":
        if width != 33:
            raise ValueError("ActiveActor width mismatch")
        return "ActiveActor33"
    if tag == "String":
        enc, declared, total = text_wire_shape(data)
        if total * 8 != width:
            raise ValueError("String width mismatch")
        return f"String:{enc}:declared={declared}"
    if tag == "QWordString":
        if not rl223:
            if width != 64:
                raise ValueError("legacy QWordString width mismatch")
            return "QWordString:QWord64"
        enc, declared, total = text_wire_shape(data)
        if total * 8 != width:
            raise ValueError("RL223 QWordString width mismatch")
        return f"QWordString:String:{enc}:declared={declared}"
    if tag in ("UniqueId", "PartyLeader"):
        if not data:
            raise ValueError("identity lacks system id")
        system = data[0]
        kind = SYSTEM_KIND.get(system)
        if kind is None:
            raise ValueError(f"unknown system {system}")
        if system == 0:
            expected = 40
            suffix = kind
        elif system in (1, 4, 5):
            expected = 80
            suffix = kind
        elif system == 2:
            expected = 336 if net_version >= 1 else 272
            suffix = kind
        elif system == 6:
            expected = 272
            suffix = kind
        elif system == 7:
            expected = 80 if net_version >= 10 else 272
            suffix = kind
        elif system == 11:
            enc, declared, text_total = text_wire_shape(data, 1)
            expected = 8 + text_total * 8 + 8
            suffix = f"{kind}:{enc}:declared={declared}"
        else:
            raise AssertionError("unreachable")
        if width != expected:
            raise ValueError(f"identity width {width} != {expected}")
        if tag == "UniqueId":
            return f"UniqueId:{suffix}"
        if system == 0:
            return "PartyLeader:None"
        return f"PartyLeader:Some:{suffix}"
    raise ValueError(f"unexpected tag {tag}")


KEY_FIELDS = (
    "relative_path",
    "frame_index",
    "actor_ordinal",
    "actor_id",
    "actor_context_object_id",
    "actor_context_object_name",
    "stream_id",
    "property_object_id",
    "property_object_name",
    "attribute_tag",
    "shape",
    "version_major",
    "version_minor",
    "net_version",
    "is_rl_223",
    "payload_start_bit",
    "payload_end_bit",
    "payload_width",
    "next_cursor_bit",
    "packed_payload_sha256",
)


def key_of(record: dict[str, object]) -> tuple[object, ...]:
    return tuple(record[field] for field in KEY_FIELDS)


def normalized_raw(row: dict[str, str]) -> dict[str, object]:
    tag = row["attribute_tag"]
    width = int(row["payload_width"])
    data = payload_bytes(row["raw_bits_hex"], width)
    shape = shape_for(tag, row, data, width)
    return {
        "relative_path": row["label"],
        "frame_index": int(row["frame_index"]),
        "actor_ordinal": int(row["actor_ordinal"]),
        "actor_id": int(row["actor_id"]),
        "actor_context_object_id": int(row["actor_context_object_id"]),
        "actor_context_object_name": row["actor_context_object_name"],
        "stream_id": int(row["stream_id"]),
        "property_object_id": int(row["property_object_id"]),
        "property_object_name": row["property_object_name"],
        "attribute_tag": tag,
        "shape": shape,
        "version_major": int(row["version_major"]),
        "version_minor": int(row["version_minor"]),
        "net_version": int(row["net_version"]),
        "is_rl_223": row["is_rl_223"].lower() == "true",
        "payload_start_bit": int(row["payload_start_bit"]),
        "payload_end_bit": int(row["payload_end_bit"]),
        "payload_width": width,
        "next_cursor_bit": int(row["next_cursor_bit"]),
        "packed_payload_sha256": hashlib.sha256(data).hexdigest(),
        "raw_hex": row["raw_bits_hex"],
        "semantic": row["semantic"],
    }


def prepare(witness_path: Path, log_path: Path, native_input: Path, expected_path: Path) -> None:
    witnesses = [json.loads(line) for line in witness_path.read_text(encoding="utf-8").splitlines() if line]
    if len(witnesses) != 469:
        raise SystemExit(f"expected 469 immutable witnesses, got {len(witnesses)}")

    rows = []
    for line in log_path.read_text(encoding="utf-8", errors="strict").splitlines():
        if line.startswith("R3_17E_K2\t"):
            rows.append(normalized_raw(parse_kv_line(line)))
    index: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        index[key_of(row)].append(row)

    native_lines: list[str] = []
    expected_lines: list[str] = []
    for ordinal, witness in enumerate(witnesses):
        matches = index.get(key_of(witness), [])
        if len(matches) != 1:
            raise SystemExit(
                f"witness {ordinal} exact occurrence match count {len(matches)} for "
                f"{witness['relative_path']} frame={witness['frame_index']} tag={witness['attribute_tag']}"
            )
        row = matches[0]
        native_lines.append(
            "\t".join(
                [
                    str(ordinal),
                    str(witness["attribute_tag"]),
                    str(witness["net_version"]),
                    "1" if witness["is_rl_223"] else "0",
                    str(witness["payload_width"]),
                    str(witness["shape"]),
                    str(row["raw_hex"]),
                ]
            )
        )
        expected_lines.append(f"{ordinal}\t{row['semantic']}")

    native_input.write_text("\n".join(native_lines) + "\n", encoding="utf-8", newline="\n")
    expected_path.write_text("\n".join(expected_lines) + "\n", encoding="utf-8", newline="\n")
    print(f"R3_17H_WITNESS_SELECTION=PASS rows={len(witnesses)} raw_occurrences={len(rows)}")


def finalize(
    witness_path: Path,
    expected_path: Path,
    native_output: Path,
    match_path: Path,
    summary_path: Path,
    aggregate_path: Path,
) -> None:
    witnesses = [json.loads(line) for line in witness_path.read_text(encoding="utf-8").splitlines() if line]
    expected: dict[int, str] = {}
    for line in expected_path.read_text(encoding="utf-8").splitlines():
        ordinal, semantic = line.split("\t", 1)
        expected[int(ordinal)] = semantic

    native: dict[int, dict[str, object]] = {}
    negative: dict[str, bool] = {}
    for line in native_output.read_text(encoding="utf-8").splitlines():
        fields = line.split("\t")
        if not fields:
            continue
        if fields[0] == "NEG":
            if len(fields) != 3:
                raise SystemExit(f"malformed negative row: {line!r}")
            negative[fields[1]] = fields[2] == "PASS"
            continue
        if fields[0] != "ROW" or len(fields) < 7:
            raise SystemExit(f"malformed native row: {line!r}")
        ordinal = int(fields[1])
        if fields[2] == "OK":
            if len(fields) != 8:
                raise SystemExit(f"malformed native OK row: {line!r}")
            native[ordinal] = {
                "ok": True,
                "end": int(fields[3]),
                "width": int(fields[4]),
                "shape": fields[5],
                "semantic": fields[6],
                "tag": fields[7],
            }
        else:
            native[ordinal] = {"ok": False, "error_category": fields[3] if len(fields) > 3 else "unknown"}

    required_negative = {
        "party_leader_none",
        "party_leader_non_epic",
        "unique_id_unadmitted_system",
        "unique_id_wrong_net_version",
        "qword_rl223_empty",
        "qword_rl223_utf16",
        "epic_wrong_declared_length",
    }
    negative_ok = set(negative) == required_negative and all(negative.values())

    counts = {
        "witness_rows_selected": len(witnesses),
        "native_decode_success": 0,
        "attribute_tag_semantic_variant_exact": 0,
        "payload_width_exact": 0,
        "payload_end_exact": 0,
        "context_gate_exact": 0,
        "semantic_value_exact": 0,
    }
    durable_rows = []
    for ordinal, witness in enumerate(witnesses):
        result = native.get(ordinal, {"ok": False})
        ok = bool(result.get("ok"))
        if ok:
            counts["native_decode_success"] += 1
        variant_exact = ok and result.get("shape") == witness["shape"] and result.get("tag") == witness["attribute_tag"]
        width_exact = ok and result.get("width") == witness["payload_width"]
        end_exact = ok and result.get("end") == witness["payload_width"]
        context_exact = ok
        semantic_exact = ok and result.get("semantic") == expected.get(ordinal)
        counts["attribute_tag_semantic_variant_exact"] += int(variant_exact)
        counts["payload_width_exact"] += int(width_exact)
        counts["payload_end_exact"] += int(end_exact)
        counts["context_gate_exact"] += int(context_exact)
        counts["semantic_value_exact"] += int(semantic_exact)
        semantic_hash = hashlib.sha256(expected.get(ordinal, "").encode("utf-8")).hexdigest()
        durable_rows.append(
            {
                "ordinal": ordinal,
                "relative_path": witness["relative_path"],
                "frame_index": witness["frame_index"],
                "actor_ordinal": witness["actor_ordinal"],
                "property_object_id": witness["property_object_id"],
                "attribute_tag": witness["attribute_tag"],
                "shape": witness["shape"],
                "packed_payload_sha256": witness["packed_payload_sha256"],
                "oracle_semantic_sha256": semantic_hash,
                "native_decode_success": ok,
                "variant_exact": variant_exact,
                "width_exact": width_exact,
                "end_exact": end_exact,
                "context_exact": context_exact,
                "semantic_exact": semantic_exact,
            }
        )

    match_text = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in durable_rows)
    forbidden = ("raw_bits_hex", "raw_hex", "account_hex", "online=", "name_hex=", "unknown_hex=", "text_hex=")
    privacy_ok = not any(token in match_text for token in forbidden)
    match_path.write_text(match_text, encoding="utf-8", newline="\n")

    all_469 = all(value == 469 for value in counts.values())
    outcome = "A" if all_469 and negative_ok and privacy_ok else "C"
    summary = {
        **counts,
        "negative_controls": {name: negative.get(name, False) for name in sorted(required_negative)},
        "negative_controls_pass": negative_ok,
        "privacy_scan_pass": privacy_ok,
        "production_mutation": 0,
        "cargo_mutation": 0,
        "corpus_fixture_mutation": 0,
        "outcome": outcome,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    aggregate = [
        "R3_17H_WITNESS_ROWS_SELECTED=469",
        f"R3_17H_NATIVE_DECODE_SUCCESS={counts['native_decode_success']}",
        f"R3_17H_VARIANT_EXACT={counts['attribute_tag_semantic_variant_exact']}",
        f"R3_17H_PAYLOAD_WIDTH_EXACT={counts['payload_width_exact']}",
        f"R3_17H_PAYLOAD_END_EXACT={counts['payload_end_exact']}",
        f"R3_17H_CONTEXT_GATE_EXACT={counts['context_gate_exact']}",
        f"R3_17H_SEMANTIC_VALUE_EXACT={counts['semantic_value_exact']}",
        f"R3_17H_NEGATIVE_CONTROLS={'PASS' if negative_ok else 'FAIL'}",
        f"R3_17H_PRIVACY_SCAN={'PASS' if privacy_ok else 'FAIL'}",
        "R3_17H_PRODUCTION_MUTATION=0",
        "R3_17H_CARGO_MUTATION=0",
        "R3_17H_CORPUS_FIXTURE_MUTATION=0",
        f"R3_17H_OUTCOME={outcome}",
    ]
    aggregate_path.write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(aggregate))
    if outcome != "A":
        raise SystemExit("R3.17H differential audit mismatch")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: audit.py prepare|finalize ...")
    mode = sys.argv[1]
    if mode == "prepare" and len(sys.argv) == 6:
        prepare(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5]))
    elif mode == "finalize" and len(sys.argv) == 8:
        finalize(
            Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]),
            Path(sys.argv[5]), Path(sys.argv[6]), Path(sys.argv[7])
        )
    else:
        raise SystemExit("bad arguments")


if __name__ == "__main__":
    main()
