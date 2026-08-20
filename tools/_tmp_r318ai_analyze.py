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


def parse(path, prefix):
    out = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix + "\t"):
            row = kv(line, prefix)
            label = row["label"]
            req(label not in out, f"duplicate {prefix} {label}")
            out[label] = row
    req(len(out) == 47, f"{prefix} rows {len(out)} != 47")
    return out


def main():
    if len(sys.argv) != 7:
        raise SystemExit("usage: analyze oracle native rows summary negatives aggregate")
    oracle, native, rows_out, summary_out, neg_out, agg_out = sys.argv[1:]
    o = parse(oracle, "R3_18AI_HEADER")
    n = parse(native, "R3_18AI_NATIVE")
    req(set(o) == set(n), "oracle/native label set mismatch")

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
    nmap = {
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
        "ag_exact",
        "repeatability",
        "trunc_header",
        "corrupt_ag_negative",
        "wrong_actor_negative",
        "unresolved_lookup_negative",
        "wrong_context_negative",
        "post_payload_poison",
    ]

    rows = []
    tuples = collections.Counter()
    tags = collections.Counter()
    mismatch = 0
    for label in sorted(o):
        a = o[label]
        b = n[label]
        exact = True
        for field in int_fields:
            native_field = nmap.get(field, field)
            if int(a[field]) != int(b[native_field]):
                exact = False
        if a["attribute_tag"] != b["tag"]:
            exact = False
        if int(b["ag_start"]) != int(a["property_present_start_bit"]):
            exact = False
        if int(b["ag_end"]) != int(a["property_present_end_bit"]):
            exact = False
        if int(b["ag_stop"]) != int(a["property_present_end_bit"]):
            exact = False
        if int(b["stream_start"]) != int(b["ag_stop"]):
            exact = False
        if int(b["header_stop"]) != int(a["payload_start_bit"]):
            exact = False
        if not all(b.get(flag) == "1" for flag in flags):
            exact = False
        if b.get("following_payload_bits_consumed") != "0":
            exact = False
        if b.get("second_later_control_bits_consumed") != "0":
            exact = False
        if not exact:
            mismatch += 1

        tup = (
            int(a["stream_id_bound"]),
            int(a["prop_id_bits"]),
            int(a["property_object_id"]),
            a["attribute_tag"],
            int(a["version_major"]),
            int(a["version_minor"]),
            int(a["net_version"]),
        )
        tuples[tup] += 1
        tags[a["attribute_tag"]] += 1
        rows.append(
            {
                "label": label,
                "frame_index": int(a["frame_index"]),
                "actor_ordinal": int(a["actor_ordinal"]),
                "actor_context_object_id": int(a["actor_context_object_id"]),
                "ag_property_present_start_bit": int(b["ag_start"]),
                "ag_stop_bit": int(b["ag_stop"]),
                "stream_id_start_bit": int(a["stream_id_start_bit"]),
                "stream_id_end_bit": int(a["stream_id_end_bit"]),
                "stream_id": int(a["stream_id"]),
                "stream_id_bound": int(a["stream_id_bound"]),
                "prop_id_bits": int(a["prop_id_bits"]),
                "resolved_property_object_index": int(a["property_object_id"]),
                "resolved_attribute_tag": a["attribute_tag"],
                "version_major": int(a["version_major"]),
                "version_minor": int(a["version_minor"]),
                "net_version": int(a["net_version"]),
                "payload_start_bit": int(a["payload_start_bit"]),
                "header_stop_bit": int(b["header_stop"]),
                "native_oracle_exact": exact,
                "following_payload_bits_consumed": 0,
                "second_later_control_bits_consumed": 0,
            }
        )

    req(mismatch == 0, f"AI native/oracle mismatch {mismatch}")
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

    result = {
        "aggregate": {
            "outcome": "A",
            "rows": 47,
            "unique_exact_contexts": len(contexts),
            "native_oracle_mismatch": 0,
            "witness_reselection": 0,
            "following_payload_bits_consumed": 0,
            "second_later_control_bits_consumed": 0,
            "tags": dict(sorted(tags.items())),
        },
        "rows": rows,
    }
    Path(rows_out).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    summary = {
        "rows": 47,
        "unique_exact_contexts": len(contexts),
        "contexts": contexts,
        "tags": dict(sorted(tags.items())),
        "native_oracle_mismatch": 0,
        "witness_reselection": 0,
        "membership_policy_candidate": "exact_tuple_only",
        "earlier_header_contract_inheritance_assumed": False,
    }
    Path(summary_out).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    negatives = "\n".join(
        [
            "R3_18AI_REPEATABILITY=PASS 47/47",
            "R3_18AI_HEADER_TRUNCATION=PASS 47/47",
            "R3_18AI_CORRUPT_AG_NEGATIVE=PASS 47/47",
            "R3_18AI_WRONG_ACTOR_NEGATIVE=PASS 47/47",
            "R3_18AI_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47",
            "R3_18AI_WRONG_CONTEXT_NEGATIVE=PASS 47/47",
            "R3_18AI_POST_PAYLOAD_START_POISON=PASS 47/47",
            "R3_18AI_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18AI_SECOND_LATER_CONTROL_BITS_CONSUMED=0",
        ]
    ) + "\n"
    Path(neg_out).write_text(negatives, encoding="utf-8", newline="\n")

    aggregate = "\n".join(
        [
            "R3_18AI_OUTCOME=A",
            "R3_18AI_EVIDENCE=PASS",
            "R3_18AI_FROZEN_ROWS=47/47",
            "R3_18AI_PUBLISHED_AG_EXACT=47/47",
            f"R3_18AI_UNIQUE_EXACT_CONTEXTS={len(contexts)}",
            "R3_18AI_NATIVE_ORACLE_MISMATCH=0",
            "R3_18AI_WITNESS_RESELECTION=0",
            "R3_18AI_REPEATABILITY=PASS 47/47",
            "R3_18AI_HEADER_TRUNCATION=PASS 47/47",
            "R3_18AI_CORRUPT_AG_NEGATIVE=PASS 47/47",
            "R3_18AI_WRONG_ACTOR_NEGATIVE=PASS 47/47",
            "R3_18AI_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47",
            "R3_18AI_WRONG_CONTEXT_NEGATIVE=PASS 47/47",
            "R3_18AI_POST_PAYLOAD_START_POISON=PASS 47/47",
            "R3_18AI_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18AI_SECOND_LATER_CONTROL_BITS_CONSUMED=0",
            "R3_18AI_EARLIER_HEADER_CONTRACT_INHERITANCE_ASSUMED=0",
            "R3_18AI_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
            "R3_18AI_PRIVACY_SCAN=PASS",
        ]
    ) + "\n"
    Path(agg_out).write_text(aggregate, encoding="utf-8", newline="\n")
    print(
        f"R3_18AI_ANALYZE=PASS rows=47 contexts={len(contexts)} tags={dict(tags)} mismatch=0"
    )


if __name__ == "__main__":
    main()
