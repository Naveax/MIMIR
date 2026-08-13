use mimir_replay::{
    replay_network_parent_class_v1, MinimalReplayNetworkLookupPlanReader, ReplayInput,
    ReplayNetworkLookupPlanReader,
};
use std::error::Error;
use std::fs;
use std::path::PathBuf;

fn sanitize(value: &str) -> String {
    value.replace('\t', "_").replace('\r', "_").replace('\n', "_")
}

fn parent_chain(mut name: &str) -> String {
    let mut parts = Vec::new();
    for _ in 0..66 {
        let Some(parent) = replay_network_parent_class_v1(name) else {
            break;
        };
        parts.push(parent.to_string());
        name = parent;
    }
    parts.join(">")
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let relative_path = args
        .next()
        .ok_or("missing relative replay path")?
        .to_string_lossy()
        .into_owned();
    let replay_path = PathBuf::from(args.next().ok_or("missing replay path")?);
    let actor_object_id: u32 = args
        .next()
        .ok_or("missing actor object id")?
        .to_string_lossy()
        .parse()?;
    let stream_id: u32 = args
        .next()
        .ok_or("missing stream id")?
        .to_string_lossy()
        .parse()?;
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }

    let bytes = fs::read(&replay_path)?;
    let input = ReplayInput::Memory {
        label: relative_path.clone(),
        bytes,
    };
    let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;
    let actor_index = usize::try_from(actor_object_id)?;
    let actor_name = plan
        .footer_lookup
        .objects
        .get(actor_index)
        .ok_or("actor object id out of range")?;
    let lookup = plan
        .object_lookups
        .get(actor_index)
        .and_then(|value| value.as_ref())
        .ok_or("actor object lookup missing")?;
    let property = lookup
        .properties
        .iter()
        .find(|property| property.stream_id == stream_id)
        .ok_or("stream id unresolved")?;
    let property_name = plan
        .footer_lookup
        .objects
        .get(usize::try_from(property.object_index)?)
        .ok_or("property object id out of range")?;

    println!(
        "R3_16A_MIMIR\tlabel={}\tactor_object_id={}\tactor_object_name={}\tlookup_object_index={}\tmax_prop_id={}\tprop_id_bits={}\tstream_id={}\tproperty_object_id={}\tproperty_object_name={}\tattribute_tag={:?}\tparent_chain={}",
        sanitize(&relative_path),
        actor_object_id,
        sanitize(actor_name),
        lookup.object_index,
        lookup.max_prop_id,
        lookup.prop_id_bits,
        stream_id,
        property.object_index,
        sanitize(property_name),
        property.tag,
        sanitize(&parent_chain(actor_name)),
    );
    Ok(())
}
