use mimir_replay::{
    R3_17N_K4_ADMITTED_GROUPS_V1, ReplayNetworkAttributeTagV1, ReplayNetworkK4DecodeContextV1,
    decode_replay_network_k4_v1,
};
#[derive(Clone, Copy)]
struct Case {
    tag: ReplayNetworkAttributeTagV1,
    major: i32,
    minor: i32,
    net: i32,
    rl223: bool,
    width: u64,
    shape: &'static str,
    payload_hex: &'static str,
}
const CASES: &[Case] = &[
    Case {
        tag: ReplayNetworkAttributeTagV1::CamSettings,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 224,
        shape: "CamSettings:f32x7",
        payload_hex: "00000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::CamSettings,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 224,
        shape: "CamSettings:f32x7",
        payload_hex: "00000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::ClubColors,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 18,
        shape: "ClubColors:b1_u8_b1_u8",
        payload_hex: "000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishExtended,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 188,
        shape: "DemolishExtended:activex5:attacker_velocity:sb0:h5:cw2:victim_velocity:sb0:h5:cw2",
        payload_hex: "000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishExtended,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 217,
        shape: "DemolishExtended:activex5:attacker_velocity:sb0:h5:cw2:victim_velocity:sb10:h4:cw12",
        payload_hex: "00000000000000000000000000000000000000000000140000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishExtended,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 246,
        shape: "DemolishExtended:activex5:attacker_velocity:sb10:h4:cw12:victim_velocity:sb10:h4:cw12",
        payload_hex: "00000000000000000000000000000000000000008002000000800200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishExtended,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 243,
        shape: "DemolishExtended:activex5:attacker_velocity:sb10:h4:cw12:victim_velocity:sb9:h4:cw11",
        payload_hex: "00000000000000000000000000000000000000008002000000400200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishExtended,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 249,
        shape: "DemolishExtended:activex5:attacker_velocity:sb11:h4:cw13:victim_velocity:sb10:h4:cw12",
        payload_hex: "0000000000000000000000000000000000000000c00200000000140000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 150,
        shape: "DemolishFx:attack_velocity:sb0:h5:cw2:victim_velocity:sb10:h4:cw12",
        payload_hex: "00000000000000000000000000800200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 141,
        shape: "DemolishFx:attack_velocity:sb0:h5:cw2:victim_velocity:sb7:h4:cw9",
        payload_hex: "00000000000000000000000000c001000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 144,
        shape: "DemolishFx:attack_velocity:sb0:h5:cw2:victim_velocity:sb8:h4:cw10",
        payload_hex: "000000000000000000000000000002000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 147,
        shape: "DemolishFx:attack_velocity:sb0:h5:cw2:victim_velocity:sb9:h4:cw11",
        payload_hex: "00000000000000000000000000400200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 179,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb10:h4:cw12",
        payload_hex: "0000000000000000000000005000000000500000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 179,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb10:h4:cw12",
        payload_hex: "0000000000000000000000005000000000500000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 182,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb11:h4:cw13",
        payload_hex: "0000000000000000000000005000000000580000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 182,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb11:h4:cw13",
        payload_hex: "0000000000000000000000005000000000580000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 173,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb8:h4:cw10",
        payload_hex: "00000000000000000000000050000000004000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 173,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb8:h4:cw10",
        payload_hex: "00000000000000000000000050000000004000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 176,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb9:h4:cw11",
        payload_hex: "00000000000000000000000050000000004800000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 176,
        shape: "DemolishFx:attack_velocity:sb10:h4:cw12:victim_velocity:sb9:h4:cw11",
        payload_hex: "00000000000000000000000050000000004800000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 182,
        shape: "DemolishFx:attack_velocity:sb11:h4:cw13:victim_velocity:sb10:h4:cw12",
        payload_hex: "0000000000000000000000005800000000800200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 182,
        shape: "DemolishFx:attack_velocity:sb11:h4:cw13:victim_velocity:sb10:h4:cw12",
        payload_hex: "0000000000000000000000005800000000800200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 185,
        shape: "DemolishFx:attack_velocity:sb11:h4:cw13:victim_velocity:sb11:h4:cw13",
        payload_hex: "0000000000000000000000005800000000c0020000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 185,
        shape: "DemolishFx:attack_velocity:sb11:h4:cw13:victim_velocity:sb11:h4:cw13",
        payload_hex: "0000000000000000000000005800000000c0020000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 165,
        shape: "DemolishFx:attack_velocity:sb11:h4:cw13:victim_velocity:sb4:h5:cw6",
        payload_hex: "000000000000000000000000580000000000010000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 179,
        shape: "DemolishFx:attack_velocity:sb11:h4:cw13:victim_velocity:sb9:h4:cw11",
        payload_hex: "0000000000000000000000005800000000400200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 179,
        shape: "DemolishFx:attack_velocity:sb11:h4:cw13:victim_velocity:sb9:h4:cw11",
        payload_hex: "0000000000000000000000005800000000400200000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::ExtendedExplosion,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 112,
        shape: "ExtendedExplosion:location:sb12:h4:cw14",
        payload_hex: "0000000018000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::ExtendedExplosion,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 112,
        shape: "ExtendedExplosion:location:sb12:h4:cw14",
        payload_hex: "0000000018000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 726,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000000000000000070000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 726,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000000000000000070000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1080,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_14);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_14);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000410000000700000000000000000000000000000000000000000000000e000000000000000000000000000000000081000000000000000000000102000000000000000208000000080030000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1112,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_16);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_16);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000000001020000000000000000000002040000000000000004100000008000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000810000000000000000000001020000000000000002080000000000400000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1176,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_20);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_20);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000410000000a00000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000081000000000000000000000102000000000000000208000000000050000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1192,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000410000000a8000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000008100000000000000000000010200000000000000020800000004005000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1208,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1224,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_23);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_23);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000410000000b80000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000810000000000000000000001020000000000000002080000000c0050000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1320,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_29);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_29);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000410000000e80000000000000000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000081000000000000000000000102000000000000000208000000040070000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1352,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000000102000000000000000000000204000000000000000410000000f800000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000810000000000000000000001020000000000000002080000000c00700000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 854,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000000000000000000000000000001000000000000000001020000000000000000000002040000000000000000000000000000700000000000000000000000000000000400000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1320,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000a8000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000008000000000000000008100000000000000000000010200000000000000020800000004005000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1320,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000a8000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000008000000000000000008100000000000000000000010200000000000000020800000004005000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1336,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000800000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1336,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000800000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1128,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_9);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_9);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000000010000000000000000010200000000000000000000020400000000000000041000000048000000000000000000000000000000000000e000000000000000000000000000000008000000000000000008100000000000000000000010200000000000000020800000004002000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000000100000000000000000200000000000000000200000000000000000000020400000000000000000000000000007000000000000000000000000000000004000000000000000008000000000000000008000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1336,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_14);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_14);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000000000000000000000000000001000000000000000002000000000000000002000000000000000000000204000000000000000410000000700000000000000000000000000000000000000000000000e00000000000000000000000000000000800000000000000001000000000000000001000000000000000000000102000000000000000208000000080030000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1400,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_26);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_26);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000410000000d00000000000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000008000000000000000000081000000000000000000000102000000000000000208000000080060000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1448,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_29);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_29);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000410000000e80000000000000000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000008000000000000000000081000000000000000000000102000000000000000208000000040070000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1480,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000410000000f800000000000000000000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000080000000000000000000810000000000000000000001020000000000000002080000000c00700000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1304,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_12);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_12);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000000000000000000000000010000000000000000010000000000000000010200000000000000000000020400000000000000041000000060000000000000000000000000000000000000000000e0000000000000000000000000000008000000000000000008000000000000000008100000000000000000000010200000000000000020800000000003000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1110,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000000000000000000000000001000000000000000001000000000000000002000000000000000002000000000000000000000204000000000000000000000000000070000000000000000000000000000004000000000000000004000000000000000008000000000000000008000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 854,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000001000000000000000000000000000000000000000001020000000000000000000002040000000000000000000000000000700000000400000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1224,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_15);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_15);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000010000000000000000000000000000000000000000010200000000000000000000020400000000000000041000000078000000000000000000000000000000000000000000000000e00000000800000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000c003000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1288,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_19);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_19);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000001000000000000000000000000000000000000000001020000000000000000000002040000000000000004100000009800000000000000000000000000000000000000000000000000000000e00000000800000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000c00400000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1480,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000100000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000f800000000000000000000000000000000000000000000000000000000000000000000000000000000e00000000800000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000c00700000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1448,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000001000000000000000000000000000000000000000002000000000000000002000000000000000000000204000000000000000410000000a8000000000000000000000000000000000000000000000000000000000000e0000000080000000000000000000000000000000000000000100000000000000000100000000000000000000010200000000000000020800000004005000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000000100000000000000000000000000000000000000010000000000000000010200000000000000000000020400000000000000000000000000007000000004000000000000000000000000000000000000000400000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1480,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_23);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_23);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000001000000000000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000410000000b80000000000000000000000000000000000000000000000000000000000000000e000000008000000000000000000000000000000000000080000000000000000000810000000000000000000001020000000000000002080000000c0050000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1110,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000000010000000000000000000000000000000000000100000000000000000100000000000000000102000000000000000000000204000000000000000000000000000070000000040000000000000000000000000000000000000400000000000000000400000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1144,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_10);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_10);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000100000000000000000000000000000000000000000001020000000000000000000002040000000000000004100000005000000000000000000000000000000000000000e00000080000000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000800200000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1272,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_18);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_18);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000001000000000000000000000000000000000000000000010200000000000000000000020400000000000000041000000090000000000000000000000000000000000000000000000000000000e000000800000000000000000000000000000000000000000008100000000000000000000010200000000000000020800000008004000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000010000000000000000000000000000000000000000000208000000000000000200000000000000000000020400000000000000000000000000007000000400000000000000000000000000000000000000000008200000000000000008000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000010000000000000000000000000000000000000000010000000000000000010200000000000000000000020400000000000000000000000000007000000400000000000000000000000000000000000000000400000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1352,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_11);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_11);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000100000000000000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000580000000000000000000000000000000000000000e0000008000000000000000008000000000000000000000000000000000000000800000000000000000810000000000000000000001020000000000000002080000000c0020000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1336,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_14);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_14);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000100000000000000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000700000000000000000000000000000000000000000000000e00000080000000000000000000000000000000000000000080000000000000000081000000000000000000000102000000000000000208000000080030000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1544,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_27);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_27);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00000100000000000000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000d8000000000000000000000000000000000000000000000000000000000000000000000000e000000800000000000000000000000000000000000000000800000000000000000810000000000000000000001020000000000000002080000000c006000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000010000000000000000000000000000000000000001000000000000000000010200000000000000000000020400000000000000000000000000007000000400000000000000000000000000000000000000040000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1320,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_13);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_13);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000001000000000000000000000000000000000000000100000000000000000001020000000000000000000002040000000000000004100000006800000000000000000000000000000000000000000000e000000800000000000000000000000000000000000000080000000000000000000810000000000000000000001020000000000000002080000000400300000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000010000000000000000010000000000000000000000000000000000000000010200000000000000000000020400000000000000000000000000007000000400000000000000000400000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0000010000000000000000010000000000000000000000000000000000000000010200000000000000000000020400000000000000000000000000007000000400000000000000000400000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1608,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_23);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_23);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000001000000000000000001000000000000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000410000000b80000000000000000000000000000000000000000000000000000000000000000e0000008000000000000000008000000000000000000000000000000000000080000000000000000000810000000000000000000001020000000000000002080000000c0050000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 854,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:1(Paint:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:1(Paint:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00010000000000000000000000000000000000000000000001020000000000000000000002040000000000000000000000000000700004000000000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1464,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:1(Paint:new31);g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:1(Paint:new31);g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00010000000000000000000100000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e000080000000000000000000800000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1238,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:1(Paint:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:1(Paint:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c00010000000000000000010000000000000000000000000000000000000000010000000000000000020000000000000000020000000000000000000002040000000000000000000000000000700004000000000000000004000000000000000000000000000000000000000004000000000000000008000000000000000008000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1576,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:1(TeamEdition:new31);g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:1(TeamEdition:new31);g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_21);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000108000000000000000001000000000000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000410000000a8000000000000000000000000000000000000000000000000000000000000e00008400000000000000000080000000000000000000000000000000000000800000000000000000008100000000000000000000010200000000000000020800000004005000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0001080000000000000001000000000000000000000000000000000000000000010200000000000000000000020400000000000000000000000000007000042000000000000000040000000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1592,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000108000000000000000100000000000000000100000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e0000840000000000000000800000000000000000800000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1592,
        shape: "LoadoutsOnline:blue:outer28[g0:0();g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c000108000000000000000100000000000000000100000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e0000840000000000000000800000000000000000800000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 854,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c01000000000000000000000000000000000000000000000001020000000000000000000002040000000000000000000000000000700400000000000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 854,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c01000000000000000000000000000000000000000000000001020000000000000000000002040000000000000000000000000000700400000000000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 918,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000000000000000000000000000000000010200000000000000000000020400000000000000000000000000007004000000000000000000000400000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1400,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e008000000000000000000000000000000000000000000080000000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1128,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_9);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_9);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000000000000000000000000000000000010200000000000000000000020400000000000000041000000048000000000000000000000000000000000000e008000000000000000000000000000000000000000000000008100000000000000000000010200000000000000020800000004002000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000000000000000000000000000000010000000000000000010200000000000000000000020400000000000000000000000000007004000000000000000000000000000000000000000000000400000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1608,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c01000000000000000000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000f800000000000000000000000000000000000000000000000000000000000000000000000000000000e008000000000000000000000000000000000000000000000800000000000000000810000000000000000000001020000000000000002080000000c00700000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000000000000000000000000000001000000000000000000010200000000000000000000020400000000000000000000000000007004000000000000000000000000000000000000000000040000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1736,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000000000000000000000000000000100000000000000000100000000000000000102000000000000000000000204000000000000000410000000f800000000000000000000000000000000000000000000000000000000000000000000000000000000e0080000000000000000000000000000000000000000000800000000000000000800000000000000000810000000000000000000001020000000000000002080000000c00700000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1238,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c01000000000000000000000000000000000000000000010000000000000000010000000000000000020000000000000000020000000000000000000002040000000000000000000000000000700400000000000000000000000000000000000000000004000000000000000004000000000000000008000000000000000008000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1608,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_15);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_15);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000000000000000000000000000000100000000000000000100000000000000000200000000000000000200000000000000000000020400000000000000041000000078000000000000000000000000000000000000000000000000e00800000000000000000000000000000000000000000008000000000000000008000000000000000010000000000000000010000000000000000000001020000000000000002080000000c003000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1720,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000000000000000000000000000001000000000000000001000000000000000002080000000000000002000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e00800000000000000000000000000000000000000000008000000000000000008000000000000000010400000000000000010000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 982,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000000010000000000000000000000000000000000000000010200000000000000000000020400000000000000000000000000007004000000000000000000000400000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1432,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_20);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_20);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c01000000000000000000000100000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000a00000000000000000000000000000000000000000000000000000000000e00800000000000000000000080000000000000000000000000000000000000000081000000000000000000000102000000000000000208000000000050000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1608,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c01000000000000000000010000000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000f800000000000000000000000000000000000000000000000000000000000000000000000000000000e008000000000000000000080000000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000c00700000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1736,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(Paint:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_31);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000000100000000000000000000000000000000000000000002000000000000000002000000000000000000000204000000000000000410000000f800000000000000000000000000000000000000000000000000000000000000000000000000000000e0080000000000000000000800000000000000000000000000000000000000000010000000000000000010000000000000000000001020000000000000002080000000c00700000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1592,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000000100000000000000000100000000000000000000000000000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e0080000000000000000000800000000000000000800000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1544,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_11);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_11);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000001000000000000000001000000000000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000410000000580000000000000000000000000000000000000000e00800000000000000000008000000000000000008000000000000000000000000000000000000000800000000000000000810000000000000000000001020000000000000002080000000c0020000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1608,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_15);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_15);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000000100000000000000000100000000000000000000000000000000000000010000000000000000010200000000000000000000020400000000000000041000000078000000000000000000000000000000000000000000000000e00800000000000000000008000000000000000008000000000000000000000000000000000000000800000000000000000810000000000000000000001020000000000000002080000000c003000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1720,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_22);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000001000000000000000001000000000000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000410000000b000000000000000000000000000000000000000000000000000000000000000e00800000000000000000008000000000000000008000000000000000000000000000000000000080000000000000000000810000000000000000000001020000000000000002080000000800500000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1366,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:0();g2:1(Paint:new31);g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000001000000000000000001000000000000000000000000000000000000010000000000000000010000000000000000010200000000000000000000020400000000000000000000000000007004000000000000000000040000000000000000040000000000000000000000000000000000000400000000000000000400000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1256,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(Paint:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_9);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(Paint:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_9);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000100000000000000000000000000000000000000000000010200000000000000000000020400000000000000041000000048000000000000000000000000000000000000e0080000000000000000080000000000000000000000000000000000000000000008100000000000000000000010200000000000000020800000004002000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1110,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(Paint:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(Paint:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000010000000000000000000000000000000000000000010000000000000000000102000000000000000000000204000000000000000000000000000070040000000000000000040000000000000000000000000000000000000000040000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1544,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(Paint:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_19);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(Paint:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_19);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000100000000000000000100000000000000000000000000000000000000000001020000000000000000000002040000000000000004100000009800000000000000000000000000000000000000000000000000000000e0080000000000000000080000000000000000080000000000000000000000000000000000000000000810000000000000000000001020000000000000002080000000c00400000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1110,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000010800000000000000000000000000000000000000000100000000000000000102000000000000000000000204000000000000000000000000000070040000000000000000042000000000000000000000000000000000000000000400000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1704,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_13);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:1(Paint:new31);g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:1(Title:w1252_13);g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000010800000000000000000100000000000000000000000000000000000001000000000000000001000000000000000001020000000000000000000002040000000000000004100000006800000000000000000000000000000000000000000000e008000000000000000008400000000000000000080000000000000000000000000000000000000800000000000000000800000000000000000810000000000000000000001020000000000000002080000000400300000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1110,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c010000000000000000010800000000000000010000000000000000000000000000000000000000000102000000000000000000000204000000000000000000000000000070040000000000000000042000000000000000040000000000000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1238,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c01000000000000000001080000000000000001000000000000000000000000000000000000000000020800000000000000020000000000000000000002040000000000000000000000000000700400000000000000000420000000000000000400000000000000000000000000000000000000000008200000000000000008000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1366,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(TeamEdition:new31);g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:1(Paint:new31);g1:1(TeamEdition:new31);g2:1(Paint:new31);g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(TeamEdition:new31);g16:2(TeamEdition:new31,UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000108000000000000000100000000000000000000000000000000000000000108000000000000000208000000000000000200000000000000000000020400000000000000000000000000007004000000000000000004200000000000000004000000000000000000000000000000000000000004200000000000000008200000000000000008000000000000000000000810000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::PlayerHistoryKey,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 14,
        shape: "PlayerHistoryKey:u14",
        payload_hex: "0000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 51,
        shape: "Reservation:sys0_split24_zero:name_none:u3_true",
        payload_hex: "00000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 51,
        shape: "Reservation:sys0_split24_zero:name_none:u3_true",
        payload_hex: "00000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 435,
        shape: "Reservation:sys11_epic_w1252_33:name_utf16_5:u3_true",
        payload_hex: "580801000000000000000000000000000000000000000000000000000000000000000000000000d8ffffff070000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 483,
        shape: "Reservation:sys11_epic_w1252_33:name_utf16_8:u3_true",
        payload_hex: "580801000000000000000000000000000000000000000000000000000000000000000000000000c0ffffff070000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 435,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_10:u3_true",
        payload_hex: "58080100000000000000000000000000000000000000000000000000000000000000000000000050000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 443,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_11:u3_true",
        payload_hex: "5808010000000000000000000000000000000000000000000000000000000000000000000000005800000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 443,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_11:u3_true",
        payload_hex: "5808010000000000000000000000000000000000000000000000000000000000000000000000005800000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 459,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_13:u3_true",
        payload_hex: "58080100000000000000000000000000000000000000000000000000000000000000000000000068000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 459,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_13:u3_true",
        payload_hex: "58080100000000000000000000000000000000000000000000000000000000000000000000000068000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 475,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_15:u3_true",
        payload_hex: "580801000000000000000000000000000000000000000000000000000000000000000000000000780000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 491,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_17:u3_true",
        payload_hex: "5808010000000000000000000000000000000000000000000000000000000000000000000000008800000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 491,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_17:u3_true",
        payload_hex: "5808010000000000000000000000000000000000000000000000000000000000000000000000008800000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 403,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_6:u3_true",
        payload_hex: "580801000000000000000000000000000000000000000000000000000000000000000000000000300000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 411,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_7:u3_true",
        payload_hex: "58080100000000000000000000000000000000000000000000000000000000000000000000000038000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 419,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_8:u3_true",
        payload_hex: "5808010000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 427,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_9:u3_true",
        payload_hex: "580801000000000000000000000000000000000000000000000000000000000000000000000000480000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 315,
        shape: "Reservation:sys1_steam64:name_utf16_12:u3_true",
        payload_hex: "08000000000000000000a0ffffff0700000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 315,
        shape: "Reservation:sys1_steam64:name_utf16_12:u3_true",
        payload_hex: "08000000000000000000a0ffffff0700000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 347,
        shape: "Reservation:sys1_steam64:name_utf16_14:u3_true",
        payload_hex: "0800000000000000000090ffffff070000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 251,
        shape: "Reservation:sys1_steam64:name_utf16_8:u3_true",
        payload_hex: "08000000000000000000c0ffffff070000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 203,
        shape: "Reservation:sys1_steam64:name_w1252_10:u3_true",
        payload_hex: "0800000000000000000050000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 203,
        shape: "Reservation:sys1_steam64:name_w1252_10:u3_true",
        payload_hex: "0800000000000000000050000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 219,
        shape: "Reservation:sys1_steam64:name_w1252_12:u3_true",
        payload_hex: "08000000000000000000600000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 227,
        shape: "Reservation:sys1_steam64:name_w1252_13:u3_true",
        payload_hex: "0800000000000000000068000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 235,
        shape: "Reservation:sys1_steam64:name_w1252_14:u3_true",
        payload_hex: "080000000000000000007000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 243,
        shape: "Reservation:sys1_steam64:name_w1252_15:u3_true",
        payload_hex: "08000000000000000000780000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 283,
        shape: "Reservation:sys1_steam64:name_w1252_20:u3_true",
        payload_hex: "08000000000000000000a000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 291,
        shape: "Reservation:sys1_steam64:name_w1252_21:u3_true",
        payload_hex: "08000000000000000000a80000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 307,
        shape: "Reservation:sys1_steam64:name_w1252_23:u3_true",
        payload_hex: "08000000000000000000b800000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 339,
        shape: "Reservation:sys1_steam64:name_w1252_27:u3_true",
        payload_hex: "08000000000000000000d80000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 379,
        shape: "Reservation:sys1_steam64:name_w1252_32:u3_true",
        payload_hex: "080000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 147,
        shape: "Reservation:sys1_steam64:name_w1252_3:u3_true",
        payload_hex: "08000000000000000000180000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 147,
        shape: "Reservation:sys1_steam64:name_w1252_3:u3_true",
        payload_hex: "08000000000000000000180000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 155,
        shape: "Reservation:sys1_steam64:name_w1252_4:u3_true",
        payload_hex: "0800000000000000000020000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 155,
        shape: "Reservation:sys1_steam64:name_w1252_4:u3_true",
        payload_hex: "0800000000000000000020000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 163,
        shape: "Reservation:sys1_steam64:name_w1252_5:u3_true",
        payload_hex: "080000000000000000002800000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 163,
        shape: "Reservation:sys1_steam64:name_w1252_5:u3_true",
        payload_hex: "080000000000000000002800000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 171,
        shape: "Reservation:sys1_steam64:name_w1252_6:u3_true",
        payload_hex: "08000000000000000000300000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 179,
        shape: "Reservation:sys1_steam64:name_w1252_7:u3_true",
        payload_hex: "0800000000000000000038000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 179,
        shape: "Reservation:sys1_steam64:name_w1252_7:u3_true",
        payload_hex: "0800000000000000000038000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 187,
        shape: "Reservation:sys1_steam64:name_w1252_8:u3_true",
        payload_hex: "080000000000000000004000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 195,
        shape: "Reservation:sys1_steam64:name_w1252_9:u3_true",
        payload_hex: "08000000000000000000480000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 195,
        shape: "Reservation:sys1_steam64:name_w1252_9:u3_true",
        payload_hex: "08000000000000000000480000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 459,
        shape: "Reservation:sys2_playstation320:name_w1252_10:u3_true",
        payload_hex: "10000000000000000000000000000000000000000000000000000000000000000000000000000000000050000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 475,
        shape: "Reservation:sys2_playstation320:name_w1252_12:u3_true",
        payload_hex: "100000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 187,
        shape: "Reservation:sys7_psynet64:name_w1252_8:u3_true",
        payload_hex: "380000000000000000004000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::StatEvent,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 33,
        shape: "StatEvent:b1_i32",
        payload_hex: "0000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::StatEvent,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 33,
        shape: "StatEvent:b1_i32",
        payload_hex: "0000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::TeamLoadout,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 1040,
        shape: "TeamLoadout:blue[v28:u2:specials:banner:product:extra3]:orange[v28:u2:specials:banner:product:extra3]",
        payload_hex: "1c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::TeamLoadout,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 1040,
        shape: "TeamLoadout:blue[v28:u2:specials:banner:product:extra3]:orange[v28:u2:specials:banner:product:extra3]",
        payload_hex: "1c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::TeamPaint,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 88,
        shape: "TeamPaint:u8x3_u32x2",
        payload_hex: "0000000000000000000000",
    },
    Case {
        tag: ReplayNetworkAttributeTagV1::TeamPaint,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 88,
        shape: "TeamPaint:u8x3_u32x2",
        payload_hex: "0000000000000000000000",
    },
];
const OBJECT_TABLE: &[&str] = &[
    "TAGame.ProductAttribute_Painted_TA",
    "TAGame.ProductAttribute_UserColor_TA",
    "TAGame.ProductAttribute_TitleID_TA",
    "TAGame.ProductAttribute_SpecialEdition_TA",
    "TAGame.ProductAttribute_TeamEdition_TA",
];
fn objects() -> Vec<String> {
    OBJECT_TABLE.iter().map(|x| (*x).to_owned()).collect()
}
fn hex(s: &str) -> Vec<u8> {
    fn n(b: u8) -> u8 {
        match b {
            b'0'..=b'9' => b - b'0',
            b'a'..=b'f' => b - b'a' + 10,
            _ => panic!(),
        }
    }
    let b = s.as_bytes();
    b.chunks_exact(2)
        .map(|c| (n(c[0]) << 4) | n(c[1]))
        .collect()
}
fn pack(c: Case, start: usize, payload: usize, trail: usize) -> Vec<u8> {
    let p = hex(c.payload_hex);
    let total = start + payload + trail;
    let mut o = vec![0u8; total.div_ceil(8)];
    for i in 0..payload {
        if ((p[i / 8] >> (i % 8)) & 1) != 0 {
            o[(start + i) / 8] |= 1 << ((start + i) % 8);
        }
    }
    for i in 0..trail {
        if i % 2 == 0 {
            let q = start + payload + i;
            o[q / 8] |= 1 << (q % 8);
        }
    }
    o
}
fn ctx(c: Case) -> ReplayNetworkK4DecodeContextV1 {
    ReplayNetworkK4DecodeContextV1 {
        version_major: c.major,
        version_minor: c.minor,
        net_version: c.net,
        is_rl_223: c.rl223,
    }
}
#[test]
fn exact_table() {
    assert_eq!(CASES.len(), 161);
    assert_eq!(R3_17N_K4_ADMITTED_GROUPS_V1.len(), 161);
    for (g, c) in R3_17N_K4_ADMITTED_GROUPS_V1.iter().zip(CASES) {
        assert_eq!(g.attribute_tag, c.tag);
        assert_eq!(g.version_major, c.major);
        assert_eq!(g.version_minor, c.minor);
        assert_eq!(g.net_version, c.net);
        assert_eq!(g.is_rl_223, c.rl223);
        assert_eq!(g.payload_width, c.width);
        assert_eq!(g.structural_shape, c.shape);
    }
}
#[test]
fn positives_161() {
    let o = objects();
    for c in CASES.iter().copied() {
        let b = pack(c, 3, c.width as usize, 13);
        let a = decode_replay_network_k4_v1(&b, 3, c.tag, ctx(c), &o)
            .unwrap_or_else(|e| panic!("{} {e}", c.shape));
        assert_eq!(a.structural_shape, c.shape);
        assert_eq!(a.payload_width, c.width);
        assert_eq!(a.payload_end_bit, 3 + c.width);
        assert_eq!(a.value.attribute_tag(), c.tag);
        assert_eq!(
            a,
            decode_replay_network_k4_v1(&b, 3, c.tag, ctx(c), &o).unwrap()
        );
    }
}
#[test]
fn basics_negative() {
    let c = CASES[0];
    let o = objects();
    let b = pack(c, 3, c.width as usize, 8);
    let mut x = ctx(c);
    x.version_minor = 31;
    assert!(
        decode_replay_network_k4_v1(&b, 3, c.tag, x, &o)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-context")
    );
    assert!(
        decode_replay_network_k4_v1(&b, 3, ReplayNetworkAttributeTagV1::Boolean, ctx(c), &o)
            .unwrap_err()
            .to_string()
            .contains("unsupported-k4-tag")
    );
    assert!(
        decode_replay_network_k4_v1(&b, (b.len() * 8 + 1) as u64, c.tag, ctx(c), &o)
            .unwrap_err()
            .to_string()
            .contains("invalid-start")
    );
}
#[test]
fn truncation() {
    let o = objects();
    for c in [
        *CASES
            .iter()
            .find(|c| c.tag == ReplayNetworkAttributeTagV1::CamSettings)
            .unwrap(),
        *CASES
            .iter()
            .find(|c| {
                c.tag == ReplayNetworkAttributeTagV1::Reservation && c.shape.contains("sys11_epic")
            })
            .unwrap(),
        *CASES
            .iter()
            .find(|c| c.tag == ReplayNetworkAttributeTagV1::LoadoutsOnline)
            .unwrap(),
    ] {
        let w = c.width as usize;
        let start = (8 - ((w - 1) % 8)) % 8;
        let b = pack(c, start, w - 1, 0);
        assert_eq!(b.len() * 8, start + w - 1);
        let e = decode_replay_network_k4_v1(&b, start as u64, c.tag, ctx(c), &o)
            .unwrap_err()
            .to_string();
        assert!(
            e.contains("insufficient-bits") || e.contains("unadmitted-k4-shape"),
            "{e}"
        );
    }
}
#[test]
fn cross_products() {
    let o = objects();
    let fx = Case {
        tag: ReplayNetworkAttributeTagV1::DemolishFx,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 153,
        shape: "DemolishFx:attack_velocity:sb0:h5:cw2:victim_velocity:sb11:h4:cw13",
        payload_hex: "00000000000000000000000000c0020000000000",
    };
    let b = pack(fx, 3, fx.width as usize, 8);
    assert!(
        decode_replay_network_k4_v1(&b, 3, fx.tag, ctx(fx), &o)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-k4-shape")
    );
    let ext = Case {
        tag: ReplayNetworkAttributeTagV1::DemolishExtended,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 214,
        shape: "DemolishExtended:activex5:attacker_velocity:sb0:h5:cw2:victim_velocity:sb9:h4:cw11",
        payload_hex: "000000000000000000000000000000000000000000001200000000",
    };
    let b = pack(ext, 3, ext.width as usize, 8);
    assert!(
        decode_replay_network_k4_v1(&b, 3, ext.tag, ctx(ext), &o)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-k4-shape")
    );
    let res = Case {
        tag: ReplayNetworkAttributeTagV1::Reservation,
        major: 868,
        minor: 32,
        net: 10,
        rl223: true,
        width: 363,
        shape: "Reservation:sys11_epic_w1252_33:name_w1252_1:u3_true",
        payload_hex: "58080100000000000000000000000000000000000000000000000000000000000000000000000008000000000000",
    };
    let b = pack(res, 3, res.width as usize, 8);
    assert!(
        decode_replay_network_k4_v1(&b, 3, res.tag, ctx(res), &o)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-k4-shape")
    );
    let load = Case {
        tag: ReplayNetworkAttributeTagV1::LoadoutsOnline,
        major: 868,
        minor: 32,
        net: 10,
        rl223: false,
        width: 790,
        shape: "LoadoutsOnline:blue:outer28[g0:1(Paint:new31);g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:0();g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:0();g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]",
        payload_hex: "1c0100000000000000000000000000000000000000000000000102000000000000000000000204000000000000000000000000000070000000000000000000000000000000000408000000000000000000000810000000000000000000000000000000",
    };
    let b = pack(load, 3, load.width as usize, 8);
    assert!(
        decode_replay_network_k4_v1(&b, 3, load.tag, ctx(load), &o)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-k4-shape")
    );
}
#[test]
fn malformed_text_unknown_object() {
    let o = objects();
    let c = *CASES
        .iter()
        .find(|c| {
            c.tag == ReplayNetworkAttributeTagV1::Reservation && c.shape.contains("sys11_epic")
        })
        .unwrap();
    let mut b = vec![0u8; 6];
    fn set(b: &mut [u8], p: usize, v: u64, w: usize) {
        for i in 0..w {
            if ((v >> i) & 1) != 0 {
                b[(p + i) / 8] |= 1 << ((p + i) % 8);
            }
        }
    }
    set(&mut b, 3, 11, 8);
    set(&mut b, 11, 0x8000_0000, 32);
    assert!(
        decode_replay_network_k4_v1(&b, 0, c.tag, ctx(c), &o)
            .unwrap_err()
            .to_string()
            .contains("invalid-length-or-count")
    );
    let c = *CASES
        .iter()
        .find(|c| c.tag == ReplayNetworkAttributeTagV1::LoadoutsOnline)
        .unwrap();
    let b = pack(c, 3, c.width as usize, 8);
    let bad = vec!["Unknown".to_owned(); 5];
    assert!(
        decode_replay_network_k4_v1(&b, 3, c.tag, ctx(c), &bad)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-k4-shape")
    );
}
#[test]
fn teamloadout_unobserved_version() {
    let c = *CASES
        .iter()
        .find(|c| c.tag == ReplayNetworkAttributeTagV1::TeamLoadout)
        .unwrap();
    let p = hex(c.payload_hex);
    let mut bits = (0..c.width as usize)
        .map(|i| (p[i / 8] >> (i % 8)) & 1)
        .collect::<Vec<_>>();
    for (base, v) in [(0usize, 27u8), (520, 27u8)] {
        for i in 0..8 {
            bits[base + i] = (v >> i) & 1;
        }
    }
    let mut b = vec![0u8; bits.len().div_ceil(8)];
    for (i, x) in bits.into_iter().enumerate() {
        if x != 0 {
            b[i / 8] |= 1 << (i % 8);
        }
    }
    assert!(
        decode_replay_network_k4_v1(&b, 0, c.tag, ctx(c), &objects())
            .unwrap_err()
            .to_string()
            .contains("unadmitted-k4-shape")
    );
}
#[test]
fn rl223_exact_coupling() {
    let o = objects();
    let c = *CASES
        .iter()
        .find(|c| {
            !CASES.iter().any(|x| {
                x.tag == c.tag
                    && x.major == c.major
                    && x.minor == c.minor
                    && x.net == c.net
                    && x.rl223 != c.rl223
                    && x.width == c.width
                    && x.shape == c.shape
            })
        })
        .unwrap();
    let b = pack(c, 3, c.width as usize, 8);
    let mut x = ctx(c);
    x.is_rl_223 = !x.is_rl_223;
    assert!(
        decode_replay_network_k4_v1(&b, 3, c.tag, x, &o)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-k4-shape")
    );
}
