import argparse
import json
from pathlib import Path

PAYLOAD_PREFIX = "R3_18I_PAYLOAD\t"
NATIVE_PREFIX = "R3_18I_NATIVE\t"


def parse_kv(line: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in line.rstrip("\n").split("\t")[1:]:
        if "=" not in token:
            raise SystemExit(f"malformed token: {token!r}")
        key, value = token.split("=", 1)
        out[key] = value
    return out


def iv(row: dict[str, str], key: str) -> int:
    try:
        return int(row[key])
    except Exception as exc:
        raise SystemExit(f"invalid integer {key}={row.get(key)!r}: {exc}") from exc


def read_u32_lsb(window_hex: str, global_bit: int, window_byte_start: int) -> int:
    raw = bytes.fromhex(window_hex)
    local = global_bit - window_byte_start * 8
    if local < 0 or local + 32 > len(raw) * 8:
        raise SystemExit("string length prefix outside payload window")
    value = 0
    for offset in range(32):
        bit = local + offset
        value |= ((raw[bit // 8] >> (bit % 8)) & 1) << offset
    return value - (1 << 32) if value & (1 << 31) else value


def build(r318f_request: Path, oracle_log: Path, out_request: Path, out_summary: Path) -> None:
    payloads: dict[str, dict[str, str]] = {}
    for line in oracle_log.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith(PAYLOAD_PREFIX):
            continue
        row = parse_kv(line)
        label = row["label"].replace("\\", "/")
        if label in payloads:
            raise SystemExit(f"duplicate R3.18I payload row: {label}")
        payloads[label] = row

    if len(payloads) != 47:
        raise SystemExit(f"expected 47 second payload oracle rows, got {len(payloads)}")

    output: list[str] = []
    continuation_labels: set[str] = set()
    tags: dict[str, int] = {}
    widths: dict[str, list[int]] = {"Int": [], "String": []}
    string_encoding = None
    string_declared = None

    source_lines = [x for x in r318f_request.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(source_lines) != 94:
        raise SystemExit(f"expected frozen 94 request rows, got {len(source_lines)}")

    for line in source_lines:
        fields = line.split("\t")
        if len(fields) != 26:
            raise SystemExit(f"frozen request field count changed: {len(fields)}")
        cls = fields[0]
        label = fields[1].replace("\\", "/")
        if cls == "terminator":
            if label in payloads:
                raise SystemExit(f"terminator unexpectedly has payload row: {label}")
            output.append("\t".join(fields + ["-1", "0", "None", "none", "none", "0", "0", "None"]))
            continue
        if cls != "continuation":
            raise SystemExit(f"unexpected frozen class: {cls}")
        continuation_labels.add(label)
        row = payloads.get(label)
        if row is None:
            raise SystemExit(f"missing payload oracle row: {label}")
        if row.get("property_ordinal") != "1":
            raise SystemExit(f"wrong payload ordinal: {label}")
        tag = row["second_attribute_tag"]
        if tag not in {"Int", "String"} or row["semantic_kind"] != tag:
            raise SystemExit(f"unsupported/mismatched payload tag: {label} {tag}")
        if fields[24] != tag:
            raise SystemExit(f"frozen second-header tag drift: {label}")
        start = iv(row, "second_payload_start_bit")
        end = iv(row, "second_payload_end_bit")
        width = iv(row, "second_payload_width")
        if start != int(fields[25]) or end <= start or width != end - start:
            raise SystemExit(f"payload boundary mismatch: {label}")
        window_base = iv(row, "window_byte_start")
        if window_base != int(fields[12]):
            raise SystemExit(f"payload window base drift: {label}")
        if iv(row, "window_local_first_start_bit") != int(fields[13]):
            raise SystemExit(f"payload local first start drift: {label}")
        if len(bytes.fromhex(row["window_hex"])) * 8 < end - window_base * 8:
            raise SystemExit(f"payload window does not cover payload end: {label}")

        declared = 0
        encoding = "None"
        if tag == "Int":
            if width != 32 or row["semantic_i32"] == "none" or row["semantic_fnv64"] != "none":
                raise SystemExit(f"invalid Int oracle shape: {label}")
        else:
            if row["semantic_i32"] != "none" or row["semantic_fnv64"] == "none":
                raise SystemExit(f"invalid String oracle shape: {label}")
            declared = read_u32_lsb(row["window_hex"], start, window_base)
            if declared == -(1 << 31):
                raise SystemExit("String oracle has i32::MIN length")
            encoding = "Empty" if declared == 0 else ("Windows1252" if declared > 0 else "Utf16Le")
            expected_width = 32 if declared == 0 else 32 + abs(declared) * (8 if declared > 0 else 16)
            if width != expected_width:
                raise SystemExit(f"String wire width mismatch: {label} got={width} expected={expected_width}")
            string_encoding = encoding
            string_declared = declared

        tags[tag] = tags.get(tag, 0) + 1
        widths[tag].append(width)
        extended = fields.copy()
        extended[12] = row["window_byte_start"]
        extended[13] = row["window_local_first_start_bit"]
        extended[14] = row["window_hex"]
        extended += [
            str(end),
            str(width),
            tag,
            row["semantic_i32"],
            row["semantic_fnv64"],
            row["semantic_utf8_len"],
            str(declared),
            encoding,
        ]
        output.append("\t".join(extended))

    if set(payloads) != continuation_labels:
        raise SystemExit("payload labels differ from frozen 47 continuation labels")
    if tags != {"Int": 46, "String": 1}:
        raise SystemExit(f"unexpected payload tag distribution: {tags}")

    out_request.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "frozen_rows": 94,
        "terminators": 47,
        "continuations": 47,
        "payload_oracle_rows": 47,
        "tags": tags,
        "int_widths": sorted(set(widths["Int"])),
        "string_widths": sorted(set(widths["String"])),
        "string_encoding": string_encoding,
        "string_declared_length": string_declared,
        "third_property_bits_observed": 0,
        "witness_reselection": 0,
    }
    out_summary.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"R3_18I_REQUEST_BUILD=PASS rows=94 Int={tags.get('Int',0)} String={tags.get('String',0)}")


def compare(native_log: Path, out_json: Path, out_aggregate: Path) -> None:
    rows: list[dict[str, str]] = []
    scalars: dict[str, str] = {}
    for line in native_log.read_text(encoding="utf-8").splitlines():
        if line.startswith(NATIVE_PREFIX):
            rows.append(parse_kv(line))
        elif line.startswith("R3_18I_") and "=" in line and "\t" not in line:
            key, value = line.split("=", 1)
            scalars[key] = value

    if len(rows) != 94 or scalars.get("R3_18I_NATIVE_ROWS") != "94":
        raise SystemExit("native row count mismatch")
    required_pass = [
        "R3_18I_WRONG_SCALAR_TAG_NEGATIVE",
        "R3_18I_WRONG_K2_TAG_NEGATIVE",
        "R3_18I_REPEATABILITY",
        "R3_18I_POST_PAYLOAD_POISON",
    ]
    for key in required_pass:
        if scalars.get(key) != "PASS":
            raise SystemExit(f"required negative/control missing: {key}")
    expected_counts = {
        "R3_18I_TERMINATOR_ROWS": "47",
        "R3_18I_CONTINUATION_ROWS": "47",
        "R3_18I_INT_ROWS": "46",
        "R3_18I_STRING_ROWS": "1",
        "R3_18I_TERMINATOR_NO_PAYLOAD_ROWS": "47",
        "R3_18I_PAYLOAD_TRUNCATION_ROWS": "47",
        "R3_18I_THIRD_PROPERTY_BITS_CONSUMED": "0",
        "R3_18I_MISMATCH_COUNT": "0",
    }
    for key, value in expected_counts.items():
        if scalars.get(key) != value:
            raise SystemExit(f"aggregate mismatch {key}={scalars.get(key)!r}, expected {value}")

    privacy_rows = []
    for row in rows:
        cls = row["class"]
        if row.get("reconstruction_exact") != "true" or row.get("repeatability") != "true":
            raise SystemExit(f"row reconstruction/repeatability failure: {row.get('label')}")
        if row.get("third_property_bits_consumed") != "0":
            raise SystemExit("third property consumption observed")
        if cls == "terminator":
            if row.get("tag") != "None" or row.get("payload_exact") != "true":
                raise SystemExit("terminator payload control failure")
        elif cls == "continuation":
            if row.get("tag") not in {"Int", "String"}:
                raise SystemExit("unexpected continuation tag")
            if row.get("payload_exact") != "true" or row.get("semantic_exact") != "true" or row.get("shape_exact") != "true" or row.get("truncation") != "true" or row.get("poison") != "true":
                raise SystemExit(f"continuation payload evidence mismatch: {row.get('label')}")
        else:
            raise SystemExit("unexpected native class")
        privacy_rows.append({
            "class": cls,
            "label": row["label"].replace("\\", "/"),
            "tag": row["tag"],
            "payload_start_bit": int(row["payload_start_bit"]),
            "payload_end_bit": int(row["payload_end_bit"]),
            "payload_width": int(row["payload_width"]),
            "reconstruction_exact": True,
            "payload_exact": row["payload_exact"] == "true",
            "semantic_exact": row["semantic_exact"] == "true",
            "shape_exact": row["shape_exact"] == "true",
            "truncation": row["truncation"] == "true",
            "poison": row["poison"] == "true",
            "third_property_bits_consumed": 0,
        })

    out_json.write_text(json.dumps({"rows": privacy_rows, "aggregate": expected_counts}, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    aggregate = "\n".join([
        "R3_18I_OUTCOME=A",
        "R3_18I_EVIDENCE=PASS",
        "R3_18I_FROZEN_ROWS=94/94",
        "R3_18I_TERMINATOR_ROWS=47",
        "R3_18I_CONTINUATION_ROWS=47",
        "R3_18I_CONTINUATION_INT=46",
        "R3_18I_CONTINUATION_STRING=1",
        "R3_18I_TERMINATOR_NO_PAYLOAD_ROWS=47",
        "R3_18I_PAYLOAD_TRUNCATION_ROWS=47",
        "R3_18I_NATIVE_ORACLE_MISMATCH=0",
        "R3_18I_THIRD_PROPERTY_BITS_CONSUMED=0",
        "R3_18I_WITNESS_RESELECTION=0",
        "R3_18I_WRONG_SCALAR_TAG_NEGATIVE=PASS",
        "R3_18I_WRONG_K2_TAG_NEGATIVE=PASS",
        "R3_18I_REPEATABILITY=PASS",
        "R3_18I_POST_PAYLOAD_POISON=PASS",
    ]) + "\n"
    out_aggregate.write_text(aggregate, encoding="utf-8", newline="\n")
    print("R3_18I_COMPARISON=PASS rows=94 mismatch=0")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("r318f_request", type=Path)
    p.add_argument("oracle_log", type=Path)
    p.add_argument("out_request", type=Path)
    p.add_argument("out_summary", type=Path)
    p = sub.add_parser("compare")
    p.add_argument("native_log", type=Path)
    p.add_argument("out_json", type=Path)
    p.add_argument("out_aggregate", type=Path)
    args = parser.parse_args()
    if args.cmd == "build":
        build(args.r318f_request, args.oracle_log, args.out_request, args.out_summary)
    else:
        compare(args.native_log, args.out_json, args.out_aggregate)


if __name__ == "__main__":
    main()
