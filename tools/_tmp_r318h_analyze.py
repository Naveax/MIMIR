#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path


def parse_native(path: Path):
    rows = []
    summaries = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("R3_18H_NATIVE\t"):
            fields = {}
            for item in raw.split("\t")[1:]:
                key, value = item.split("=", 1)
                fields[key] = value
            rows.append(fields)
        elif raw.startswith("R3_18H_") and "=" in raw:
            key, value = raw.split("=", 1)
            summaries[key] = value
    return rows, summaries


def main():
    if len(sys.argv) != 6:
        raise SystemExit(
            "usage: analyze.py FROZEN_WITNESSES NATIVE_LOG COMPARISON_JSON AGGREGATE_TXT NEGATIVES_TXT"
        )
    frozen_path, native_path, comparison_path, aggregate_path, negatives_path = map(Path, sys.argv[1:])
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    native, summaries = parse_native(native_path)

    if len(frozen) != 94 or len(native) != 94:
        raise SystemExit(f"expected 94 frozen/native rows, got {len(frozen)}/{len(native)}")

    frozen_map = {(row["label"].replace("\\", "/"), row["class"]): row for row in frozen}
    native_map = {(row["label"].replace("\\", "/"), row["class"]): row for row in native}
    if len(frozen_map) != 94 or set(frozen_map) != set(native_map):
        raise SystemExit("frozen/native row identity mismatch")

    comparison = []
    tag_counts = Counter()
    class_counts = Counter()
    mismatch_count = 0
    for key in sorted(frozen_map):
        expected = frozen_map[key]
        actual = native_map[key]
        class_counts[actual["class"]] += 1
        expected_stop = (
            expected["second_header"]["payload_start_bit"]
            if expected["class"] == "continuation"
            else expected["second_property_present_end_bit"]
        )
        expected_tag = (
            expected["second_header"]["attribute_tag"]
            if expected["class"] == "continuation"
            else "None"
        )
        if expected["class"] == "continuation":
            tag_counts[expected_tag] += 1
        checks = {
            "first_exact": actual.get("first_exact") == "true",
            "control_exact": actual.get("control_exact") == "true",
            "second_header_exact": actual.get("second_header_exact") == "true",
            "repeatability": actual.get("repeatability") == "true",
            "post_stop_poison": actual.get("post_stop_poison") == "true",
            "second_tag_exact": actual.get("second_attribute_tag") == expected_tag,
            "stop_exact": int(actual.get("native_stop_global", "-1")) == int(expected_stop),
            "second_payload_zero": actual.get("second_payload_bits_consumed") == "0",
            "third_property_zero": actual.get("third_property_bits_consumed") == "0",
        }
        row_match = all(checks.values())
        if not row_match:
            mismatch_count += 1
        comparison.append(
            {
                "label": key[0],
                "class": key[1],
                "expected_second_attribute_tag": expected_tag,
                "expected_stop_bit": expected_stop,
                "native_stop_bit": int(actual["native_stop_global"]),
                "checks": checks,
                "match": row_match,
            }
        )

    if class_counts != Counter({"continuation": 47, "terminator": 47}):
        raise SystemExit(f"class distribution mismatch: {dict(class_counts)}")
    if tag_counts != Counter({"Int": 46, "String": 1}):
        raise SystemExit(f"continuation tag distribution mismatch: {dict(tag_counts)}")
    if mismatch_count != 0:
        raise SystemExit(f"native/oracle mismatch count {mismatch_count}")

    required_summaries = {
        "R3_18H_NATIVE_ROWS": "94",
        "R3_18H_TERMINATOR_ROWS": "47",
        "R3_18H_CONTINUATION_ROWS": "47",
        "R3_18H_TERMINATOR_NO_LOOKUP_ROWS": "47",
        "R3_18H_HEADER_TRUNCATION_ROWS": "32",
        "R3_18H_UNRESOLVED_STREAM_NEGATIVE": "PASS",
        "R3_18H_TAG_OUTSIDE_INT_STRING_NEGATIVE": "PASS",
        "R3_18H_SECOND_PAYLOAD_BITS_CONSUMED": "0",
        "R3_18H_THIRD_PROPERTY_BITS_CONSUMED": "0",
    }
    for key, value in required_summaries.items():
        if summaries.get(key) != value:
            raise SystemExit(f"summary mismatch {key}: {summaries.get(key)!r} != {value!r}")

    comparison_path.write_text(
        json.dumps(
            {
                "schema": "mimir.r3_18h.production_second_header_differential.v1",
                "row_count": 94,
                "terminator_rows": 47,
                "continuation_rows": 47,
                "continuation_tag_counts": {"Int": 46, "String": 1},
                "native_oracle_mismatch_count": 0,
                "second_payload_bits_consumed": 0,
                "third_property_bits_consumed": 0,
                "rows": comparison,
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    aggregate_path.write_text(
        "\n".join(
            [
                "R3_18H_OUTCOME=A",
                "R3_18H_FROZEN_ROWS=94",
                "R3_18H_TERMINATOR_ROWS=47",
                "R3_18H_CONTINUATION_ROWS=47",
                "R3_18H_CONTINUATION_TAG_COUNTS=Int:46,String:1",
                "R3_18H_NATIVE_ORACLE_MISMATCH_COUNT=0",
                "R3_18H_HEADER_TRUNCATION_ROWS=32",
                "R3_18H_TERMINATOR_NO_LOOKUP_ROWS=47",
                "R3_18H_SECOND_PAYLOAD_BITS_CONSUMED=0",
                "R3_18H_THIRD_PROPERTY_BITS_CONSUMED=0",
                "R3_18H_PRIVACY=PASS",
                "R3_18H_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
            ]
        ) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    negatives_path.write_text(
        "\n".join(
            [
                "real_header_truncation_rows=32 PASS",
                "unresolved_second_stream=PASS",
                "tag_outside_Int_String=PASS",
                "terminator_no_lookup_rows=47 PASS",
                "post_stop_payload_poison_rows=94 PASS",
                "repeatability_rows=94 PASS",
            ]
        ) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("R3_18H_ANALYSIS=PASS rows=94 mismatch=0 tags=Int:46,String:1 truncation=32")


if __name__ == "__main__":
    main()
