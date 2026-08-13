from pathlib import Path
import argparse


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one source match, found {count}")
    return text.replace(old, new, 1)


def patch(root: Path) -> None:
    frame = root / "src/network/frame_decoder.rs"
    text = frame.read_text(encoding="utf-8")

    marker = "#[derive(Debug)]\nenum DecodedFrame {"
    static = r'''static R3_16A_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);

'''
    text = replace_once(text, marker, static + marker, "atomic marker")

    text = replace_once(
        text,
        '''        if time == 0.0 && delta == 0.0 {
            return Ok(DecodedFrame::EndFrame);
        }

        let mut r3_15a_actor_ordinal = 0usize;
''',
        '''        if time == 0.0 && delta == 0.0 {
            return Ok(DecodedFrame::EndFrame);
        }

        let r3_16a_time_raw_bits = time.to_bits();
        let r3_16a_delta_raw_bits = delta.to_bits();
        let total_bits = self.body.network_data.len() * 8;

        let mut r3_15a_actor_ordinal = 0usize;
''',
        "frame timing capture",
    )

    text = replace_once(
        text,
        '''                // new
                if bits
                    .read_bit()
                    .ok_or(FrameError::NotEnoughDataFor("Is new actor"))?
                {
''',
        '''                // new
                let r3_16a_is_new = bits
                    .read_bit()
                    .ok_or(FrameError::NotEnoughDataFor("Is new actor"))?;
                let r3_16a_new_bit_end = r3_15a_offset(bits, total_bits);
                if r3_16a_is_new {
''',
        "new bit capture",
    )

    original = r'''                    // While there are more attributes to update for our actor:
                    while bits
                        .read_bit()
                        .ok_or(FrameError::NotEnoughDataFor("Is prop present"))?
                    {
                        // We've previously calculated the max the stream id can be for a
                        // given type and how many bits that it encompasses so use those
                        // values now
                        bits.refill_lookahead();
                        if bits.lookahead_bits() < cache_info.prop_id_bits + 1 {
                            return Err(FrameError::NotEnoughDataFor("Prop id"));
                        }

                        let stream_id_raw = bits.peek_bits_max_computed(
                            cache_info.prop_id_bits,
                            u64::from(cache_info.max_prop_id),
                        );
                        let stream_id = StreamId(stream_id_raw as i32);

                        // Look the stream id up and find the corresponding attribute
                        // decoding function. Experience has told me replays that fail to
                        // parse, fail to do so here, so a large chunk is dedicated to
                        // generating an error message with context
                        let attr = cache_info.attributes.get(stream_id).ok_or(
                            FrameError::MissingAttribute {
                                actor: actor_id,
                                actor_object: *object_id,
                                attribute_stream: stream_id,
                            },
                        )?;

                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
                            |e| match e {
                                AttributeError::Unimplemented => FrameError::MissingAttribute {
                                    actor: actor_id,
                                    actor_object: *object_id,
                                    attribute_stream: stream_id,
                                },
                                e => FrameError::AttributeError {
                                    actor: actor_id,
                                    actor_object: *object_id,
                                    attribute_stream: stream_id,
                                    error: e,
                                },
                            },
                        )?;

                        updated_actors.push(UpdatedAttribute {
                            actor_id,
                            stream_id,
                            object_id: attr.object_id,
                            attribute,
                        });
                    }
'''
    instrumented = r'''                    // While there are more attributes to update for our actor:
                    loop {
                        let r3_16a_property_present_start_bit = r3_15a_offset(bits, total_bits);
                        let r3_16a_property_present = bits
                            .read_bit()
                            .ok_or(FrameEror::NotEnoughDataFor("Is prop present")))?;
                        let r3_16a_property_present_end_bit = r3_15a_offset(bits, total_bits);
                        if !r3_16a_property_present {
                            break;
                        }

                        // We've previously calculated the max the stream id can be for a
                        // given type and how many bits that it encompasses so use those
                        // values now
                        bits.refill_lookahead();
                        if bits.lookahead_bits() < cache_info.prop_id_bits + 1 {
                            return Err(FrameError::NotEnoughDataFor("Prop id"));
                        }

                        let r3_16a_stream_id_start_bit = r3_15a_offset(bits, total_bits);
                        let stream_id_raw = bits.peek_bits_max_computed(
                            cache_info.prop_id_bits,
                            u64::from(cache_info.max_prop_id),
                        );
                        let r3_16a_stream_id_end_bit = r3_15a_offset(bits, total_bits);
                        let stream_id = StreamId(stream_id_raw as i32);

                        // Look the stream id up and find the corresponding attribute
                        // decoding function. Experience has told me replays that fail to
                        // parse, fail to do so here, so a large chunk is dedicated to
                        // generating an error message with context
                        let attr = cache_info.attributes.get(stream_id).ok_or(
                            FrameError::MissingAttribute {
                                actor: actor_id,
                                actor_object: *object_id,
                                attribute_stream: stream_id,
                            },
                        )?;

                        let r3_16a_payload_start_bit = r3_15a_offset(bits, total_bits);
                        if R3_16A_EMITTED
                            .compare_exchange(
                                false,
                                true,
                                std::sync::atomic::Ordering::SeqCst,
                                std::sync::atomic::Ordering::SeqCst,
                            )
                            .is_ok()
                        {
                            let actor_object_index = usize::from(*object_id);
                            let property_object_index = usize::from(attr.object_id);
                            let actor_object_name = self
                                .body
                                .objects
                                .get(actor_object_index)
                                .map(String::as_str)
                                .unwrap_or("<out-of-range>")
                                .replace('\t', "_")
                                .replace('\r', "_")
                                .replace('\n', "_");
                            let property_object_name = self
                                .body
                                .objects
                                .get(property_object_index)
                                .map(String::as_str)
                                .unwrap_or("<out-of-range>")
                                .replace('\t', "_")
                                .replace('\r', "_")
                                .replace('\n', "_");
                            println!(
                                "R3_16A_PROPERTY\tlabel={}\tframe_index={}\tactor_ordinal={}\tframe_time_raw_bits={}\tframe_delta_raw_bits={}\tactor_id={}\tactor_context_object_id={}\tactor_context_object_name={}\tnew_bit_end={}\tproperty_present_start_bit={}\tproperty_present_end_bit={}\tproperty_present_value=true\tstream_id_start_bit={}\tstream_id_end_bit={}\tstream_id_value={}\tstream_id_bound={}\tprop_id_bits={}\tresolved_property_object_id={}\tresolved_property_object_name={}\tresolved_attribute_tag={:?}\tpayload_start_bit={}",
                                r3_15a_label(),
                                frame_index,
                                r3_15a_current_actor_ordinal,
                                r3_16a_time_raw_bits,
                                r3_16a_delta_raw_bits,
                                actor_id.0,
                                object_id.0,
                                actor_object_name,
                                r3_16a_new_bit_end,
                                r3_16a_property_present_start_bit,
                                r3_16a_property_present_end_bit,
                                r3_16a_stream_id_start_bit,
                                r3_16a_stream_id_end_bit,
                                stream_id.0,
                                cache_info.max_prop_id,
                                cache_info.prop_id_bits,
                                attr.object_id.0,
                                property_object_name,
                                attr.attribute,
                                r3_16a_payload_start_bit,
                            );
                        }

                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
                            |e| match e {
                                AttributeError::Unimplemented => FrameError::MissingAttribute {
                                    actor: actor_id,
                                    actor_object: *object_id,
                                    attribute_stream: stream_id,
                                },
                                e => FrameError::AttributeError {
                                    actor: actor_id,
                                    actor_object: *object_id,
                                    attribute_stream: stream_id,
                                    error: e,
                                },
                            },
                        )?;

                        updated_actors.push(UpdatedAttribute {
                            actor_id,
                            stream_id,
                            object_id: attr.object_id,
                            attribute,
                        });
                    }
'''
    text = replace_once(text, original, instrumented, "property loop instrumentation")
    frame.write_text(text, encoding="utf-8", newline="\n")

    example_dir = root / "examples"
    example_dir.mkdir(exist_ok=True)
    example = r'''use boxcars::ParserBuilder;
use std::error::Error;
use std::fs;
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let replay_path = PathBuf::from(args.next().ok_or("missing replay path")?);
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }
    let bytes = fs::read(&replay_path)?;
    let _replay = ParserBuilder::new(&bytes).must_parse_network_data().parse()?;
    Ok(())
}
'''
    (example_dir / "r3_16a_probe.rs").write_text(example, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    args = parser.parse_args()
    patch(Path(args.root).resolve())


if __name__ == "__main__":
    main()
