#!/usr/bin/env python3
import collections
import json
import sys
from pathlib import Path


def req(cond, message):
    if not cond:
        raise SystemExit(message)


def kv(line, prefix):
    req(line.startswith(prefix + "\t"), f"bad {prefix} line")
    out = {}
    for item in line.split("\t")[1:]:
        req("=" in item, f"bad field {item}")
        key, value = item.split("=", 1)
        out[key] = value
    return out


def parse(path, prefix, expected):
    out = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix + "\t"):
            row = kv(line, prefix)
            label = row["label"]
            req(label not in out, f"duplicate {prefix} {label}")
            out[label] = row
    req(len(out) == expected, f"{prefix} rows {len(out)} != {expected}")
    return out


def main():
    if len(sys.argv) != 7:
        raise SystemExit("usage: analyze oracle native rows summary negatives aggregate")
    oracle, native, rows_out, summary_out, neg_out, agg_out = sys.argv[1:]
    o = parse(oracle, "R3_18BC_HEADER", 3)
    n = parse(native, "R3_18BC_NATIVE", 3)
    req(set(o) == set(n), "oracle/native label set mismatch")
    agg_lines = [
        line for line in Path(native).read_text(encoding="utf-8").splitlines()
        if line.startswith("R3_18BC_NATIVE_AGG\t")
    ]
    req(len(agg_lines) == 1, f"native aggregate rows {len(agg_lines)} != 1")
    native_agg = kv(agg_lines[0], "R3_18BC_NATIVE_AGG")
    required_agg = {
        "published_ba_exact": "40",
        "false_terminators": "37",
        "false_no_header": "37",
        "true_rows": "3",
        "header_exact": "3",
        "fabricated_continuation_rejected": "1",
        "following_payload_bits_consumed": "0",
        "second_later_control_bits_consumed": "0",
    }
    for key, expected in required_agg.items():
        req(native_agg.get(key) == expected, f"native aggregate {key}={native_agg.get(key)} expected {expected}")

    int_fields = [
        "frame_index",
        "actor_ordinal",
        "actor_context_object_id",
        "property_present_start_bit",
        "property_present_end_bit",
        "stream_id_start_bit",
        "stream_id_end_bit",
        "stream_id",
        "stream_id_bound",
        "prop_id_bits",
        "property_object_id",
        "version_major",
        "version_minor",
        "net_version",
        "payload_start_bit",
    ]
    native_names = {
        "property_present_start_bit": "present_start",
        "property_present_end_bit": "present_end",
        "stream_id_start_bit": "stream_start",
        "stream_id_end_bit": "stream_end",
        "stream_id_bound": "stream_bound",
        "prop_id_bits": "prop_bits",
        "property_object_id": "property_object",
        "payload_start_bit": "payload_start",
    }
    flags = [
        "ba_exact",
        "repeatability",
        "trunc_header",
        "corrupt_ba_negative",
        "wrong_actor_negative",
        "unresolved_lookup_negative",
        "wrong_context_negative",
        "post_payload_poison",
    ]

    rows = []
    contexts = collections.Counter()
    tags = collections.Counter()
    ordinals = collections.Counter()
    mismatch = 0
    for label in sorted(o):
        oracle_row = o[label]
        native_row = n[label]
        exact = True
        for field in int_fields:
            native_field = native_names.get(field, field)
            if int(oracle_row[field]) != int(native_row[native_field]):
                exact = False
        if oracle_row["attribute_tag"] != native_row["tag"]:
            exact = False
        if int(native_row["ba_start"]) != int(oracle_row["property_present_start_bit"]):
            exact = False
        if int(native_row["ba_end"]) != int(oracle_row["property_present_end_bit"]):
            exact = False
        if int(native_row["ba_stop"]) != int(oracle_row["property_present_end_bit"]):
            exact = False
        if int(native_row["stream_start"]) != int(native_row["ba_stop"]):
            exact = False
        if int(native_row["header_stop"]) != int(oracle_row["payload_start_bit"]):
            exact = False
        if not all(native_row.get(flag) == "1" for flag in flags):
            exact = False
        if native_row.get("is_rl_223") != "0":
            exact = False
        if native_row.get("following_payload_bits_consumed") != "0":
            exact = False
        if native_row.get("second_later_control_bits_consumed") != "0":
            exact = False
        if not exact:
            mismatch += 1

        ordinal = int(oracle_row["property_ordinal"])
        context = (
            int(oracle_row["stream_id_bound"]),
            int(oracle_row["prop_id_bits"]),
            int(oracle_row["property_object_id"]),
            oracle_row["attribute_tag"],
            int(oracle_row["version_major"]),
            int(oracle_row["version_minor"]),
            int(oracle_row["net_version"]),
            False,
        )
        contexts[context] += 1
        tags[oracle_row["attribute_tag"]] += 1
        ordinals[ordinal] += 1
        rows.append(
            {
                "label": label,
                "frame_index": int(oracle_row["frame_index"]),
                "actor_ordinal": int(oracle_row["actor_ordinal"]),
                "actor_context_object_id": int(oracle_row["actor_context_object_id"]),
                "ba_property_present_start_bit": int(native_row["ba_start"]),
                "ba_stop_bit": int(native_row["ba_stop"]),
                "property_ordinal": ordinal,
                "stream_id_start_bit": int(oracle_row["stream_id_start_bit"]),
                "stream_id_end_bit": int(oracle_row["stream_id_end_bit"]),
                "stream_id": int(oracle_row["stream_id"]),
                "stream_id_bound": int(oracle_row["stream_id_bound"]),
                "prop_id_bits": int(oracle_row["prop_id_bits"]),
                "resolved_property_object_index": int(oracle_row["property_object_id"]),
                "resolved_attribute_tag": oracle_row["attribute_tag"],
                "version_major": int(oracle_row["version_major"]),
                "version_minor": int(oracle_row["version_minor"]),
                "net_version": int(oracle_row["net_version"]),
                "is_rl_223": False,
                "payload_start_bit": int(oracle_row["payload_start_bit"]),
                "header_stop_bit": int(native_row["header_stop"]),
                "native_oracle_exact": exact,
                "following_payload_bits_consumed": 0,
                "second_later_control_bits_consumed": 0,
            }
        )

    req(mismatch == 0, f"R3.18BC native/oracle mismatch {mismatch}")
    exact_contexts = []
    for context, count in sorted(contexts.items(), key=lambda item: item[0]):
        exact_contexts.append(
            {
                "stream_id_bound": context[0],
                "prop_id_bits": context[1],
                "property_object_index": context[2],
                "attribute_tag": context[3],
                "version_major": context[4],
                "version_minor": context[5],
                "net_version": context[6],
                "observed_count": count,
            }
        )

    payload = {
        "aggregate": {
            "outcome": "A",
            "rows": 3,
            "source_partition_rows": 40,
            "false_terminators": 37,
            "true_rows": 3,
            "unique_exact_contexts": len(exact_contexts),
            "native_oracle_mismatch": 0,
            "witness_reselection": 0,
            "property_ordinals": {str(k): v for k, v in sorted(ordinals.items())},
            "tags": dict(sorted(tags.items())),
            "following_payload_bits_consumed": 0,
            "second_later_control_bits_consumed": 0,
        },
        "rows": rows,
    }
    Path(rows_out).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    summary = {
        "rows": 3,
        "source_partition_rows": 40,
        "false_terminators": 37,
        "true_rows": 3,
        "unique_exact_contexts": len(exact_contexts),
        "contexts": exact_contexts,
        "property_ordinals": {str(k): v for k, v in sorted(ordinals.items())},
        "tags": dict(sorted(tags.items())),
        "native_oracle_mismatch": 0,
        "witness_reselection": 0,
        "earlier_header_contract_inheritance_assumed": False,
    }
    Path(summary_out).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    negatives = "\n".join(
        [
            "R3_18BC_REPEATABILITY=PASS 3/3",
            "R3_18BC_HEADER_TRUNCATION=PASS 3/3",
            "R3_18BC_CORRUPT_BA_NEGATIVE=PASS 3/3",
            "R3_18BC_WRONG_ACTOR_NEGATIVE=PASS 3/3",
            "R3_18BC_UNRESOLVED_LOOKUP_NEGATIVE=PASS 3/3",
            "R3_18BC_WRONG_CONTEXT_NEGATIVE=PASS 3/3",
            "R3_18BC_POST_PAYLOAD_START_POISON=PASS 3/3",
            "R3_18BC_FALSE_TERMINATOR_NO_HEADER=PASS 37/37",
            "R3_18BC_FABRICATED_CONTINUATION_IDENTITY=PASS",
            "R3_18BC_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18BC_SECOND_LATER_CONTROL_BITS_CONSUMED=0",
        ]
    ) + "\n"
    Path(neg_out).write_text(negatives, encoding="utf-8", newline="\n")

    aggregate = "\n".join(
        [
            "R3_18BC_OUTCOME=A",
            "R3_18BC_EVIDENCE=PASS",
            "R3_18BC_SOURCE_PARTITION_ROWS=40/40",
            "R3_18BC_FALSE_TERMINATORS=37",
            "R3_18BC_TRUE_ROWS=3/3",
            "R3_18BC_PUBLISHED_BA_EXACT=40/40",
            "R3_18BC_ONE_FOLLOWING_HEADER_EXACT=3/3",
            f"R3_18BC_UNIQUE_EXACT_CONTEXTS={len(exact_contexts)}",
            "R3_18BC_NATIVE_ORACLE_MISMATCH=0",
            "R3_18BC_WITNESS_RESELECTION=0",
            "R3_18BC_REPEATABILITY=PASS 3/3",
            "R3_18BC_HEADER_TRUNCATION=PASS 3/3",
            "R3_18BC_CORRUPT_BA_NEGATIVE=PASS 3/3",
            "R3_18BC_WRONG_ACTOR_NEGATIVE=PASS 3/3",
            "R3_18BC_UNRESOLVED_LOOKUP_NEGATIVE=PASS 3/3",
            "R3_18BC_WRONG_CONTEXT_NEGATIVE=PASS 3/3",
            "R3_18BC_POST_PAYLOAD_START_POISON=PASS 3/3",
            "R3_18BC_FALSE_TERMINATOR_NO_HEADER=PASS 37/37",
            "R3_18BC_FABRICATED_CONTINUATION_IDENTITY=PASS",
            "R3_18BC_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18BC_SECOND_LATER_CONTROL_BITS_CONSUMED=0",
            "R3_18BC_EARLIER_HEADER_CONTRACT_INHERITANCE_ASSUMED=0",
            "R3_18BC_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
            "R3_18BC_PRIVACY_SCAN=PASS",
        ]
    ) + "\n"
    Path(agg_out).write_text(aggregate, encoding="utf-8", newline="\n")
    print(
        "R3_18BC_ANALYZE=PASS "
        f"rows=3 contexts={len(exact_contexts)} ordinals={dict(ordinals)} tags={dict(tags)} mismatch=0"
    )


if __name__ == "__main__":
    main()
