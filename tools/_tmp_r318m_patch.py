#!/usr/bin/env python3
from pathlib import Path

libp=Path('crates/mimir-replay/src/lib.rs')
testp=Path('crates/mimir-replay/tests/r3_18m_following_control.rs')
s=libp.read_text(encoding='utf-8')
marker='ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1'
if marker in s:
    raise SystemExit('R3.18M marker already exists')
append=r'''

/// Exactly one evidence-admitted `property_present` bit after a valid R3.18J second payload.
/// This is not a generic or repeatedly-chainable property cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1 {
    pub following_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_after_second_payload_following_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network after-second-payload following-control error: {category}: {}",
        detail.into()
    ))
}

/// Read exactly one R3.18L-admitted following control bit after a valid R3.18J result.
/// R3.18L observed only `true` (47/47); `false` therefore fails closed. No following
/// stream id, header, payload, extra control bit, or property loop is consumed.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1> {
    if !prior.header_composition.control.next_property_present {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "invalid-prior-control",
            "R3.18J prior does not contain a present second property",
        ));
    }
    let second_header = prior.header_composition.second_header.as_ref().ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "missing-second-header",
            "R3.18J prior is missing its second property header",
        )
    })?;
    let payload_start = second_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "missing-second-payload-start",
            "R3.18J second header has no payload start",
        )
    })?;
    if prior.header_composition.stop_bit != payload_start || second_header.stop_bit != payload_start {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "prior-header-stop-mismatch",
            "R3.18J header composition does not stop exactly at second payload start",
        ));
    }
    if second_header.property_present_start_bit
        != prior.header_composition.control.property_present_start_bit
        || second_header.property_present_end_bit
            != prior.header_composition.control.property_present_end_bit
        || prior.header_composition.control.stop_bit
            != prior.header_composition.control.property_present_end_bit
    {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "prior-control-header-mismatch",
            "R3.18J second control/header coordinates are inconsistent",
        ));
    }
    let second_payload = prior.second_payload.as_ref().ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "missing-second-payload",
            "R3.18J prior is missing its decoded second payload",
        )
    })?;
    let (decoded_start, decoded_end, expected_tag) = match second_payload {
        ReplayNetworkExistingActorSecondPropertyPayloadV1::Int(decoded) => {
            if decoded.stop_bit != decoded.payload_end_bit {
                return Err(network_existing_actor_after_second_payload_following_control_error(
                    "prior-int-stop-mismatch",
                    "R3.18J Int payload stop differs from payload end",
                ));
            }
            (decoded.payload_start_bit, decoded.payload_end_bit, ReplayNetworkAttributeTagV1::Int)
        }
        ReplayNetworkExistingActorSecondPropertyPayloadV1::String(decoded) => (
            decoded.payload_start_bit,
            decoded.payload_end_bit,
            ReplayNetworkAttributeTagV1::String,
        ),
    };
    if decoded_start != payload_start {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "prior-payload-start-mismatch",
            "R3.18J decoded payload start differs from second header payload start",
        ));
    }
    if second_header.resolved_attribute_tag != Some(expected_tag) {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "prior-payload-tag-mismatch",
            "R3.18J second header tag disagrees with decoded second payload",
        ));
    }
    if prior.stop_bit != decoded_end {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "prior-stop-mismatch",
            format!("R3.18J prior stop {} differs from second payload end {decoded_end}", prior.stop_bit),
        ));
    }

    let property_present_start_bit = prior.stop_bit;
    let property_present_end_bit = property_present_start_bit.checked_add(1).ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-position",
            "following property_present end bit overflows u64",
        )
    })?;
    let start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-position",
            "following property_present start does not fit usize",
        )
    })?;
    let end = usize::try_from(property_present_end_bit).map_err(|_| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-position",
            "following property_present end does not fit usize",
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if end > total_bits {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "insufficient-bits",
            format!("need one following control bit at {start}, network has {total_bits} bits"),
        ));
    }
    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let following_property_present = cursor.read_bit()?;
    let stop_bit = network_position_to_u64(cursor.position_bits())?;
    if stop_bit != property_present_end_bit {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "control-stop-mismatch",
            "one-bit following control did not stop at its exact end",
        ));
    }
    if !following_property_present {
        return Err(network_existing_actor_after_second_payload_following_control_error(
            "unadmitted-false-following-control",
            "R3.18L observed no false after-second-payload control witness",
        ));
    }
    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1 {
        following_property_present,
        property_present_start_bit,
        property_present_end_bit,
        stop_bit,
    })
}
'''
libp.write_text(s+append,encoding='utf-8',newline='\n')
testp.write_text(r'''use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
    ReplayNetworkExistingActorSecondPropertyPayloadV1, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn plan() -> ReplayNetworkLookupPlanV1 {
    let p=PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let bytes=std::fs::read(p).unwrap();
    MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&ReplayInput::Memory{label:"r318m".into(),bytes}).unwrap()
}
fn ctx()->ReplayNetworkK2DecodeContextV1 { ReplayNetworkK2DecodeContextV1{net_version:10,is_rl_223:false} }
fn bit(bytes:&mut Vec<u8>,p:usize,v:bool){ let n=p/8+1;if bytes.len()<n{bytes.resize(n,0)};if v{bytes[p/8]|=1<<(p%8)}else{bytes[p/8]&=!(1<<(p%8))}}
fn bits(bytes:&mut Vec<u8>,p:usize,w:usize,v:u64){for i in 0..w{bit(bytes,p+i,((v>>i)&1)!=0)}}
fn retag(p:&mut ReplayNetworkLookupPlanV1,t:ReplayNetworkAttributeTagV1){p.object_lookups[47].as_mut().unwrap().properties.iter_mut().find(|x|x.stream_id==30).unwrap().tag=t;}
fn int_packet(start:usize,following:bool,trail:usize)->Vec<u8>{let a=start+6;let e=a+32;let s=e+6;let mut b=vec![];bit(&mut b,start,true);bits(&mut b,start+1,5,30);bits(&mut b,a,32,62);bit(&mut b,e,true);bits(&mut b,e+1,5,30);bits(&mut b,s,32,0x12345678);let end=s+32;bit(&mut b,end,following);if trail>0{bit(&mut b,end+trail,false)}b}
fn string_packet(following:bool)->Vec<u8>{let start=0;let a=6;let e=a+32;let s=e+6;let mut b=vec![];bit(&mut b,start,true);bits(&mut b,1,5,30);bits(&mut b,a,32,62);bit(&mut b,e,true);bits(&mut b,e+1,5,30);bits(&mut b,s,32,7);let mut p=s+32;for c in b"ABCDEF"{bits(&mut b,p,8,u64::from(*c));p+=8}bits(&mut b,p,8,0x7f);p+=8;bit(&mut b,p,following);b}
fn prior_int(bytes:&[u8],start:usize,p:&ReplayNetworkLookupPlanV1)->ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1{let first=decode_replay_network_existing_actor_single_primitive_property_v1(bytes,start as u64,47,p).unwrap();decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(bytes,&first,p,ctx()).unwrap()}

#[test]
fn true_control_stops_exactly_one_bit_later_aligned_and_unaligned(){for start in [0usize,4,7]{let mut p=plan();retag(&mut p,ReplayNetworkAttributeTagV1::Int);let b=int_packet(start,true,12);let prior=prior_int(&b,start,&p);let got=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();assert!(got.following_property_present);assert_eq!(got.property_present_start_bit,prior.stop_bit);assert_eq!(got.property_present_end_bit,prior.stop_bit+1);assert_eq!(got.stop_bit,prior.stop_bit+1);}}
#[test]
fn repeatability_and_post_control_poison_are_invariant(){let mut p=plan();retag(&mut p,ReplayNetworkAttributeTagV1::Int);let b=int_packet(4,true,32);let prior=prior_int(&b,4,&p);let one=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();let two=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();assert_eq!(one,two);let mut poisoned=b.clone();for i in 0..16{bit(&mut poisoned,one.stop_bit as usize+i,i%2==0)}let got=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&poisoned,&prior).unwrap();assert_eq!(got,one);}
#[test]
fn false_control_is_evidence_unadmitted_and_rejected(){let mut p=plan();retag(&mut p,ReplayNetworkAttributeTagV1::Int);let b=int_packet(4,false,0);let prior=prior_int(&b,4,&p);let e=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap_err();assert!(e.to_string().contains("unadmitted-false-following-control"));}
#[test]
fn missing_bit_and_inconsistent_prior_fail_closed(){let mut p=plan();retag(&mut p,ReplayNetworkAttributeTagV1::Int);let full=int_packet(4,true,0);let prior=prior_int(&full,4,&p);assert_eq!(prior.stop_bit%8,0);let truncated=full[..(prior.stop_bit/8) as usize].to_vec();assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&truncated,&prior).is_err());let mut bad=prior.clone();bad.stop_bit+=1;let e=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&[],&bad).unwrap_err();assert!(e.to_string().contains("prior-stop-mismatch"));}
#[test]
fn missing_second_payload_or_header_rejects_before_read(){let mut p=plan();retag(&mut p,ReplayNetworkAttributeTagV1::Int);let b=int_packet(4,true,0);let prior=prior_int(&b,4,&p);let mut no_payload=prior.clone();no_payload.second_payload=None;assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&[],&no_payload).unwrap_err().to_string().contains("missing-second-payload"));let mut no_header=prior.clone();no_header.header_composition.second_header=None;assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&[],&no_header).unwrap_err().to_string().contains("missing-second-header"));}
#[test]
fn exact_context_string_prior_uses_same_true_only_control(){let mut p=plan();retag(&mut p,ReplayNetworkAttributeTagV1::Int);let b=string_packet(true);let first=decode_replay_network_existing_actor_single_primitive_property_v1(&b,0,47,&p).unwrap();retag(&mut p,ReplayNetworkAttributeTagV1::String);let prior=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(&b,&first,&p,ctx()).unwrap();assert!(matches!(&prior.second_payload,Some(ReplayNetworkExistingActorSecondPropertyPayloadV1::String(_))));let got=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();assert!(got.following_property_present);assert_eq!(got.stop_bit,prior.stop_bit+1);}
''',encoding='utf-8',newline='\n')
print('R3_18M_PATCH=PASS files=2')
