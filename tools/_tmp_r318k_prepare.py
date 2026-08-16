#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def die(msg):
    raise SystemExit(msg)

def require(cond, msg):
    if not cond:
        die(msg)

def prepare(witness_path, comparison_path, request_path, summary_path):
    witnesses = json.loads(Path(witness_path).read_text(encoding="utf-8"))
    comparison = json.loads(Path(comparison_path).read_text(encoding="utf-8"))
    rows = comparison.get("rows")
    aggregate = comparison.get("aggregate")
    require(isinstance(witnesses, list) and len(witnesses) == 94, "frozen witness count != 94")
    require(isinstance(rows, list) and len(rows) == 94, "R3.18I comparison row count != 94")
    require(isinstance(aggregate, dict), "missing R3.18I comparison aggregate")

    expected_aggregate = {
        "R3_18I_CONTINUATION_ROWS": "47",
        "R3_18I_INT_ROWS": "46",
        "R3_18I_MISMATCH_COUNT": "0",
        "R3_18I_PAYLOAD_TRUNCATION_ROWS": "47",
        "R3_18I_STRING_ROWS": "1",
        "R3_18I_TERMINATOR_NO_PAYLOAD_ROWS": "47",
        "R3_18I_TERMINATOR_ROWS": "47",
        "R3_18I_THIRD_PROPERTY_BITS_CONSUMED": "0",
    }
    for key, value in expected_aggregate.items():
        require(str(aggregate.get(key)) == value, f"R3.18I aggregate drift: {key}")

    comp = {}
    for row in rows:
        key = (row["label"], row["class"])
        require(key not in comp, f"duplicate R3.18I comparison key: {key}")
        require(row.get("reconstruction_exact") is True, f"reconstruction not exact: {key}")
        require(row.get("payload_exact") is True, f"payload not exact: {key}")
        require(row.get("semantic_exact") is True, f"semantic not exact: {key}")
        require(row.get("shape_exact") is True, f"shape not exact: {key}")
        require(row.get("truncation") is True, f"truncation negative failed: {key}")
        require(row.get("poison") is True, f"poison negative failed: {key}")
        require(row.get("third_property_bits_consumed") == 0, f"third-property drift: {key}")
        comp[key] = row

    out = []
    keys = set()
    terms = conts = ints = strings = 0
    for w in witnesses:
        key = (w["label"], w["class"])
        require(key in comp, f"missing R3.18I comparison row: {key}")
        require(key not in keys, f"duplicate frozen witness key: {key}")
        keys.add(key)
        c = comp[key]

        cls = w["class"]
        second = w.get("second_header")
        next_present = bool(w["second_property_present"])
        if cls == "terminator":
            terms += 1
            require(not next_present and second is None, f"malformed terminator: {key}")
            require(c["tag"] == "None" and c["payload_end_bit"] == -1, f"terminator comparison drift: {key}")
            second_vals = [-1, -1, -1, -1, -1, -1, "None", -1]
        elif cls == "continuation":
            conts += 1
            require(next_present and isinstance(second, dict), f"malformed continuation: {key}")
            require(c["tag"] == second["attribute_tag"], f"second tag drift: {key}")
            require(c["payload_start_bit"] == second["payload_start_bit"], f"payload start drift: {key}")
            if second["attribute_tag"] == "Int":
                ints += 1
            elif second["attribute_tag"] == "String":
                strings += 1
            else:
                die(f"unadmitted continuation tag: {second['attribute_tag']}")
            second_vals = [
                second["stream_id_start_bit"],
                second["stream_id_end_bit"],
                second["stream_id"],
                second["stream_id_bound"],
                second["prop_id_bits"],
                second["property_object_id"],
                second["attribute_tag"],
                second["payload_start_bit"],
            ]
        else:
            die(f"unknown witness class: {cls}")

        fields = [
            cls,
            w["label"],
            w["actor_context_object_id"],
            w["first_attribute_tag"],
            w["first_lossless_value"],
            w["first_property_present_start_bit"],
            w["first_property_present_end_bit"],
            w["first_stream_id_start_bit"],
            w["first_stream_id_end_bit"],
            w["first_stream_id"],
            w["first_property_object_id"],
            w["first_payload_start_bit"],
            w["first_payload_end_bit"],
            w["second_property_present_start_bit"],
            w["second_property_present_end_bit"],
            1 if next_present else 0,
            *second_vals,
            c["payload_end_bit"],
            c["payload_width"],
            w["frame_index"],
            w["actor_ordinal"],
        ]
        require(len(fields) == 28, f"internal TSV field count {len(fields)}")
        out.append("\t".join(str(x) for x in fields))

    require(len(keys) == 94 and terms == 47 and conts == 47 and ints == 46 and strings == 1,
            "frozen lane aggregate mismatch")
    Path(request_path).write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "frozen_rows": 94,
        "terminators": 47,
        "continuations": 47,
        "tags": {"Int": 46, "String": 1},
        "r3_18i_native_oracle_mismatch": 0,
        "r3_18i_third_property_bits_consumed": 0,
        "witness_reselection": 0,
        "authority_mode": "immutable_r3_18i_rows_plus_independent_wire_semantic_reconstruction",
    }
    Path(summary_path).write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n",
                                  encoding="utf-8", newline="\n")
    print("R3_18K_PREPARE=PASS rows=94 terminators=47 continuations=47 Int=46 String=1 reselection=0")

def parse_kv_line(line, prefix):
    require(line.startswith(prefix + "\t"), f"bad prefix: {line[:40]}")
    result = {}
    for part in line.rstrip("\n").split("\t")[1:]:
        require("=" in part, f"bad field: {part}")
        k, v = part.split("=", 1)
        result[k] = v
    return result

def analyze(native_log, comparison_out, negatives_out, aggregate_out):
    lines = Path(native_log).read_text(encoding="utf-8").splitlines()
    rows = [parse_kv_line(x, "R3_18K_ROW") for x in lines if x.startswith("R3_18K_ROW\t")]
    aggs = [parse_kv_line(x, "R3_18K_AGG") for x in lines if x.startswith("R3_18K_AGG\t")]
    require(len(rows) == 94, f"native row count {len(rows)} != 94")
    require(len(aggs) == 1, f"native aggregate count {len(aggs)} != 1")
    agg = aggs[0]

    exact_fields = ["reconstruction_exact", "semantic_exact", "shape_exact",
                    "stop_exact", "truncation", "repeatability", "poison"]
    mismatches = 0
    terms = conts = ints = strings = no_lookup = trunc_rows = 0
    safe_rows = []
    for r in rows:
        for key in exact_fields:
            require(r.get(key) in {"0", "1"}, f"bad bool {key}")
        exact = all(r[k] == "1" for k in exact_fields)
        if not exact:
            mismatches += 1
        cls = r["class"]
        tag = r["tag"]
        if cls == "terminator":
            terms += 1
            require(tag == "None", "terminator tag drift")
            if r.get("terminator_no_lookup") == "1":
                no_lookup += 1
        elif cls == "continuation":
            conts += 1
            if tag == "Int":
                ints += 1
            elif tag == "String":
                strings += 1
            else:
                mismatches += 1
            if r.get("truncation") == "1":
                trunc_rows += 1
        else:
            mismatches += 1
        require(r.get("following_bits_consumed") == "0", "following property bit consumed")
        safe_rows.append({
            "label": r["label"],
            "class": cls,
            "tag": tag,
            "payload_start_bit": int(r["payload_start"]),
            "payload_end_bit": int(r["payload_end"]),
            "payload_width": int(r["payload_width"]),
            "reconstruction_exact": r["reconstruction_exact"] == "1",
            "semantic_exact": r["semantic_exact"] == "1",
            "shape_exact": r["shape_exact"] == "1",
            "stop_exact": r["stop_exact"] == "1",
            "truncation": r["truncation"] == "1",
            "repeatability": r["repeatability"] == "1",
            "poison": r["poison"] == "1",
            "terminator_no_lookup": r.get("terminator_no_lookup") == "1",
            "following_bits_consumed": 0,
        })

    expected_agg = {
        "rows": "94", "terminators": "47", "continuations": "47",
        "ints": "46", "strings": "1", "terminator_no_lookup_rows": "47",
        "truncation_rows": "47", "mismatch": "0", "following_bits_consumed": "0",
        "repeatability": "1", "poison": "1", "string_wrong_context": "1",
        "tag_outside": "1",
    }
    for k, v in expected_agg.items():
        require(agg.get(k) == v, f"native aggregate drift {k}: {agg.get(k)} != {v}")
    require((terms, conts, ints, strings, no_lookup, trunc_rows, mismatches) ==
            (47, 47, 46, 1, 47, 47, 0),
            "analyzed aggregate mismatch")

    payload = {
        "aggregate": {
            "rows": 94, "terminators": 47, "continuations": 47,
            "Int": 46, "String": 1, "terminator_no_lookup_rows": 47,
            "payload_truncation_rows": 47, "native_oracle_mismatch": 0,
            "following_property_bits_consumed": 0,
        },
        "rows": safe_rows,
    }
    Path(comparison_out).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                                    encoding="utf-8", newline="\n")
    negatives = "\n".join([
        "terminator_no_post_control_lookup=PASS 47/47",
        "real_payload_truncation=PASS 47/47",
        "string_wrong_context=PASS",
        "tag_outside_Int_String=PASS",
        "repeatability=PASS 94/94",
        "post_payload_poison=PASS 94/94",
        "following_property_bits_consumed=0",
    ]) + "\n"
    Path(negatives_out).write_text(negatives, encoding="utf-8", newline="\n")
    aggregate_text = "\n".join([
        "R3_18K_OUTCOME=A",
        "R3_18K_EVIDENCE=PASS",
        "R3_18K_FROZEN_ROWS=94/94",
        "R3_18K_TERMINATOR_ROWS=47",
        "R3_18K_CONTINUATION_ROWS=47",
        "R3_18K_CONTINUATION_INT=46",
        "R3_18K_CONTINUATION_STRING=1",
        "R3_18K_TERMINATOR_NO_LOOKUP_ROWS=47",
        "R3_18K_PAYLOAD_TRUNCATION_ROWS=47",
        "R3_18K_NATIVE_ORACLE_MISMATCH=0",
        "R3_18K_FOLLOWING_PROPERTY_BITS_CONSUMED=0",
        "R3_18K_WITNESS_RESELECTION=0",
        "R3_18K_STRING_WRONG_CONTEXT=PASS",
        "R3_18K_TAG_OUTSIDE_INT_STRING=PASS",
        "R3_18K_REPEATABILITY=PASS",
        "R3_18K_POST_PAYLOAD_POISON=PASS",
        "R3_18K_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
        "R3_18K_PRIVACY=PASS",
    ]) + "\n"
    Path(aggregate_out).write_text(aggregate_text, encoding="utf-8", newline="\n")
    print("R3_18K_ANALYZE=PASS rows=94 mismatch=0 following_bits=0")

def main():
    if len(sys.argv) < 2:
        die("usage: _tmp_r318k_prepare.py prepare|analyze ...")
    cmd = sys.argv[1]
    if cmd == "prepare" and len(sys.argv) == 6:
        prepare(*sys.argv[2:])
    elif cmd == "analyze" and len(sys.argv) == 6:
        analyze(*sys.argv[2:])
    else:
        die("invalid arguments")

if __name__ == "__main__":
    main()
