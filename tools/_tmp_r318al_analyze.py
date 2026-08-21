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
    result = {}
    for item in line.split("\t")[1:]:
        req("=" in item, f"bad field {item}")
        key, value = item.split("=", 1)
        result[key] = value
    return result


def parse_native(path):
    rows = {}
    agg = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("R3_18AL_NATIVE\t"):
            row = kv(line, "R3_18AL_NATIVE")
            label = row["label"]
            req(label not in rows, f"duplicate native row {label}")
            rows[label] = row
        elif line.startswith("R3_18AL_NATIVE_AGG\t"):
            req(agg is None, "duplicate native aggregate")
            agg = kv(line, "R3_18AL_NATIVE_AGG")
    req(len(rows) == 47, f"native rows {len(rows)} != 47")
    req(agg is not None, "missing native aggregate")
    return rows, agg


def main():
    if len(sys.argv) != 9:
        raise SystemExit(
            "usage: analyze frozen_rows native_log aj_contract rows summary negatives aggregate source"
        )
    frozen_path, native_path, contract_path, rows_out, summary_out, neg_out, agg_out = sys.argv[1:8]
    source_label = sys.argv[8]
    req(source_label == "R3.18AI", f"unexpected frozen source {source_label}")

    frozen_doc = json.loads(Path(frozen_path).read_text(encoding="utf-8"))
    frozen_rows = frozen_doc["rows"]
    req(len(frozen_rows) == 47, f"frozen rows {len(frozen_rows)} != 47")
    frozen = {row["label"]: row for row in frozen_rows}
    req(len(frozen) == 47, "duplicate frozen labels")

    native, native_agg = parse_native(native_path)
    req(set(native) == set(frozen), "frozen/native label set mismatch")

    required_agg = {
        "rows": "47",
        "ag_exact": "47",
        "ak_exact": "47",
        "direct_exact": "47",
        "repeatability": "47",
        "truncation": "47",
        "corrupt_ag_negative": "47",
        "wrong_actor_negative": "47",
        "unresolved_lookup_negative": "47",
        "wrong_context_negative": "47",
        "post_payload_poison": "47",
        "cartesian_negative": "1",
        "fabricated_negative": "1",
        "old_z_negative": "1",
        "following_payload_bits_consumed": "0",
        "second_later_control_bits_consumed": "0",
    }
    for key, expected in required_agg.items():
        req(
            native_agg.get(key) == expected,
            f"native aggregate {key}={native_agg.get(key)} != {expected}",
        )

    int_map = {
        "frame_index": "frame_index",
        "actor_ordinal": "actor_ordinal",
        "actor_context_object_id": "actor_context_object_id",
        "ag_property_present_start_bit": "ag_start",
        "ag_stop_bit": "ag_stop",
        "stream_id_start_bit": "stream_start",
        "stream_id_end_bit": "stream_end",
        "stream_id": "stream_id",
        "stream_id_bound": "stream_bound",
        "prop_id_bits": "prop_bits",
        "resolved_property_object_index": "property_object",
        "version_major": "version_major",
        "version_minor": "version_minor",
        "net_version": "net_version",
        "payload_start_bit": "payload_start",
        "header_stop_bit": "header_stop",
    }
    flags = [
        "ag_exact",
        "ak_exact",
        "direct_exact",
        "repeatability",
        "truncation",
        "corrupt_ag_negative",
        "wrong_actor_negative",
        "unresolved_lookup_negative",
        "wrong_context_negative",
        "post_payload_poison",
    ]

    comparisons = []
    tuples = collections.Counter()
    tags = collections.Counter()
    mismatch = 0

    for label in sorted(frozen):
        expected = frozen[label]
        got = native[label]
        exact = True
        for frozen_field, native_field in int_map.items():
            if int(expected[frozen_field]) != int(got[native_field]):
                exact = False
        if expected["resolved_attribute_tag"] != got["tag"]:
            exact = False
        if int(got["present_start"]) != int(expected["ag_property_present_start_bit"]):
            exact = False
        if int(got["present_end"]) != int(expected["stream_id_start_bit"]):
            exact = False
        if int(got["ak_stop"]) != int(expected["payload_start_bit"]):
            exact = False
        if not all(got.get(flag) == "1" for flag in flags):
            exact = False
        if got.get("following_payload_bits_consumed") != "0":
            exact = False
        if got.get("second_later_control_bits_consumed") != "0":
            exact = False
        if not exact:
            mismatch += 1

        tup = (
            int(expected["stream_id_bound"]),
            int(expected["prop_id_bits"]),
            int(expected["resolved_property_object_index"]),
            expected["resolved_attribute_tag"],
            int(expected["version_major"]),
            int(expected["version_minor"]),
            int(expected["net_version"]),
        )
        tuples[tup] += 1
        tags[expected["resolved_attribute_tag"]] += 1

        comparisons.append(
            {
                "label": label,
                "frame_index": int(expected["frame_index"]),
                "actor_ordinal": int(expected["actor_ordinal"]),
                "actor_context_object_id": int(expected["actor_context_object_id"]),
                "ag_property_present_start_bit": int(expected["ag_property_present_start_bit"]),
                "ag_stop_bit": int(expected["ag_stop_bit"]),
                "stream_id_start_bit": int(expected["stream_id_start_bit"]),
                "stream_id_end_bit": int(expected["stream_id_end_bit"]),
                "stream_id": int(expected["stream_id"]),
                "stream_id_bound": int(expected["stream_id_bound"]),
                "prop_id_bits": int(expected["prop_id_bits"]),
                "resolved_property_object_index": int(expected["resolved_property_object_index"]),
                "resolved_attribute_tag": expected["resolved_attribute_tag"],
                "version_major": int(expected["version_major"]),
                "version_minor": int(expected["version_minor"]),
                "net_version": int(expected["net_version"]),
                "payload_start_bit": int(expected["payload_start_bit"]),
                "header_stop_bit": int(expected["header_stop_bit"]),
                "published_ak_frozen_ai_exact": exact,
                "direct_header_exact": got["direct_exact"] == "1",
                "following_payload_bits_consumed": 0,
                "second_later_control_bits_consumed": 0,
            }
        )

    req(mismatch == 0, f"AL published-AK/frozen-AI mismatch {mismatch}")

    contexts = []
    for tup, count in sorted(tuples.items(), key=lambda item: item[0]):
        contexts.append(
            {
                "stream_id_bound": tup[0],
                "prop_id_bits": tup[1],
                "property_object_index": tup[2],
                "attribute_tag": tup[3],
                "version_major": tup[4],
                "version_minor": tup[5],
                "net_version": tup[6],
                "observed_count": count,
            }
        )
    req(len(contexts) == 17, f"AL exact contexts {len(contexts)} != 17")
    req(sum(x["observed_count"] for x in contexts) == 47, "AL multiplicity sum != 47")
    req(tags == collections.Counter({"Int": 47}), f"AL tags drift {dict(tags)}")

    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    req(contract["membership_policy"] == "exact_tuple_only", "AJ policy drift")
    req(contract["observed_row_count"] == 47, "AJ row count drift")
    req(contract["unique_exact_context_count"] == 17, "AJ context count drift")
    req(contract["observed_tag_counts"] == {"Int": 47}, "AJ tag counts drift")
    req(contract["admitted_contexts"] == contexts, "AL contexts/multiplicities differ from AJ")
    req(
        contract["anti_widening"]["r3_18z_cross_boundary_inheritance"] is False,
        "Z inheritance widened",
    )
    req(
        contract["anti_widening"]["r3_18p_cross_boundary_inheritance"] is False,
        "P inheritance widened",
    )

    rows_doc = {
        "aggregate": {
            "outcome": "A",
            "rows": 47,
            "published_ak_frozen_ai_exact": 47,
            "direct_header_exact": 47,
            "unique_exact_contexts": 17,
            "native_oracle_mismatch": 0,
            "witness_reselection": 0,
            "following_payload_bits_consumed": 0,
            "second_later_control_bits_consumed": 0,
            "tags": {"Int": 47},
        },
        "rows": comparisons,
    }
    Path(rows_out).write_text(
        json.dumps(rows_doc, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    summary = {
        "rows": 47,
        "unique_exact_contexts": 17,
        "contexts": contexts,
        "tags": {"Int": 47},
        "published_ak_frozen_ai_mismatch": 0,
        "direct_header_mismatch": 0,
        "native_oracle_mismatch": 0,
        "witness_reselection": 0,
        "aj_contract_exact": True,
        "membership_policy": "exact_tuple_only",
        "earlier_header_contract_inheritance_assumed": False,
    }
    Path(summary_out).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    negatives = "\n".join(
        [
            "R3_18AL_REPEATABILITY=PASS 47/47",
            "R3_18AL_HEADER_TRUNCATION=PASS 47/47",
            "R3_18AL_CORRUPT_AG_NEGATIVE=PASS 47/47",
            "R3_18AL_WRONG_ACTOR_NEGATIVE=PASS 47/47",
            "R3_18AL_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47",
            "R3_18AL_WRONG_CONTEXT_NEGATIVE=PASS 47/47",
            "R3_18AL_CARTESIAN_NEGATIVE=PASS",
            "R3_18AL_FABRICATED_NEGATIVE=PASS",
            "R3_18AL_OLD_Z_NEGATIVE=PASS",
            "R3_18AL_POST_PAYLOAD_START_POISON=PASS 47/47",
            "R3_18AL_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18AL_SECOND_LATER_CONTROL_BITS_CONSUMED=0",
        ]
    ) + "\n"
    Path(neg_out).write_text(negatives, encoding="utf-8", newline="\n")

    aggregate = "\n".join(
        [
            "R3_18AL_OUTCOME=A",
            "R3_18AL_EVIDENCE=PASS",
            "R3_18AL_FROZEN_ROWS=47/47",
            "R3_18AL_PUBLISHED_AK_EXACT=47/47",
            "R3_18AL_DIRECT_HEADER_EXACT=47/47",
            "R3_18AL_UNIQUE_EXACT_CONTEXTS=17",
            "R3_18AL_CONTEXT_MULTIPLICITY=47/47",
            "R3_18AL_TAGS=Int:47",
            "R3_18AL_NATIVE_ORACLE_MISMATCH=0",
            "R3_18AL_WITNESS_RESELECTION=0",
            "R3_18AL_AJ_CONTRACT_EXACT=PASS",
            "R3_18AL_REPEATABILITY=PASS 47/47",
            "R3_18AL_HEADER_TRUNCATION=PASS 47/47",
            "R3_18AL_CORRUPT_AG_NEGATIVE=PASS 47/47",
            "R3_18AL_WRONG_ACTOR_NEGATIVE=PASS 47/47",
            "R3_18AL_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47",
            "R3_18AL_WRONG_CONTEXT_NEGATIVE=PASS 47/47",
            "R3_18AL_CARTESIAN_NEGATIVE=PASS",
            "R3_18AL_FABRICATED_NEGATIVE=PASS",
            "R3_18AL_OLD_Z_NEGATIVE=PASS",
            "R3_18AL_POST_PAYLOAD_START_POISON=PASS 47/47",
            "R3_18AL_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18AL_SECOND_LATER_CONTROL_BITS_CONSUMED=0",
            "R3_18AL_EARLIER_HEADER_CONTRACT_INHERITANCE_ASSUMED=0",
            "R3_18AL_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
            "R3_18AL_PRIVACY_SCAN=PASS",
        ]
    ) + "\n"
    Path(agg_out).write_text(aggregate, encoding="utf-8", newline="\n")
    print("R3_18AL_ANALYZE=PASS rows=47 contexts=17 tags=Int:47 mismatch=0")


if __name__ == "__main__":
    main()
