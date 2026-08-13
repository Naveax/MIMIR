from __future__ import annotations

import argparse
from pathlib import Path

PINNED_FRAME_DECODER_BLOB = "6f2ff153d3a27cdacccc65e3f23851489077a7d8"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one source match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("boxcars_root")
    args = parser.parse_args()

    root = Path(args.boxcars_root).resolve()
    source = root / "src" / "network" / "frame_decoder.rs"
    text = source.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "use fnv::FnvHashMap;\n\nuse crate::bits::RlBits;",
        "use fnv::FnvHashMap;\nuse std::fmt::Display;\nuse std::sync::atomic::{AtomicBool, Ordering};\n\nuse crate::bits::RlBits;",
        "instrumentation imports",
    )

    marker = "#[derive(Debug)]\npub(crate) struct RawSegmentedArray<T> {"
    helper = r'''static R3_14A_EVIDENCE_EMITTED: AtomicBool = AtomicBool::new(false);

fn r3_14a_offset(bits: &LittleEndianReader<'_>, total_bits: usize) -> usize {
    total_bits
        - bits
            .bits_remaining()
            .expect("R3.14A instrumentation requires a bounded bit reader")
}

fn r3_14a_optional<T: Display>(value: Option<T>) -> String {
    value
        .map(|value| value.to_string())
        .unwrap_or_else(|| "null".to_owned())
}

#[allow(clippy::too_many_arguments)]
fn r3_14a_emit(
    frame_start_bit: usize,
    time_raw_u32: u32,
    time_f32: f32,
    delta_raw_u32: u32,
    delta_f32: f32,
    bit_after_time_delta: usize,
    actor_present_offset: Option<usize>,
    actor_present: Option<bool>,
    actor_id_bound: Option<u32>,
    actor_id_start_bit: Option<usize>,
    actor_id_value: Option<i32>,
    actor_id_end_bit: Option<usize>,
    actor_id_bits_consumed: Option<usize>,
    actor_id_discriminator: Option<u64>,
    alive_bit_offset: Option<usize>,
    alive: Option<bool>,
    new_bit_offset: Option<usize>,
    is_new: Option<bool>,
    first_actor_header_end_bit: usize,
    terminal: bool,
) {
    let label = std::env::var("MIMIR_R3_14A_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\t', "_")
        .replace('\r', "_")
        .replace('\n', "_");

    println!(
        "R3_14A_EVIDENCE\tlabel={label}\tframe_start_bit={frame_start_bit}\ttime_raw_u32={time_raw_u32}\ttime_f32={time_f32:?}\tdelta_raw_u32={delta_raw_u32}\tdelta_f32={delta_f32:?}\tbit_after_time_delta={bit_after_time_delta}\tactor_present_bit_offset={}\tactor_present={}\tactor_id_bound={}\tactor_id_start_bit={}\tactor_id_value={}\tactor_id_end_bit={}\tactor_id_bits_consumed={}\tactor_id_discriminator={}\talive_bit_offset={}\talive={}\tnew_bit_offset={}\tnew={}\tfirst_actor_header_end_bit={first_actor_header_end_bit}\tterminal={terminal}",
        r3_14a_optional(actor_present_offset),
        r3_14a_optional(actor_present),
        r3_14a_optional(actor_id_bound),
        r3_14a_optional(actor_id_start_bit),
        r3_14a_optional(actor_id_value),
        r3_14a_optional(actor_id_end_bit),
        r3_14a_optional(actor_id_bits_consumed),
        r3_14a_optional(actor_id_discriminator),
        r3_14a_optional(alive_bit_offset),
        r3_14a_optional(alive),
        r3_14a_optional(new_bit_offset),
        r3_14a_optional(is_new),
    );
}

'''.replace(r'\"', '"')
    text = replace_once(text, marker, helper + marker, "instrumentation helper insertion")

    original_preamble = r'''        let time = bits
            .read_f32()
            .ok_or(FrameError::NotEnoughDataFor("Time"))?;

        if time < 0.0 || (time > 0.0 && time < 1e-10) {
            return Err(FrameError::TimeOutOfRange { time });
        }

        let delta = bits
            .read_f32()
            .ok_or(FrameError::NotEnoughDataFor("Delta"))?;

        if delta < 0.0 || (delta > 0.0 && delta < 1e-10) {
            return Err(FrameError::DeltaOutOfRange { delta });
        }

        if time == 0.0 && delta == 0.0 {
            return Ok(DecodedFrame::EndFrame);
        }

        while bits
            .read_bit()
            .ok_or(FrameError::NotEnoughDataFor("Actor data"))?
        {
'''.replace(r'\"', '"')
    instrumented_preamble = r'''        let r3_14a_observe = std::env::var_os("MIMIR_R3_14A_OBSERVE").is_some()
            && !R3_14A_EVIDENCE_EMITTED.load(Ordering::Relaxed);
        let r3_14a_total_bits = self.body.network_data.len() * 8;
        let r3_14a_frame_start_bit = if r3_14a_observe {
            r3_14a_offset(bits, r3_14a_total_bits)
        } else {
            0
        };

        let time = bits
            .read_f32()
            .ok_or(FrameError::NotEnoughDataFor("Time"))?;
        let r3_14a_time_raw_u32 = time.to_bits();

        if time < 0.0 || (time > 0.0 && time < 1e-10) {
            return Err(FrameError::TimeOutOfRange { time });
        }

        let delta = bits
            .read_f32()
            .ok_or(FrameError::NotEnoughDataFor("Delta"))?;
        let r3_14a_delta_raw_u32 = delta.to_bits();
        let r3_14a_bit_after_time_delta = if r3_14a_observe {
            r3_14a_offset(bits, r3_14a_total_bits)
        } else {
            0
        };

        if delta < 0.0 || (delta > 0.0 && delta < 1e-10) {
            return Err(FrameError::DeltaOutOfRange { delta });
        }

        if time == 0.0 && delta == 0.0 {
            if r3_14a_observe {
                r3_14a_emit(
                    r3_14a_frame_start_bit,
                    r3_14a_time_raw_u32,
                    time,
                    r3_14a_delta_raw_u32,
                    delta,
                    r3_14a_bit_after_time_delta,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    r3_14a_bit_after_time_delta,
                    true,
                );
                R3_14A_EVIDENCE_EMITTED.store(true, Ordering::Relaxed);
            }
            return Ok(DecodedFrame::EndFrame);
        }

        let mut r3_14a_actor_present_offset = 0usize;
        while {
            if r3_14a_observe {
                r3_14a_actor_present_offset = r3_14a_offset(bits, r3_14a_total_bits);
            }
            let actor_present = bits
                .read_bit()
                .ok_or(FrameError::NotEnoughDataFor("Actor data"))?;
            if r3_14a_observe && !actor_present {
                let actor_present_end = r3_14a_offset(bits, r3_14a_total_bits);
                r3_14a_emit(
                    r3_14a_frame_start_bit,
                    r3_14a_time_raw_u32,
                    time,
                    r3_14a_delta_raw_u32,
                    delta,
                    r3_14a_bit_after_time_delta,
                    Some(r3_14a_actor_present_offset),
                    Some(false),
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    actor_present_end,
                    false,
                );
                R3_14A_EVIDENCE_EMITTED.store(true, Ordering::Relaxed);
            }
            actor_present
        } {
'''.replace(r'\"', '"')
    text = replace_once(
        text,
        original_preamble,
        instrumented_preamble,
        "first-frame preamble instrumentation",
    )

    original_actor_header = r'''            let max = u64::from(self.max_channels);
            let actor_id_raw = bits.peek_bits_max_computed(self.channel_bits, max);
            let actor_id = ActorId(actor_id_raw as i32);

            // alive
            if bits.peek_and_consume(1) == 1 {
                // new
                if bits
                    .read_bit()
                    .ok_or(FrameError::NotEnoughDataFor("Is new actor"))?
                {
'''.replace(r'\"', '"')
    instrumented_actor_header = r'''            let max = u64::from(self.max_channels);
            let r3_14a_actor_id_start_bit = if r3_14a_observe {
                r3_14a_offset(bits, r3_14a_total_bits)
            } else {
                0
            };
            let actor_id_raw = bits.peek_bits_max_computed(self.channel_bits, max);
            let r3_14a_actor_id_end_bit = if r3_14a_observe {
                r3_14a_offset(bits, r3_14a_total_bits)
            } else {
                0
            };
            let actor_id = ActorId(actor_id_raw as i32);
            let r3_14a_actor_id_bits_consumed =
                r3_14a_actor_id_end_bit.saturating_sub(r3_14a_actor_id_start_bit);
            let r3_14a_actor_id_discriminator = if r3_14a_observe
                && r3_14a_actor_id_bits_consumed > self.channel_bits as usize
            {
                Some(u64::from(actor_id_raw >= (1u64 << self.channel_bits)))
            } else {
                None
            };

            // alive
            let r3_14a_alive_bit_offset = if r3_14a_observe {
                r3_14a_offset(bits, r3_14a_total_bits)
            } else {
                0
            };
            let alive = bits.peek_and_consume(1) == 1;
            let r3_14a_alive_end_bit = if r3_14a_observe {
                r3_14a_offset(bits, r3_14a_total_bits)
            } else {
                0
            };
            if alive {
                // new
                let r3_14a_new_bit_offset = if r3_14a_observe {
                    r3_14a_offset(bits, r3_14a_total_bits)
                } else {
                    0
                };
                let is_new = bits
                    .read_bit()
                    .ok_or(FrameError::NotEnoughDataFor("Is new actor"))?;
                let r3_14a_header_end_bit = if r3_14a_observe {
                    r3_14a_offset(bits, r3_14a_total_bits)
                } else {
                    0
                };
                if r3_14a_observe {
                    r3_14a_emit(
                        r3_14a_frame_start_bit,
                        r3_14a_time_raw_u32,
                        time,
                        r3_14a_delta_raw_u32,
                        delta,
                        r3_14a_bit_after_time_delta,
                        Some(r3_14a_actor_present_offset),
                        Some(true),
                        Some(self.max_channels),
                        Some(r3_14a_actor_id_start_bit),
                        Some(actor_id.0),
                        Some(r3_14a_actor_id_end_bit),
                        Some(r3_14a_actor_id_bits_consumed),
                        r3_14a_actor_id_discriminator,
                        Some(r3_14a_alive_bit_offset),
                        Some(true),
                        Some(r3_14a_new_bit_offset),
                        Some(is_new),
                        r3_14a_header_end_bit,
                        false,
                    );
                    R3_14A_EVIDENCE_EMITTED.store(true, Ordering::Relaxed);
                }
                if is_new {
'''.replace(r'\"', '"')
    text = replace_once(
        text,
        original_actor_header,
        instrumented_actor_header,
        "first actor header instrumentation",
    )

    original_deleted = r'''            } else {
                deleted_actors.push(actor_id);
                actors.delete(actor_id);
            }
'''
    instrumented_deleted = r'''            } else {
                if r3_14a_observe {
                    r3_14a_emit(
                        r3_14a_frame_start_bit,
                        r3_14a_time_raw_u32,
                        time,
                        r3_14a_delta_raw_u32,
                        delta,
                        r3_14a_bit_after_time_delta,
                        Some(r3_14a_actor_present_offset),
                        Some(true),
                        Some(self.max_channels),
                        Some(r3_14a_actor_id_start_bit),
                        Some(actor_id.0),
                        Some(r3_14a_actor_id_end_bit),
                        Some(r3_14a_actor_id_bits_consumed),
                        r3_14a_actor_id_discriminator,
                        Some(r3_14a_alive_bit_offset),
                        Some(false),
                        None,
                        None,
                        r3_14a_alive_end_bit,
                        false,
                    );
                    R3_14A_EVIDENCE_EMITTED.store(true, Ordering::Relaxed);
                }
                deleted_actors.push(actor_id);
                actors.delete(actor_id);
            }
'''.replace(r'\"', '"')
    text = replace_once(
        text,
        original_deleted,
        instrumented_deleted,
        "alive-false instrumentation",
    )

    source.write_text(text, encoding="utf-8")

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
    let _replay = ParserBuilder::new(&bytes)
        .must_parse_network_data()
        .parse()?;
    println!("R3_14A_ORACLE_PARSE=PASS");
    Ok(())
}
'''.replace(r'\"', '"')
    (example_dir / "r3_14a_probe.rs").write_text(example, encoding="utf-8")

    print(f"patched={source}")
    print(f"pinned_frame_decoder_blob={PINNED_FRAME_DECODER_BLOB}")


if __name__ == "__main__":
    main()
