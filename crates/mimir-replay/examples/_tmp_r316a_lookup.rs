use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkLookupPlanReader,
};
use std::{env, fs};

fn clean(value: &str) -> String {
    value
        .replace('\t', "_")
        .replace('\r', "_")
        .replace('\n', "_")
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args().skip(1);
    let rel = args.next().ok_or("missing relative path")?;
    let actor_object_id: usize = args
        .next()
        .ok_or("missing actor object id")?
        .parse()?;
    let stream_id: u32 = args.next().ok_or("missing stream id")?.parse()?;
    if args.next().is_some() {
        return Err("too many arguments".into());
    }

    let bytes = fs::read(&rel)?;
    let input = ReplayInput::Memory {
        label: rel.clone(),
        bytes,
    };
    let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;
    let lookup = plan
        .object_lookups
        .get(actor_object_id)
        .and_then(|entry| entry.as_ref())
        .ok_or("missing actor lookup")?;
    let property = lookup
        .properties
        .iter()
        .find(|property| property.stream_id == stream_id)
        .ok_or("missing stream")?;
    let actor_name = plan
        .footer_lookup
        .objects
        .get(actor_object_id)
        .map(String::as_str)
        .ok_or("actor name oob")?;
    let property_name = plan
        .footer_lookup
        .objects
        .get(property.object_index as usize)
        .map(String::as_str)
        .ok_or("property name oob")?;

    println!(
        "R3_16A_MIMIR\tlabel={}\tactor_object_id={}\tactor_object_name={}\tstream_id={}\tmax_prop_id={}\tprop_id_bits={}\tproperty_object_id={}\tproperty_object_name={}\ttag={:?}",
        clean(&rel),
        actor_object_id,
        clean(actor_name),
        stream_id,
        lookup.max_prop_id,
        lookup.prop_id_bits,
        property.object_index,
        clean(property_name),
        property.tag,
    );
    Ok(())
}
