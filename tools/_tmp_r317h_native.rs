use mimir_replay::{
    ReplayNetworkAttributeTagV1, ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1,
    ReplayNetworkTextEncodingV1, ReplayNetworkTextV1, ReplayNetworkUniqueIdRemoteV1,
    ReplayNetworkUniqueIdV1, decode_replay_network_k2_v1,
};
use std::env;
use std::fs;

fn hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(bytes.len() * 2);
    for &b in bytes {
        out.push(HEX[(b >> 4) as usize] as char);
        out.push(HEX[(b & 0x0f) as usize] as char);
    }
    out
}

fn from_hex(value: &str) -> Result<Vec<u8>, String> {
    if value.len() % 2 != 0 {
        return Err("odd hex length".to_owned());
    }
    let mut out = Vec::with_capacity(value.len() / 2);
    let bytes = value.as_bytes();
    let nibble = |b: u8| -> Result<u8, String> {
        match b {
            b'0'..=b'9' => Ok(b - b'0'),
            b'a'..=b'f' => Ok(b - b'a' + 10),
            b'A'..=b'F' => Ok(b - b'A' + 10),
            _ => Err("invalid hex".to_owned()),
        }
    };
    for i in (0..bytes.len()).step_by(2) {
        out.push((nibble(bytes[i])? << 4) | nibble(bytes[i + 1])?);
    }
    Ok(out)
}

fn encoding_name(encoding: ReplayNetworkTextEncodingV1) -> &'static str {
    match encoding {
        ReplayNetworkTextEncodingV1::Empty => "Empty",
        ReplayNetworkTextEncodingV1::Windows1252 => "Windows1252",
        ReplayNetworkTextEncodingV1::Utf16Le => "UTF16",
    }
}

fn text_shape(prefix: &str, text: &ReplayNetworkTextV1) -> String {
    format!(
        "{}:{}:declared={}",
        prefix,
        encoding_name(text.encoding),
        text.declared_length
    )
}

fn uid_shape(prefix: &str, uid: &ReplayNetworkUniqueIdV1) -> String {
    match &uid.remote_id {
        ReplayNetworkUniqueIdRemoteV1::Steam { .. } => format!("{}:Steam", prefix),
        ReplayNetworkUniqueIdRemoteV1::PlayStation { .. } => format!("{}:PlayStation", prefix),
        ReplayNetworkUniqueIdRemoteV1::PsyNet { .. } => format!("{}:PsyNet", prefix),
        ReplayNetworkUniqueIdRemoteV1::Epic { account_id } => format!(
            "{}:Epic:{}:declared={}",
            prefix,
            encoding_name(account_id.encoding),
            account_id.declared_length
        ),
    }
}

fn uid_semantic(uid: &ReplayNetworkUniqueIdV1) -> String {
    match &uid.remote_id {
        ReplayNetworkUniqueIdRemoteV1::Steam { online_id } => format!(
            "uid;system={};local={};kind=Steam;online={}",
            uid.system_id, uid.local_id, online_id
        ),
        ReplayNetworkUniqueIdRemoteV1::PlayStation { name, unknown, online_id } => format!(
            "uid;system={};local={};kind=PlayStation;name_hex={};unknown_hex={};online={}",
            uid.system_id,
            uid.local_id,
            hex(name.as_bytes()),
            hex(unknown),
            online_id
        ),
        ReplayNetworkUniqueIdRemoteV1::PsyNet { online_id } => format!(
            "uid;system={};local={};kind=PsyNet;online={};unknown_hex=",
            uid.system_id, uid.local_id, online_id
        ),
        ReplayNetworkUniqueIdRemoteV1::Epic { account_id } => format!(
            "uid;system={};local={};kind=Epic;account_hex={}",
            uid.system_id,
            uid.local_id,
            hex(account_id.value.as_bytes())
        ),
    }
}

fn normalized(value: &ReplayNetworkK2ValueV1) -> (String, String) {
    match value {
        ReplayNetworkK2ValueV1::ActiveActor { active, actor } => (
            "ActiveActor33".to_owned(),
            format!("active={};actor={}", u8::from(*active), actor),
        ),
        ReplayNetworkK2ValueV1::String(text) => (
            text_shape("String", text),
            format!("text_hex={}", hex(text.value.as_bytes())),
        ),
        ReplayNetworkK2ValueV1::QWordStringQWord(value) => (
            "QWordString:QWord64".to_owned(),
            format!("qword={}", value),
        ),
        ReplayNetworkK2ValueV1::QWordStringText(text) => (
            text_shape("QWordString:String", text),
            format!("text_hex={}", hex(text.value.as_bytes())),
        ),
        ReplayNetworkK2ValueV1::UniqueId(uid) => (
            uid_shape("UniqueId", uid),
            uid_semantic(uid),
        ),
        ReplayNetworkK2ValueV1::PartyLeader(uid) => (
            uid_shape("PartyLeader:Some", uid),
            format!("party;{}", uid_semantic(uid)),
        ),
    }
}

fn tag(name: &str) -> Result<ReplayNetworkAttributeTagV1, String> {
    match name {
        "ActiveActor" => Ok(ReplayNetworkAttributeTagV1::ActiveActor),
        "String" => Ok(ReplayNetworkAttributeTagV1::String),
        "QWordString" => Ok(ReplayNetworkAttributeTagV1::QWordString),
        "UniqueId" => Ok(ReplayNetworkAttributeTagV1::UniqueId),
        "PartyLeader" => Ok(ReplayNetworkAttributeTagV1::PartyLeader),
        _ => Err(format!("unsupported tag {name}")),
    }
}

fn ctx(net_version: i32, is_rl_223: bool) -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 { net_version, is_rl_223 }
}

fn push_bits(bytes: &mut Vec<u8>, bit: &mut usize, value: u64, width: usize) {
    for offset in 0..width {
        let pos = *bit + offset;
        while bytes.len() <= pos / 8 {
            bytes.push(0);
        }
        if ((value >> offset) & 1) != 0 {
            bytes[pos / 8] |= 1 << (pos % 8);
        }
    }
    *bit += width;
}

fn push_u8(bytes: &mut Vec<u8>, bit: &mut usize, value: u8) {
    push_bits(bytes, bit, u64::from(value), 8);
}

fn push_i32(bytes: &mut Vec<u8>, bit: &mut usize, value: i32) {
    push_bits(bytes, bit, u64::from(value as u32), 32);
}

fn push_u16(bytes: &mut Vec<u8>, bit: &mut usize, value: u16) {
    push_bits(bytes, bit, u64::from(value), 16);
}

fn negative(name: &str, bytes: &[u8], tag: ReplayNetworkAttributeTagV1, context: ReplayNetworkK2DecodeContextV1) {
    match decode_replay_network_k2_v1(bytes, 0, tag, context) {
        Ok(_) => println!("NEG\t{}\tFAIL", name),
        Err(_) => println!("NEG\t{}\tPASS", name),
    }
}

fn run_negative_controls() {
    negative(
        "party_leader_none",
        &[0],
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    );

    let mut non_epic = Vec::new();
    let mut bit = 0usize;
    push_u8(&mut non_epic, &mut bit, 1);
    push_bits(&mut non_epic, &mut bit, 0x1122_3344_5566_7788, 64);
    push_u8(&mut non_epic, &mut bit, 1);
    negative(
        "party_leader_non_epic",
        &non_epic,
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    );

    let mut unadmitted = Vec::new();
    bit = 0;
    push_u8(&mut unadmitted, &mut bit, 4);
    push_bits(&mut unadmitted, &mut bit, 1, 64);
    push_u8(&mut unadmitted, &mut bit, 0);
    negative(
        "unique_id_unadmitted_system",
        &unadmitted,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    );

    let mut wrong_net = Vec::new();
    bit = 0;
    push_u8(&mut wrong_net, &mut bit, 1);
    push_bits(&mut wrong_net, &mut bit, 2, 64);
    push_u8(&mut wrong_net, &mut bit, 0);
    negative(
        "unique_id_wrong_net_version",
        &wrong_net,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(9, true),
    );

    let mut empty = Vec::new();
    bit = 0;
    push_i32(&mut empty, &mut bit, 0);
    negative(
        "qword_rl223_empty",
        &empty,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    );

    let mut utf16 = Vec::new();
    bit = 0;
    push_i32(&mut utf16, &mut bit, -2);
    push_u16(&mut utf16, &mut bit, 0x41);
    push_u16(&mut utf16, &mut bit, 0);
    negative(
        "qword_rl223_utf16",
        &utf16,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    );

    let mut epic_bad = Vec::new();
    bit = 0;
    push_u8(&mut epic_bad, &mut bit, 11);
    push_i32(&mut epic_bad, &mut bit, 2);
    push_u8(&mut epic_bad, &mut bit, b'X');
    push_u8(&mut epic_bad, &mut bit, 0);
    push_u8(&mut epic_bad, &mut bit, 0);
    negative(
        "epic_wrong_declared_length",
        &epic_bad,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    );
}

fn main() -> Result<(), String> {
    let path = env::args().nth(1).ok_or_else(|| "missing input path".to_owned())?;
    let text = fs::read_to_string(path).map_err(|e| e.to_string())?;
    for line in text.lines() {
        if line.is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split('\t').collect();
        if fields.len() != 7 {
            return Err(format!("bad input row field count {}", fields.len()));
        }
        let ordinal: usize = fields[0].parse().map_err(|_| "bad ordinal".to_owned())?;
        let tag_name = fields[1];
        let net_version: i32 = fields[2].parse().map_err(|_| "bad net version".to_owned())?;
        let rl223 = match fields[3] {
            "1" => true,
            "0" => false,
            _ => return Err("bad rl223 flag".to_owned()),
        };
        let expected_width: u64 = fields[4].parse().map_err(|_| "bad width".to_owned())?;
        let _expected_shape = fields[5];
        let bytes = from_hex(fields[6])?;
        match decode_replay_network_k2_v1(&bytes, 0, tag(tag_name)?, ctx(net_version, rl223)) {
            Ok(decoded) => {
                let (shape, semantic) = normalized(&decoded.value);
                println!(
                    "ROW\t{}\tOK\t{}\t{}\t{}\t{}\t{}",
                    ordinal,
                    decoded.payload_end_bit,
                    decoded.payload_width,
                    shape,
                    semantic,
                    tag_name
                );
                if decoded.payload_width != expected_width {
                    return Err(format!("row {ordinal} width drift"));
                }
            }
            Err(error) => {
                let clean = error.to_string().replace('\t', " ").replace('\n', " ");
                println!("ROW\t{}\tERR\t{}", ordinal, clean);
            }
        }
    }
    run_negative_controls();
    Ok(())
}
