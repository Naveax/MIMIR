use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_first_property_header_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::{env, fs, path::Path};

fn set_bit(bytes:&mut Vec<u8>, position:u64, value:bool)->Result<(),String>{
    let p=usize::try_from(position).map_err(|_|"bit position conversion")?; let need=p/8+1;
    if bytes.len()<need { bytes.resize(need,0); }
    if value { bytes[p/8]|=1<<(p%8); } else { bytes[p/8]&=!(1<<(p%8)); }
    Ok(())
}
fn k2()->ReplayNetworkK2DecodeContextV1{ ReplayNetworkK2DecodeContextV1{net_version:10,is_rl_223:false} }

fn main()->Result<(),Box<dyn std::error::Error>>{
    let request_path=env::args_os().nth(1).ok_or("missing target TSV")?;
    if env::args_os().nth(2).is_some(){return Err("unexpected extra argument".into());}
    let request=fs::read_to_string(request_path)?;
    let(mut rows,mut exact_n,mut direct_n,mut control_n,mut repeat_n,mut trunc_n,mut corrupt_n,mut wrong_actor_n,mut unresolved_n,mut wrong_ctx_n,mut poison_n)=(0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize);
    for line in request.lines().filter(|x|!x.trim().is_empty()){
        rows+=1; let f:Vec<&str>=line.split('\t').collect(); if f.len()!=18{return Err(format!("expected 18 fields got {}",f.len()).into());}
        let label=f[0]; let frame_index:usize=f[1].parse()?; let actor_ordinal:usize=f[2].parse()?; let actor_object:u32=f[3].parse()?; let first_start:u64=f[4].parse()?;
        let control_start:u64=f[5].parse()?; let control_end:u64=f[6].parse()?; let stream_start:u64=f[7].parse()?; let stream_end:u64=f[8].parse()?; let stream_id:u32=f[9].parse()?; let stream_bound:u32=f[10].parse()?; let prop_bits:u8=f[11].parse()?; let property_object:u32=f[12].parse()?; let tag=f[13]; let payload_start:u64=f[14].parse()?; let version_major=f[15].parse()?; let version_minor=f[16].parse()?; let net_version=f[17].parse()?;
        let replay_bytes=fs::read(Path::new(label))?; let input=ReplayInput::Memory{label:label.to_owned(),bytes:replay_bytes.clone()};
        let scaffold=MinimalReplayContentScaffoldReader.read_content_scaffold(&input)?; let ns=usize::try_from(scaffold.network_start)?; let ne=usize::try_from(scaffold.network_end)?; if ns>ne||ne>replay_bytes.len(){return Err(format!("{label}: invalid network slice").into());}
        let network=replay_bytes[ns..ne].to_vec(); let plan=MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;
        let first=decode_replay_network_existing_actor_single_primitive_property_v1(&network,first_start,actor_object,&plan)?;
        let second=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(&network,&first,&plan,k2())?;
        let context=ReplayNetworkK3DecodeContextV1{version_major,version_minor,net_version,is_rl_223:false};
        let t=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(&network,&second,&plan,context)?;
        let ad=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(&network,&t,&plan,context)?;
        if ad.stop_bit!=control_start{return Err(format!("{label}: AD stop drift {} expected {control_start}",ad.stop_bit).into());}
        let control=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(&network,&ad,context)?;
        if control.property_present_start_bit!=control_start||control.stop_bit!=control_end||!control.following_property_present{return Err(format!("{label}: AG control drift {control:?}").into());}
        let published=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&ad,&control,&plan,context)?;
        let h=&published.following_header; let resolved_tag=h.resolved_attribute_tag.ok_or("AK missing tag")?;
        let exact=published.control==control && h.property_present_start_bit==control_start && h.property_present_end_bit==control_end && h.stream_id_start_bit==Some(stream_start) && h.stream_id_end_bit==Some(stream_end) && h.stream_id==Some(stream_id) && h.stream_id_bound==Some(stream_bound) && h.prop_id_bits==Some(prop_bits) && h.resolved_property_object_index==Some(property_object) && format!("{resolved_tag:?}")==tag && h.payload_start_bit==Some(payload_start) && h.stop_bit==payload_start && published.stop_bit==payload_start;
        if !exact{return Err(format!("{label}: AK frozen-AI mismatch {published:?}").into());} exact_n+=1; control_n+=usize::from(published.control==control);
        let direct=decode_replay_network_existing_actor_first_property_header_v1(&network,control_start,actor_object,&plan)?; let direct_equal=direct==published.following_header; if !direct_equal{return Err(format!("{label}: direct differs").into());} direct_n+=1;
        let repeated=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&ad,&control,&plan,context)?; let repeat=repeated==published; repeat_n+=usize::from(repeat);
        let trunc_len=usize::try_from(control_start/8)?.min(network.len()); let trunc=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network[..trunc_len],&ad,&control,&plan,context).is_err(); trunc_n+=usize::from(trunc);
        let mut bad_control=control.clone(); bad_control.stop_bit+=1; let corrupt=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&ad,&bad_control,&plan,context).is_err(); corrupt_n+=usize::from(corrupt);
        let mut bad_ad=ad.clone(); bad_ad.header_composition.following_header.actor_object_index=u32::MAX; let wrong_actor=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&bad_ad,&control,&plan,context).is_err(); wrong_actor_n+=usize::from(wrong_actor);
        let mut missing=plan.clone(); let unresolved=if let Some(slot)=missing.object_lookups.get_mut(usize::try_from(actor_object)?){*slot=None; decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&ad,&control,&missing,context).is_err()}else{true}; unresolved_n+=usize::from(unresolved);
        let wrong_context=ReplayNetworkK3DecodeContextV1{version_major:868,version_minor:31,net_version:10,is_rl_223:false}; let wrong_ctx=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&ad,&control,&plan,wrong_context).is_err(); wrong_ctx_n+=usize::from(wrong_ctx);
        let mut poisoned=network.clone(); for off in 0..16u64{set_bit(&mut poisoned,payload_start+off,off%2==0).map_err(std::io::Error::other)?;} let after=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&poisoned,&ad,&control,&plan,context)?; let poison=after==published; poison_n+=usize::from(poison);
        println!("R3_18AL_PUBLISHED\tlabel={label}\tframe_index={frame_index}\tactor_ordinal={actor_ordinal}\tactor_context_object_id={actor_object}\tproperty_present_start_bit={}\tproperty_present_end_bit={}\tstream_id_start_bit={}\tstream_id_end_bit={}\tstream_id={}\tstream_id_bound={}\tprop_id_bits={}\tproperty_object_id={}\tattribute_tag={:?}\tversion_major={}\tversion_minor={}\tnet_version={}\tpayload_start_bit={}\tstop_bit={}\tpublished_exact={}\tdirect_equal={}\tcontrol_identity={}\trepeatability={}\ttruncation={}\tcorrupt_ag_negative={}\twrong_actor_negative={}\tunresolved_lookup_negative={}\twrong_version_negative={}\tpost_payload_poison={}\tfollowing_payload_bits_consumed=0\tanother_control_bits_consumed=0",h.property_present_start_bit,h.property_present_end_bit,h.stream_id_start_bit.ok_or("missing stream start")?,h.stream_id_end_bit.ok_or("missing stream end")?,h.stream_id.ok_or("missing stream id")?,h.stream_id_bound.ok_or("missing bound")?,h.prop_id_bits.ok_or("missing prop bits")?,h.resolved_property_object_index.ok_or("missing object")?,resolved_tag,context.version_major,context.version_minor,context.net_version,h.payload_start_bit.ok_or("missing payload start")?,published.stop_bit,u8::from(exact),u8::from(direct_equal),u8::from(published.control==control),u8::from(repeat),u8::from(trunc),u8::from(corrupt),u8::from(wrong_actor),u8::from(unresolved),u8::from(wrong_ctx),u8::from(poison));
    }
    if [rows,exact_n,direct_n,control_n,repeat_n,trunc_n,corrupt_n,wrong_actor_n,unresolved_n,wrong_ctx_n,poison_n].iter().any(|&x|x!=47){return Err(format!("aggregate failure rows={rows} exact={exact_n} direct={direct_n} control={control_n} repeat={repeat_n} trunc={trunc_n} corrupt={corrupt_n} wrong_actor={wrong_actor_n} unresolved={unresolved_n} wrong_ctx={wrong_ctx_n} poison={poison_n}").into());}
    println!("R3_18AL_PUBLISHED_AGG\trows=47\tpublished_exact=47\tdirect_equal=47\tcontrol_identity=47\trepeatability=47\ttruncation=47\tcorrupt_ag_negative=47\twrong_actor_negative=47\tunresolved_lookup_negative=47\twrong_version_negative=47\tpost_payload_poison=47\tfollowing_payload_bits_consumed=0\tanother_control_bits_consumed=0"); Ok(())
}
