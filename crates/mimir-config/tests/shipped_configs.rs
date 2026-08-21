use mimir_config::{
    AnchorsConfig, BaseConfig, BranchingConfig, LabelingConfig, LoopConfig, ScoringConfig,
};

#[test]
fn all_shipped_toml_configs_deserialize_into_their_public_types() {
    let _: BaseConfig = toml::from_str(include_str!("../../../configs/mimir.base.toml"))
        .expect("shipped base config should deserialize");
    let _: AnchorsConfig = toml::from_str(include_str!("../../../configs/anchors.toml"))
        .expect("shipped anchors config should deserialize");
    let _: BranchingConfig = toml::from_str(include_str!("../../../configs/branching.toml"))
        .expect("shipped branching config should deserialize");
    let _: ScoringConfig = toml::from_str(include_str!("../../../configs/scoring.toml"))
        .expect("shipped scoring config should deserialize");
    let _: LabelingConfig = toml::from_str(include_str!("../../../configs/labeling.toml"))
        .expect("shipped labeling config should deserialize");
    let _: LoopConfig = toml::from_str(include_str!("../../../configs/loop.toml"))
        .expect("shipped loop config should deserialize");
}
