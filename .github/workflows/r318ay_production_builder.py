from pathlib import Path
import subprocess

MAIN='dae58bc2d27aef2daac02b626ae37dbd309706bc'; TREE='06f5cb02daa94be784e7ab31aac101493bc8e959'
SPEC='d636344a63854b25f2be89540cf3dbf672a28b5c'; LIBSHA='d7b18acd7ea832acc73e94921b994fa1b341e006'; AUTEST='5455121b2f0eafad09e031a66aa70178691c28fe'
LIB=Path('crates/mimir-replay/src/lib.rs'); AU=Path('crates/mimir-replay/tests/r3_18au_post_aq_following_header.rs'); TEST=Path('crates/mimir-replay/tests/r3_18ay_post_au_payload.rs'); SPECP=Path('docs/continuity/MIMIR_R3_18AY_EXECUTION_SPEC.md')
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
def req(x,m):
    if not x: raise SystemExit(m)
def blob(p): return git('hash-object',str(p))
req(git('rev-parse','HEAD')==MAIN,'AY HEAD drift'); req(git('rev-parse','HEAD^{tree}')==TREE,'AY tree drift')
req(blob(SPECP)==SPEC and blob(LIB)==LIBSHA and blob(AU)==AUTEST,'AY frozen blob drift')
req(not TEST.exists() and not git('status','--porcelain'),'AY dirty/preexisting target')
marker='// R3.18AU PRE-ADMISSION END bounded post-AQ mixed-continuation following header'
s=LIB.read_text(); req(s.count(marker)==1 and 'R3.18AY PRE-ADMISSION BEGIN' not in s,'AY insertion authority drift')
block=r'''

// R3.18AY PRE-ADMISSION BEGIN bounded post-AU one-following-payload
/// One validated R3.18AU true header plus exactly one R3.18AW-admitted signed Int/32 payload.
/// The AU result is recomputed from published prerequisites and false terminators fail closed
/// before payload decoding. `stop_bit` is payload end; the R3.18AX control bit is not consumed.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    pub header_composition: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    pub following_payload: ReplayNetworkPrimitiveScalarDecodeV1,
    pub stop_bit: u64,
}
fn network_existing_actor_post_au_following_payload_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!("replay network post-AU following-payload error: {category}: {}", detail.into()))
}
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
    an_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    aq_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    au_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1> {
    let expected_au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(network_bytes, prior, control, lookup_plan, context, an_prior, aq_prior)?;
    if expected_au != *au_prior { return Err(network_existing_actor_post_au_following_payload_error("invalid-r3-18au-prior", "supplied AU result differs from recomputed authority")); }
    let header = au_prior.following_header.as_ref().ok_or_else(|| network_existing_actor_post_au_following_payload_error("unadmitted-false-terminator", "AY excludes AU false terminators before payload decode"))?;
    if !header.property_present || au_prior.context != context { return Err(network_existing_actor_post_au_following_payload_error("invalid-au-header", "AY requires exact present AU header/context")); }
    let tag = header.resolved_attribute_tag.ok_or_else(|| network_existing_actor_post_au_following_payload_error("missing-resolved-attribute-tag", "AU header has no resolved tag"))?;
    if tag != ReplayNetworkAttributeTagV1::Int { return Err(network_existing_actor_post_au_following_payload_error("unsupported-payload-tag", format!("AY admits only Int, got {tag:?}"))); }
    let start = header.payload_start_bit.ok_or_else(|| network_existing_actor_post_au_following_payload_error("missing-payload-start", "AU header has no payload start"))?;
    if start != au_prior.stop_bit || start != header.stop_bit { return Err(network_existing_actor_post_au_following_payload_error("header-stop-mismatch", format!("start={start} AU_stop={} header_stop={}",au_prior.stop_bit,header.stop_bit))); }
    let payload = decode_replay_network_primitive_scalar_v1(network_bytes, start, tag)?;
    let end = start.checked_add(32).ok_or_else(|| network_existing_actor_post_au_following_payload_error("payload-end-overflow", "Int32 end overflow"))?;
    if payload.attribute_tag != ReplayNetworkAttributeTagV1::Int || payload.payload_start_bit != start || payload.payload_width != 32 || payload.payload_end_bit != end || payload.stop_bit != end || !matches!(&payload.value, ReplayNetworkPrimitiveScalarValueV1::Int(_)) {
        return Err(network_existing_actor_post_au_following_payload_error("int-boundary-mismatch", format!("start={} end={} width={} stop={} value={:?}",payload.payload_start_bit,payload.payload_end_bit,payload.payload_width,payload.stop_bit,payload.value)));
    }
    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 { header_composition: au_prior.clone(), following_payload: payload, stop_bit: end })
}
// R3.18AY PRE-ADMISSION END bounded post-AU one-following-payload
'''
LIB.write_text(s.replace(marker,marker+block,1))
TEST.write_text(r'''include!("r3_18au_post_aq_following_header.rs");
use mimir_replay::decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1 as decode_ay;

#[test]
fn r3_18ay_exact_aw_lane_and_hard_stop() {
    let (mut t,mut f,mut low)=(0usize,0usize,0usize);
    for (i,(path,first,actor,control_start)) in au_cases().into_iter().enumerate() {
        let (network,plan)=frozen_network_and_plan(path,&format!("r318ay_{i}"));
        let (prior,control,an)=aq_from_frozen(&network,&plan,first,actor); assert_eq!(an.stop_bit,control_start,"{path}");
        let aq=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(&network,&prior,&control,&plan,k3_context(),&an).unwrap();
        let au=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&prior,&control,&plan,k3_context(),&an,&aq).unwrap();
        if au.following_header.is_none() { f+=1; assert!(decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&au).is_err()); continue; }
        t+=1; let got=decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&au).unwrap(); let h=au.following_header.as_ref().unwrap(); let start=h.payload_start_bit.unwrap(); let end=start+32;
        let expected=if path.contains("079_1f838b01-66b5-4963-b62e-64f3d7dbd545") { low+=1; 5 } else { 300 };
        assert_eq!(got.header_composition,au,"{path}"); assert_eq!(got.following_payload.attribute_tag,ReplayNetworkAttributeTagV1::Int,"{path}"); assert_eq!((got.following_payload.payload_start_bit,got.following_payload.payload_end_bit,got.following_payload.payload_width,got.following_payload.stop_bit,got.stop_bit),(start,end,32,end,end),"{path}"); assert_eq!(got.following_payload.value,ReplayNetworkPrimitiveScalarValueV1::Int(expected),"{path}");
        let direct=decode_replay_network_primitive_scalar_v1(&network,start,ReplayNetworkAttributeTagV1::Int).unwrap(); assert_eq!(got.following_payload,direct,"{path}"); assert_eq!(decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&au).unwrap(),got,"{path}");
        let mut poisoned=network.clone(); let bit=usize::try_from(got.stop_bit).unwrap(); if bit<poisoned.len()*8 { let old=((poisoned[bit/8]>>(bit%8))&1)!=0; set_bit(&mut poisoned,bit,!old); assert_eq!(decode_ay(&poisoned,&prior,&control,&plan,k3_context(),&an,&aq,&au).unwrap(),got,"{path}"); }
    }
    assert_eq!((t,f,low),(40,7,1));
}

#[test]
fn r3_18ay_negative_authority_and_truncation_controls() {
    let (network,plan)=frozen_network_and_plan("../../external_fixtures/sample_001.replay","r318ay_neg"); let (prior,control,an)=aq_from_frozen(&network,&plan,10227,98);
    let aq=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(&network,&prior,&control,&plan,k3_context(),&an).unwrap();
    let au=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&prior,&control,&plan,k3_context(),&an,&aq).unwrap(); let base=decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&au).unwrap();
    let n=usize::try_from((base.stop_bit-1)/8).unwrap(); assert!(n*8>=usize::try_from(au.stop_bit).unwrap()); assert!(decode_ay(&network[..n],&prior,&control,&plan,k3_context(),&an,&aq,&au).is_err());
    let mut bad=au.clone(); bad.stop_bit+=1; assert!(decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&bad).is_err()); bad=au.clone(); bad.following_header.as_mut().unwrap().resolved_attribute_tag=Some(ReplayNetworkAttributeTagV1::Boolean); assert!(decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&bad).is_err()); bad=au.clone(); bad.following_header.as_mut().unwrap().payload_start_bit=Some(au.stop_bit+1); assert!(decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&bad).is_err()); bad=au.clone(); bad.following_header.as_mut().unwrap().stream_id_bound=Some(60); assert!(decode_ay(&network,&prior,&control,&plan,k3_context(),&an,&aq,&bad).is_err());
    let mut bad_an=an.clone(); bad_an.header_composition.following_header.actor_object_index=u32::MAX; assert!(decode_ay(&network,&prior,&control,&plan,k3_context(),&bad_an,&aq,&au).is_err());
    let mut bad_plan=plan.clone(); let h=au.following_header.as_ref().unwrap(); let ai=usize::try_from(h.actor_object_index).unwrap(); let sid=h.stream_id.unwrap(); if let Some(l)=bad_plan.object_lookups.get_mut(ai).and_then(Option::as_mut) { l.properties.retain(|p|p.stream_id!=sid); } assert!(decode_ay(&network,&prior,&control,&bad_plan,k3_context(),&an,&aq,&au).is_err());
    let mut ctx=k3_context(); ctx.version_minor-=1; assert!(decode_ay(&network,&prior,&control,&plan,ctx,&an,&aq,&au).is_err()); let mut ctx=k3_context(); ctx.is_rl_223=true; assert!(decode_ay(&network,&prior,&control,&plan,ctx,&an,&aq,&au).is_err());
}

#[test]
fn r3_18ay_source_scope_is_one_payload_and_no_later_control_loop() {
    let s=include_str!("../src/lib.rs"); let b=s.split_once("// R3.18AY PRE-ADMISSION BEGIN bounded post-AU one-following-payload").unwrap().1.split_once("// R3.18AY PRE-ADMISSION END bounded post-AU one-following-payload").unwrap().0;
    assert_eq!(b.matches("decode_replay_network_primitive_scalar_v1(").count(),1); assert_eq!(b.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(").count(),1);
    assert!(b.find("unadmitted-false-terminator").unwrap()<b.find("decode_replay_network_primitive_scalar_v1(").unwrap()); for x in ["NetworkBitCursor",".read_bit(","decode_replay_network_k2_v1(","loop {","while "] { assert_eq!(b.matches(x).count(),0,"forbidden AY token: {x}"); }
}
''')
req(set(git('diff','--name-only').splitlines())=={str(LIB),str(TEST)},'AY pre-format scope drift')
print('R3.18AY patch materialized')
