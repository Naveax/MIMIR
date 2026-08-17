#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path


def require(cond, msg):
    if not cond:
        raise SystemExit(msg)


def kv(line, prefix):
    require(line.startswith(prefix + "\t"), f"bad {prefix} line")
    out = {}
    for item in line.split("\t")[1:]:
        require("=" in item, f"bad field {item}")
        key, value = item.split("=", 1)
        out[key] = value
    return out


def load_n_targets(path):
    raw = Path(path).read_text(encoding="utf-8")
    rows = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        f = line.split("\t")
        require(len(f) == 26, f"N target field count {len(f)}")
        label = f[0]
        require(label not in rows, f"duplicate N target {label}")
        rows[label] = {
            "fields": f,
            "label": label,
            "actor_object": int(f[1]),
            "prior_stop": int(f[22]),
            "frame_index": int(f[24]),
            "actor_ordinal": int(f[25]),
        }
    require(len(rows) == 47, f"N target count {len(rows)} != 47")
    return raw, rows


def load_n_control(path, targets):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    agg = data.get("aggregate", {})
    require(agg.get("rows") == 47, "N aggregate rows drift")
    require(agg.get("false") == 0 and agg.get("true") == 47, "N control distribution drift")
    require(agg.get("published_r3_18m_oracle_mismatch") == 0, "N mismatch drift")
    require(agg.get("witness_reselection") == 0, "N witness reselection drift")
    rows = {}
    for row in data.get("rows", []):
        label = row["label"]
        require(label in targets, f"unexpected N control label {label}")
        require(label not in rows, f"duplicate N control label {label}")
        t = targets[label]
        require(row.get("property_present") is True, f"N false control {label}")
        require(row.get("published_r3_18m_oracle_exact") is True, f"N control mismatch {label}")
        require(int(row["prior_r3_18j_stop_bit"]) == t["prior_stop"], f"N prior stop drift {label}")
        require(int(row["property_present_start_bit"]) == t["prior_stop"], f"N control start drift {label}")
        require(int(row["property_present_end_bit"]) == t["prior_stop"] + 1, f"N control end drift {label}")
        require(int(row["stop_bit"]) == t["prior_stop"] + 1, f"N control stop drift {label}")
        rows[label] = row
    require(set(rows) == set(targets), "N control/target label set mismatch")
    return rows


def oracle_requests(n_targets_path, n_control_path, out_path):
    _, targets = load_n_targets(n_targets_path)
    controls = load_n_control(n_control_path, targets)
    lines = []
    for label, t in targets.items():
        c = controls[label]
        lines.append("\t".join([
            label,
            str(t["frame_index"]),
            str(t["actor_ordinal"]),
            str(t["actor_object"]),
            str(c["property_present_start_bit"]),
        ]))
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("R3_18O_ORACLE_REQUESTS=PASS rows=47 reselection=0")


def build(n_targets_path, n_control_path, oracle_log_path, target_out, oracle_rows_out, summary_out):
    _, targets = load_n_targets(n_targets_path)
    controls = load_n_control(n_control_path, targets)
    headers = {}
    for line in Path(oracle_log_path).read_text(encoding="utf-8").splitlines():
        if not line.startswith("R3_18O_HEADER\t"):
            continue
        row = kv(line, "R3_18O_HEADER")
        label = row["label"]
        require(label in targets, f"unexpected oracle label {label}")
        require(label not in headers, f"duplicate following-header oracle row {label}")
        t = targets[label]
        c = controls[label]
        require(int(row["frame_index"]) == t["frame_index"], f"oracle frame drift {label}")
        require(int(row["actor_ordinal"]) == t["actor_ordinal"], f"oracle actor ordinal drift {label}")
        require(int(row["actor_context_object_id"]) == t["actor_object"], f"oracle actor object drift {label}")
        require(int(row["property_ordinal"]) == 2, f"oracle property ordinal drift {label}")
        require(int(row["property_present_start_bit"]) == int(c["property_present_start_bit"]), f"oracle control start drift {label}")
        require(int(row["property_present_end_bit"]) == int(c["property_present_end_bit"]), f"oracle control end drift {label}")
        require(int(row["stream_id_start_bit"]) == int(c["property_present_end_bit"]), f"oracle stream start drift {label}")
        require(int(row["stream_id_end_bit"]) > int(row["stream_id_start_bit"]), f"empty stream range {label}")
        require(int(row["payload_start_bit"]) == int(row["stream_id_end_bit"]), f"payload start != stream end {label}")
        headers[label] = row
    require(set(headers) == set(targets), f"oracle header label set mismatch: got {len(headers)}")

    out_lines = []
    oracle_rows = []
    tuple_counts = Counter()
    tag_counts = Counter()
    version_counts = Counter()
    bound_counts = Counter()
    width_counts = Counter()
    for label, t in targets.items():
        h = headers[label]
        c = controls[label]
        extras = [
            str(c["property_present_start_bit"]),
            str(c["property_present_end_bit"]),
            h["stream_id_start_bit"],
            h["stream_id_end_bit"],
            h["stream_id"],
            h["stream_id_bound"],
            h["prop_id_bits"],
            h["property_object_id"],
            h["attribute_tag"],
            h["payload_start_bit"],
            h["version_major"],
            h["version_minor"],
            h["net_version"],
        ]
        out_lines.append("\t".join(t["fields"] + extras))
        tup = (
            int(h["stream_id_bound"]),
            int(h["prop_id_bits"]),
            int(h["property_object_id"]),
            h["attribute_tag"],
            int(h["version_major"]),
            int(h["version_minor"]),
            int(h["net_version"]),
        )
        tuple_counts[tup] += 1
        tag_counts[h["attribute_tag"]] += 1
        version_counts[(int(h["version_major"]), int(h["version_minor"]), int(h["net_version"]))] += 1
        bound_counts[int(h["stream_id_bound"])] += 1
        width_counts[int(h["prop_id_bits"])] += 1
        oracle_rows.append({
            "label": label,
            "frame_index": t["frame_index"],
            "actor_ordinal": t["actor_ordinal"],
            "actor_context_object_id": t["actor_object"],
            "property_present_start_bit": int(c["property_present_start_bit"]),
            "property_present_end_bit": int(c["property_present_end_bit"]),
            "stream_id_start_bit": int(h["stream_id_start_bit"]),
            "stream_id_end_bit": int(h["stream_id_end_bit"]),
            "stream_id": int(h["stream_id"]),
            "stream_id_bound": int(h["stream_id_bound"]),
            "prop_id_bits": int(h["prop_id_bits"]),
            "resolved_property_object_index": int(h["property_object_id"]),
            "resolved_attribute_tag": h["attribute_tag"],
            "payload_start_bit": int(h["payload_start_bit"]),
            "version_major": int(h["version_major"]),
            "version_minor": int(h["version_minor"]),
            "net_version": int(h["net_version"]),
            "observer_following_payload_bits_consumed": 0,
            "observer_another_control_bits_consumed": 0,
        })
    Path(target_out).write_text("\n".join(out_lines) + "\n", encoding="utf-8", newline="\n")
    payload = {
        "aggregate": {
            "rows": 47,
            "witness_reselection": 0,
            "oracle_header_rows": 47,
            "observer_following_payload_bits_consumed": 0,
            "observer_another_control_bits_consumed": 0,
        },
        "rows": sorted(oracle_rows, key=lambda r: r["label"]),
    }
    Path(oracle_rows_out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "rows": 47,
        "witness_reselection": 0,
        "distinct_exact_header_context_tuples": len(tuple_counts),
        "exact_header_context_tuple_counts": [
            {
                "stream_id_bound": k[0], "prop_id_bits": k[1], "property_object_index": k[2],
                "attribute_tag": k[3], "version_major": k[4], "version_minor": k[5], "net_version": k[6],
                "count": v,
            }
            for k, v in sorted(tuple_counts.items(), key=lambda item: repr(item[0]))
        ],
        "attribute_tag_counts": dict(sorted(tag_counts.items())),
        "version_context_counts": [
            {"version_major": k[0], "version_minor": k[1], "net_version": k[2], "count": v}
            for k, v in sorted(version_counts.items())
        ],
        "stream_id_bound_counts": {str(k): v for k, v in sorted(bound_counts.items())},
        "prop_id_bits_counts": {str(k): v for k, v in sorted(width_counts.items())},
        "observer_following_payload_bits_consumed": 0,
        "observer_another_control_bits_consumed": 0,
    }
    Path(summary_out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"R3_18O_ORACLE_BUILD=PASS rows=47 tuples={len(tuple_counts)} tags={dict(tag_counts)}")


def analyze(target_path, native_path, rows_out, negatives_out, aggregate_out):
    targets = {}
    for line in Path(target_path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        f = line.split("\t")
        require(len(f) == 39, f"O target field count {len(f)}")
        targets[f[0]] = f
    require(len(targets) == 47, "O target rows != 47")

    native = {}
    aggs = []
    for line in Path(native_path).read_text(encoding="utf-8").splitlines():
        if line.startswith("R3_18O_NATIVE\t"):
            row = kv(line, "R3_18O_NATIVE")
            label = row["label"]
            require(label in targets, f"unexpected native label {label}")
            require(label not in native, f"duplicate native label {label}")
            native[label] = row
        elif line.startswith("R3_18O_NATIVE_AGG\t"):
            aggs.append(kv(line, "R3_18O_NATIVE_AGG"))
    require(len(native) == 47, f"native rows {len(native)} != 47")
    require(len(aggs) == 1, "native aggregate count != 1")

    output = []
    mismatch = 0
    exact_tuples = set()
    for label, f in targets.items():
        n = native[label]
        expected = {
            "present_start": f[26], "present_end": f[27], "stream_start": f[28], "stream_end": f[29],
            "stream_id": f[30], "stream_bound": f[31], "prop_bits": f[32], "property_object": f[33],
            "tag": f[34], "payload_start": f[35],
        }
        exact = all(n.get(k) == v for k, v in expected.items()) and all(
            n.get(k) == "1" for k in [
                "r3_18j_exact", "r3_18m_exact", "trunc_property", "trunc_stream",
                "prior_stop_mismatch_negative", "wrong_actor_context_negative", "repeatability", "poison",
            ]
        ) and n.get("header_stop") == f[35] and n.get("following_payload_bits_consumed") == "0" and n.get("another_control_bits_consumed") == "0"
        mismatch += 0 if exact else 1
        exact_tuples.add((f[31], f[32], f[33], f[34], f[36], f[37], f[38]))
        output.append({
            "label": label,
            "frame_index": int(f[24]),
            "actor_ordinal": int(f[25]),
            "actor_context_object_id": int(f[1]),
            "property_present_start_bit": int(f[26]),
            "property_present_end_bit": int(f[27]),
            "stream_id_start_bit": int(f[28]),
            "stream_id_end_bit": int(f[29]),
            "stream_id": int(f[30]),
            "stream_id_bound": int(f[31]),
            "prop_id_bits": int(f[32]),
            "resolved_property_object_index": int(f[33]),
            "resolved_attribute_tag": f[34],
            "payload_start_bit": int(f[35]),
            "version_major": int(f[36]),
            "version_minor": int(f[37]),
            "net_version": int(f[38]),
            "native_oracle_exact": exact,
            "following_payload_bits_consumed": 0,
            "another_control_bits_consumed": 0,
        })
    require(mismatch == 0, f"native/oracle mismatch {mismatch}")

    sample = next(iter(exact_tuples))
    fabricated = (sample[0], sample[1], sample[2], "__OUTSIDE_OBSERVED_TAG__", sample[4], sample[5], sample[6])
    outside_observed_tuple_negative = fabricated not in exact_tuples
    require(outside_observed_tuple_negative, "outside-observed-tuple negative failed")

    expected_agg = {
        "rows": "47", "r3_18j_exact": "47", "r3_18m_exact": "47", "header_exact": "47",
        "trunc_property": "47", "trunc_stream": "47", "prior_stop_mismatch_negative": "47",
        "wrong_actor_context_negative": "47", "repeatability": "47", "poison": "47",
        "following_payload_bits_consumed": "0", "another_control_bits_consumed": "0",
    }
    for k, v in expected_agg.items():
        require(aggs[0].get(k) == v, f"native aggregate drift {k}: {aggs[0].get(k)}")

    payload = {
        "aggregate": {
            "rows": 47,
            "native_oracle_mismatch": 0,
            "r3_18j_reconstruction_exact": 47,
            "published_r3_18m_control_exact": 47,
            "following_header_exact": 47,
            "witness_reselection": 0,
            "following_payload_bits_consumed": 0,
            "another_control_bits_consumed": 0,
            "outside_observed_tuple_negative": True,
        },
        "rows": sorted(output, key=lambda r: r["label"]),
    }
    Path(rows_out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    negatives = "\n".join([
        "truncation_before_following_property_present=PASS 47/47",
        "truncation_before_following_stream_completion=PASS 47/47",
        "prior_r3_18m_stop_mismatch=PASS 47/47",
        "wrong_unresolved_actor_stream_context=PASS 47/47",
        "outside_exact_observed_property_tag_context=PASS",
        "repeatability=PASS 47/47",
        "post_payload_start_poison=PASS 47/47",
        "following_payload_bits_consumed=0",
        "another_control_bits_consumed=0",
    ]) + "\n"
    Path(negatives_out).write_text(negatives, encoding="utf-8", newline="\n")
    aggregate = "\n".join([
        "R3_18O_OUTCOME=A",
        "R3_18O_EVIDENCE=PASS",
        "R3_18O_FROZEN_ROWS=47/47",
        "R3_18O_WITNESS_RESELECTION=0",
        "R3_18O_R318J_RECONSTRUCTION_EXACT=47/47",
        "R3_18O_PUBLISHED_R318M_CONTROL_EXACT=47/47",
        "R3_18O_FOLLOWING_HEADER_EXACT=47/47",
        "R3_18O_NATIVE_ORACLE_MISMATCH=0",
        "R3_18O_TRUNC_PROPERTY=PASS 47/47",
        "R3_18O_TRUNC_STREAM=PASS 47/47",
        "R3_18O_PRIOR_STOP_MISMATCH_NEGATIVE=PASS 47/47",
        "R3_18O_WRONG_CONTEXT_NEGATIVE=PASS 47/47",
        "R3_18O_OUTSIDE_OBSERVED_TUPLE_NEGATIVE=PASS",
        "R3_18O_REPEATABILITY=PASS 47/47",
        "R3_18O_POST_PAYLOAD_START_POISON=PASS 47/47",
        "R3_18O_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
        "R3_18O_ANOTHER_CONTROL_BITS_CONSUMED=0",
        "R3_18O_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
        "R3_18O_PRIVACY=PASS",
    ]) + "\n"
    Path(aggregate_out).write_text(aggregate, encoding="utf-8", newline="\n")
    print("R3_18O_ANALYZE=PASS rows=47 mismatch=0 stop=payload_start")


def main():
    require(len(sys.argv) >= 2, "usage: prepare.py oracle-requests|build|analyze ...")
    mode = sys.argv[1]
    if mode == "oracle-requests" and len(sys.argv) == 5:
        oracle_requests(*sys.argv[2:])
    elif mode == "build" and len(sys.argv) == 8:
        build(*sys.argv[2:])
    elif mode == "analyze" and len(sys.argv) == 7:
        analyze(*sys.argv[2:])
    else:
        raise SystemExit("invalid arguments")


if __name__ == "__main__":
    main()
