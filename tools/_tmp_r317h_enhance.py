from pathlib import Path
import sys

root = Path(sys.argv[1])
frame = root / "src/network/frame_decoder.rs"
s = frame.read_text(encoding="utf-8")
marker = "#[derive(Debug)]\nenum DecodedFrame {"
if s.count(marker) != 1:
    raise SystemExit("R3.17H marker mismatch")
helper = r'''fn r3_17h_uid_semantic(uid: &UniqueId) -> String {
    match &uid.remote_id {
        RemoteId::Steam(value) => format!(
            "uid;system={};local={};kind=Steam;online={}",
            uid.system_id, uid.local_id, value
        ),
        RemoteId::PlayStation(value) => format!(
            "uid;system={};local={};kind=PlayStation;name_hex={};unknown_hex={};online={}",
            uid.system_id,
            uid.local_id,
            r3_17e_hex(value.name.as_bytes()),
            r3_17e_hex(&value.unknown1),
            value.online_id
        ),
        RemoteId::PsyNet(value) => format!(
            "uid;system={};local={};kind=PsyNet;online={};unknown_hex={}",
            uid.system_id,
            uid.local_id,
            value.online_id,
            r3_17e_hex(&value.unknown1)
        ),
        RemoteId::Epic(value) => format!(
            "uid;system={};local={};kind=Epic;account_hex={}",
            uid.system_id,
            uid.local_id,
            r3_17e_hex(value.as_bytes())
        ),
        RemoteId::SplitScreen(value) => format!(
            "uid;system={};local={};kind=SplitScreen;value={}",
            uid.system_id, uid.local_id, value
        ),
        RemoteId::Switch(value) => format!(
            "uid;system={};local={};kind=Switch;online={};unknown_hex={}",
            uid.system_id,
            uid.local_id,
            value.online_id,
            r3_17e_hex(&value.unknown1)
        ),
        RemoteId::Xbox(value) => format!(
            "uid;system={};local={};kind=Xbox;online={}",
            uid.system_id, uid.local_id, value
        ),
        RemoteId::QQ(value) => format!(
            "uid;system={};local={};kind=QQ;online={}",
            uid.system_id, uid.local_id, value
        ),
    }
}

fn r3_17h_semantic(tag: AttributeTag, attribute: &Attribute) -> Option<String> {
    match (tag, attribute) {
        (AttributeTag::ActiveActor, Attribute::ActiveActor(value)) => Some(format!(
            "active={};actor={}",
            u8::from(value.active), value.actor.0
        )),
        (AttributeTag::String, Attribute::String(value)) => {
            Some(format!("text_hex={}", r3_17e_hex(value.as_bytes())))
        }
        (AttributeTag::QWordString, Attribute::QWord(value)) => {
            Some(format!("qword={}", value))
        }
        (AttributeTag::QWordString, Attribute::String(value)) => {
            Some(format!("text_hex={}", r3_17e_hex(value.as_bytes())))
        }
        (AttributeTag::UniqueId, Attribute::UniqueId(value)) => {
            Some(r3_17h_uid_semantic(value.as_ref()))
        }
        (AttributeTag::PartyLeader, Attribute::PartyLeader(Some(value))) => {
            Some(format!("party;{}", r3_17h_uid_semantic(value.as_ref())))
        }
        (AttributeTag::PartyLeader, Attribute::PartyLeader(None)) => {
            Some("party;none".to_owned())
        }
        _ => None,
    }
}

'''
s = s.replace(marker, helper + marker, 1)
needle = "                            if let Some((tag_name, shape, decoded)) = r3_17e_decoded {\n                                println!(\n"
replacement = "                            if let Some((tag_name, shape, decoded)) = r3_17e_decoded {\n                                let r3_17h_semantic = r3_17h_semantic(attr.attribute, &attribute)\n                                    .expect(\"R3.17H candidate must have semantic normalization\");\n                                println!(\n"
if s.count(needle) != 1:
    raise SystemExit("R3.17H semantic insertion mismatch")
s = s.replace(needle, replacement, 1)
needle = "\\traw_bits_hex={}\\tdecoded={}\","
replacement = "\\traw_bits_hex={}\\tdecoded={}\\tsemantic={}\","
if s.count(needle) != 1:
    raise SystemExit("R3.17H format insertion mismatch")
s = s.replace(needle, replacement, 1)
needle = "                                    raw_hex,\n                                    r3_17e_clean(&decoded),\n                                );"
replacement = "                                    raw_hex,\n                                    r3_17e_clean(&decoded),\n                                    r3_17e_clean(&r3_17h_semantic),\n                                );"
if s.count(needle) != 1:
    raise SystemExit("R3.17H semantic argument mismatch")
s = s.replace(needle, replacement, 1)
frame.write_text(s, encoding="utf-8", newline="\n")
print("R3_17H_BOXCARS_SEMANTIC_ENHANCER=PASS")
