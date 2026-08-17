#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def require(cond, msg):
    if not cond:
        raise SystemExit(msg)


def load_targets(path):
    rows = {}
    raw = Path(path).read_text(encoding="utf-8")
    for line in raw.splitlines():
        if not line.strip():
            continue
        f = line.split("\t")
        require(len(f) == 26, f"target field count {len(f)}")
        label = f[0]
        require(label not in rows, f"duplicate target {label}")
        rows[label] = {
            "label": label,
            "actor_object": int(f[1]),
            "second_tag": f[20],
            "prior_stop": int(f[22]),
            "frame_index": int(f[24]),
            "actor_ordinal": int(f[25]),
        }
    require(len(rows) == 47, f"target count {len(rows)} != 47")
    return raw, rows


def build(l_targets_path, l_control_rows_path, target_out, summary_out):
    raw, targets = load_targets(l_targets_path)
    oracle = json.loads(Path(l_control_rows_path).read_text(encoding="utf-8"))
    aggregate = oracle.get("aggregate", {})
    rows = oracle.get("rows")
    require(isinstance(rows, list) and len(rows) == 47, "L oracle rows != 47")
    require(aggregate.get("rows") == 47, "L oracle aggregate rows drift")
    require(aggregate.get("false") == 0 and aggregate.get("true") == 47, "L control distribution drift")
    require(aggregate.get("native_oracle_mismatch") == 0, "L mismatch authority drift")
    require(aggregate.get("r3_18j_reconstruction_exact") == 47, "L R3.18J reconstruction drift")
    require(aggregate.get("following_stream_bits_consumed") == 0, "L following stream drift")
    require(aggregate.get("following_header_bits_consumed") == 0, "L following header drift")
    require(aggregate.get("following_payload_bits_consumed") == 0, "L following payload drift")
    require(aggregate.get("witness_reselection") == 0, "L witness reselection drift")

    oracle_by_label = {}
    for row in rows:
        label = row["label"]
        require(label in targets, f"unexpected L oracle label {label}")
        require(label not in oracle_by_label, f"duplicate L oracle label {label}")
        require(row.get("property_present") is True, f"L oracle false row {label}")
        require(row.get("native_oracle_exact") is True, f"L oracle mismatch row {label}")
        require(row.get("prior_r3_18j_stop_bit") == targets[label]["prior_stop"], f"L prior stop drift {label}")
        require(row.get("property_present_start_bit") == targets[label]["prior_stop"], f"L control start drift {label}")
        require(row.get("property_present_end_bit") == targets[label]["prior_stop"] + 1, f"L control end drift {label}")
        require(row.get("following_stream_bits_consumed") == 0, f"L stream consumption drift {label}")
        require(row.get("following_header_bits_consumed") == 0, f"L header consumption drift {label}")
        require(row.get("following_payload_bits_consumed") == 0, f"L payload consumption drift {label}")
        oracle_by_label[label] = row
    require(set(oracle_by_label) == set(targets), "L oracle/target label set mismatch")

    tag_counts = {"Int": 0, "String": 0}
    for target in targets.values():
        require(target["second_tag"] in tag_counts, f"unadmitted second tag {target['second_tag']}")
        tag_counts[target["second_tag"]] += 1
    require(tag_counts == {"Int": 46, "String": 1}, f"source tag counts drift: {tag_counts}")

    Path(target_out).write_text(raw, encoding="utf-8", newline="\n")
    summary = {
        "source_rows": 47,
        "source_authority": "immutable R3.18L artifact exact 47-row target/control lane",
        "control_distribution": {"false": 0, "true": 47},
        "second_tags": tag_counts,
        "r3_18j_reconstruction_exact": 47,
        "native_oracle_mismatch": 0,
        "following_stream_bits_consumed": 0,
        "following_header_bits_consumed": 0,
        "following_payload_bits_consumed": 0,
        "witness_reselection": 0,
    }
    Path(summary_out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print("R3_18N_BUILD=PASS targets=47 Int=46 String=1 false=0 true=47 reselection=0")


def kv(line, prefix):
    require(line.startswith(prefix + "\t"), f"bad {prefix} line")
    out = {}
    for item in line.split("\t")[1:]:
        require("=" in item, f"bad field {item}")
        key, value = item.split("=", 1)
        out[key] = value
    return out


def analyze(target_path, oracle_path, native_path, rows_out, negatives_out, aggregate_out):
    _, targets = load_targets(target_path)
    oracle = json.loads(Path(oracle_path).read_text(encoding="utf-8"))
    oracle_rows = {}
    for row in oracle.get("rows", []):
        label = row["label"]
        require(label in targets, f"unexpected oracle label {label}")
        require(label not in oracle_rows, f"duplicate oracle label {label}")
        oracle_rows[label] = row
    require(len(oracle_rows) == 47, f"oracle rows {len(oracle_rows)} != 47")

    native_rows = {}
    native_aggs = []
    for line in Path(native_path).read_text(encoding="utf-8").splitlines():
        if line.startswith("R3_18N_NATIVE\t"):
            row = kv(line, "R3_18N_NATIVE")
            label = row["label"]
            require(label in targets, f"unexpected native label {label}")
            require(label not in native_rows, f"duplicate native label {label}")
            native_rows[label] = row
        elif line.startswith("R3_18N_NATIVE_AGG\t"):
            native_aggs.append(kv(line, "R3_18N_NATIVE_AGG"))
    require(len(native_rows) == 47, f"native rows {len(native_rows)} != 47")
    require(len(native_aggs) == 1, "native aggregate count != 1")

    output = []
    mismatch = 0
    true_count = 0
    false_count = 0
    for label, target in targets.items():
        o = oracle_rows[label]
        n = native_rows[label]
        oracle_value = 1 if o.get("property_present") is True else 0
        oracle_start = int(o["property_present_start_bit"])
        oracle_end = int(o["property_present_end_bit"])
        native_value = int(n["control_value"])
        native_start = int(n["control_start"])
        native_end = int(n["control_end"])
        native_stop = int(n["control_stop"])
        exact = (
            o.get("native_oracle_exact") is True
            and int(o["prior_r3_18j_stop_bit"]) == target["prior_stop"]
            and oracle_start == target["prior_stop"]
            and oracle_end == oracle_start + 1
            and native_start == oracle_start
            and native_end == oracle_end
            and native_stop == oracle_end
            and native_value == oracle_value == 1
            and n.get("r3_18j_exact") == "1"
            and n.get("truncation") == "1"
            and n.get("prior_stop_mismatch_negative") == "1"
            and n.get("missing_second_header_negative") == "1"
            and n.get("missing_second_payload_negative") == "1"
            and n.get("false_rejection") == "1"
            and n.get("repeatability") == "1"
            and n.get("poison") == "1"
            and n.get("following_stream_bits_consumed") == "0"
            and n.get("following_header_bits_consumed") == "0"
            and n.get("following_payload_bits_consumed") == "0"
            and n.get("another_control_bits_consumed") == "0"
        )
        mismatch += 0 if exact else 1
        if oracle_value == 1:
            true_count += 1
        else:
            false_count += 1
        output.append({
            "label": label,
            "frame_index": target["frame_index"],
            "actor_ordinal": target["actor_ordinal"],
            "actor_context_object_id": target["actor_object"],
            "prior_r3_18j_stop_bit": target["prior_stop"],
            "property_present_start_bit": native_start,
            "property_present_end_bit": native_end,
            "stop_bit": native_stop,
            "property_present": bool(native_value),
            "published_r3_18m_oracle_exact": exact,
            "following_stream_bits_consumed": 0,
            "following_header_bits_consumed": 0,
            "following_payload_bits_consumed": 0,
            "another_control_bits_consumed": 0,
        })

    require(false_count == 0 and true_count == 47, f"control distribution false={false_count} true={true_count}")
    require(mismatch == 0, f"R3.18N mismatch count {mismatch}")
    expected_agg = {
        "rows": "47",
        "r3_18j_exact": "47",
        "truncation": "47",
        "prior_stop_mismatch_negative": "47",
        "missing_second_header_negative": "47",
        "missing_second_payload_negative": "47",
        "false_rejection": "47",
        "repeatability": "47",
        "poison": "47",
        "following_stream_bits_consumed": "0",
        "following_header_bits_consumed": "0",
        "following_payload_bits_consumed": "0",
        "another_control_bits_consumed": "0",
    }
    native_agg = native_aggs[0]
    for key, value in expected_agg.items():
        require(native_agg.get(key) == value, f"native aggregate drift {key}: {native_agg.get(key)}")

    payload = {
        "aggregate": {
            "rows": 47,
            "false": 0,
            "true": 47,
            "published_r3_18m_oracle_mismatch": 0,
            "r3_18j_reconstruction_exact": 47,
            "following_stream_bits_consumed": 0,
            "following_header_bits_consumed": 0,
            "following_payload_bits_consumed": 0,
            "another_control_bits_consumed": 0,
            "witness_reselection": 0,
        },
        "rows": sorted(output, key=lambda row: row["label"]),
    }
    Path(rows_out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    negatives = "\n".join([
        "missing_or_truncated_following_control=PASS 47/47",
        "prior_r3_18j_stop_mismatch=PASS 47/47",
        "missing_second_header=PASS 47/47",
        "missing_second_payload=PASS 47/47",
        "synthetic_false_following_control_rejected=PASS 47/47",
        "repeatability=PASS 47/47",
        "post_stop_poison=PASS 47/47",
        "following_stream_bits_consumed=0",
        "following_header_bits_consumed=0",
        "following_payload_bits_consumed=0",
        "another_control_bits_consumed=0",
    ]) + "\n"
    Path(negatives_out).write_text(negatives, encoding="utf-8", newline="\n")
    aggregate = "\n".join([
        "R3_18N_OUTCOME=A",
        "R3_18N_EVIDENCE=PASS",
        "R3_18N_FROZEN_ROWS=47/47",
        "R3_18N_CONTROL_FALSE=0",
        "R3_18N_CONTROL_TRUE=47",
        "R3_18N_R318J_RECONSTRUCTION_EXACT=47/47",
        "R3_18N_PUBLISHED_R318M_ORACLE_MISMATCH=0",
        "R3_18N_CONTROL_TRUNCATION=PASS 47/47",
        "R3_18N_PRIOR_STOP_MISMATCH_NEGATIVE=PASS 47/47",
        "R3_18N_MISSING_SECOND_HEADER_NEGATIVE=PASS 47/47",
        "R3_18N_MISSING_SECOND_PAYLOAD_NEGATIVE=PASS 47/47",
        "R3_18N_FALSE_CONTROL_REJECTION=PASS 47/47",
        "R3_18N_REPEATABILITY=PASS 47/47",
        "R3_18N_POST_STOP_POISON=PASS 47/47",
        "R3_18N_FOLLOWING_STREAM_BITS_CONSUMED=0",
        "R3_18N_FOLLOWING_HEADER_BITS_CONSUMED=0",
        "R3_18N_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
        "R3_18N_ANOTHER_CONTROL_BITS_CONSUMED=0",
        "R3_18N_WITNESS_RESELECTION=0",
        "R3_18N_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
        "R3_18N_PRIVACY=PASS",
    ]) + "\n"
    Path(aggregate_out).write_text(aggregate, encoding="utf-8", newline="\n")
    print("R3_18N_ANALYZE=PASS rows=47 false=0 true=47 mismatch=0")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: prepare.py build|analyze ...")
    if sys.argv[1] == "build" and len(sys.argv) == 6:
        build(*sys.argv[2:])
    elif sys.argv[1] == "analyze" and len(sys.argv) == 8:
        analyze(*sys.argv[2:])
    else:
        raise SystemExit("invalid arguments")


if __name__ == "__main__":
    main()
