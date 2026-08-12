from pathlib import Path

path = Path('crates/mimir-replay/src/lib.rs')
text = path.read_text(encoding='utf-8')
marker = '#[derive(Debug, Default, Clone, Copy)]\npub struct MinimalReplayHeaderReader;'
if text.count(marker) != 1:
    raise SystemExit('R3.12 insertion marker drift')
if 'pub enum ReplayNetworkAttributeTagV1' in text:
    raise SystemExit('R3.12 registry already present')

attrs = [
('Engine.Actor:DrawScale','Float'),('Engine.Actor:RemoteRole','Enum'),('Engine.Actor:bBlockActors','Boolean'),('Engine.Actor:bCollideActors','Boolean'),('Engine.Actor:bHidden','Boolean'),
('Engine.GameReplicationInfo:GameClass','ActiveActor'),('Engine.GameReplicationInfo:ServerName','String'),('Engine.Pawn:PlayerReplicationInfo','ActiveActor'),
('Engine.PlayerReplicationInfo:Ping','Byte'),('Engine.PlayerReplicationInfo:PlayerID','Int'),('Engine.PlayerReplicationInfo:PlayerName','String'),('Engine.PlayerReplicationInfo:Score','Int'),('Engine.PlayerReplicationInfo:Team','ActiveActor'),('Engine.PlayerReplicationInfo:UniqueId','UniqueId'),('Engine.PlayerReplicationInfo:bTimedOut','Boolean'),('Engine.TeamInfo:Score','Int'),
('ProjectX.GRI_X:GameServerID','QWordString'),('ProjectX.GRI_X:MatchGUID','String'),('ProjectX.GRI_X:MatchGuid','String'),('ProjectX.GRI_X:ReplicatedGamePlaylist','Int'),('ProjectX.GRI_X:ReplicatedServerRegion','String'),('ProjectX.GRI_X:Reservations','Reservation'),('ProjectX.GRI_X:bGameStarted','Boolean'),
('TAGame.Ball_TA:GameEvent','ActiveActor'),('TAGame.Ball_TA:HitTeamNum','Byte'),('TAGame.Ball_TA:ReplicatedExplosionDataExtended','ExtendedExplosion'),('TAGame.Ball_TA:ReplicatedWorldBounceScale','Float'),
('TAGame.CameraSettingsActor_TA:CameraPitch','Byte'),('TAGame.CameraSettingsActor_TA:CameraYaw','Byte'),('TAGame.CameraSettingsActor_TA:PRI','ActiveActor'),('TAGame.CameraSettingsActor_TA:ProfileSettings','CamSettings'),('TAGame.CameraSettingsActor_TA:bMouseCameraToggleEnabled','Boolean'),('TAGame.CameraSettingsActor_TA:bUsingBehindView','Boolean'),('TAGame.CameraSettingsActor_TA:bUsingSecondaryCamera','Boolean'),('TAGame.CameraSettingsActor_TA:bUsingSwivel','Boolean'),
('TAGame.CarComponent_AirActivate_TA:AirActivateCount','Int'),('TAGame.CarComponent_Boost_TA:ReplicatedBoost','ReplicatedBoost'),('TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount','Byte'),('TAGame.CarComponent_Dodge_TA:DodgeImpulse','Location'),('TAGame.CarComponent_Dodge_TA:DodgeTorque','Location'),('TAGame.CarComponent_DoubleJump_TA:DoubleJumpImpulse','Location'),('TAGame.CarComponent_FlipCar_TA:FlipCarTime','Float'),('TAGame.CarComponent_FlipCar_TA:bFlipRight','Boolean'),('TAGame.CarComponent_TA:ReplicatedActive','Byte'),('TAGame.CarComponent_TA:Vehicle','ActiveActor'),
('TAGame.Car_TA:ClubColors','ClubColors'),('TAGame.Car_TA:ReplicatedDemolishExtended','DemolishExtended'),('TAGame.Car_TA:ReplicatedDemolishGoalExplosion','DemolishFx'),('TAGame.Car_TA:RumblePickups','ActiveActor'),('TAGame.Car_TA:TeamPaint','TeamPaint'),
('TAGame.GameEvent_Soccar_TA:ReplicatedScoredOnTeam','Byte'),('TAGame.GameEvent_Soccar_TA:ReplicatedStatEvent','StatEvent'),('TAGame.GameEvent_Soccar_TA:RoundNum','Int'),('TAGame.GameEvent_Soccar_TA:SecondsRemaining','Int'),('TAGame.GameEvent_Soccar_TA:bBallHasBeenHit','Boolean'),('TAGame.GameEvent_Soccar_TA:bClubMatch','Boolean'),('TAGame.GameEvent_Soccar_TA:bOverTime','Boolean'),('TAGame.GameEvent_Soccar_TA:bReadyToStartGame','Boolean'),
('TAGame.GameEvent_TA:BotSkill','Int'),('TAGame.GameEvent_TA:MatchStartEpoch','Int64'),('TAGame.GameEvent_TA:MatchTypeClass','ActiveActor'),('TAGame.GameEvent_TA:ReplicatedGameStateTimeRemaining','Int'),('TAGame.GameEvent_TA:ReplicatedRoundCountDownNumber','Int'),('TAGame.GameEvent_TA:ReplicatedStateName','Int'),('TAGame.GameEvent_TA:bCanVoteToForfeit','Boolean'),('TAGame.GameEvent_TA:bHasLeaveMatchPenalty','Boolean'),
('TAGame.GameEvent_Team_TA:MaxTeamSize','Int'),('TAGame.GameEvent_Team_TA:bForfeit','Boolean'),
('TAGame.PRI_TA:CarDemolitions','Int'),('TAGame.PRI_TA:ClientLoadouts','TeamLoadout'),('TAGame.PRI_TA:ClientLoadoutsOnline','LoadoutsOnline'),('TAGame.PRI_TA:ClubID','Int64'),('TAGame.PRI_TA:CurrentVoiceRoom','String'),('TAGame.PRI_TA:MatchAssists','Int'),('TAGame.PRI_TA:MatchGoals','Int'),('TAGame.PRI_TA:MatchSaves','Int'),('TAGame.PRI_TA:MatchScore','Int'),('TAGame.PRI_TA:MatchShots','Int'),('TAGame.PRI_TA:PartyLeader','PartyLeader'),('TAGame.PRI_TA:PersistentCamera','ActiveActor'),('TAGame.PRI_TA:PlayerHistoryKey','PlayerHistoryKey'),('TAGame.PRI_TA:PlayerHistoryValid','Boolean'),('TAGame.PRI_TA:ReplicatedGameEvent','ActiveActor'),('TAGame.PRI_TA:ReplicatedWorstNetQualityBeyondLatency','Byte'),('TAGame.PRI_TA:SelfDemolitions','Int'),('TAGame.PRI_TA:SpectatorShortcut','Int'),('TAGame.PRI_TA:SteeringSensitivity','Float'),('TAGame.PRI_TA:Title','Int'),('TAGame.PRI_TA:TotalGameTimePlayed','Float'),('TAGame.PRI_TA:ViralItemActor','ActiveActor'),('TAGame.PRI_TA:bIsDistracted','Boolean'),('TAGame.PRI_TA:bReady','Boolean'),
('TAGame.RBActor_TA:ReplicatedRBState','RigidBody'),('TAGame.RBActor_TA:bReplayActor','Boolean'),('TAGame.Team_TA:ClubColors','ClubColors'),('TAGame.Team_TA:ClubID','Int64'),('TAGame.Team_TA:GameEvent','ActiveActor'),('TAGame.VehiclePickup_TA:NewReplicatedPickupData','PickupNew'),('TAGame.Vehicle_TA:ReplicatedSteer','Byte'),('TAGame.Vehicle_TA:ReplicatedThrottle','Byte'),('TAGame.Vehicle_TA:bDriving','Boolean'),('TAGame.Vehicle_TA:bReplicatedHandbrake','Boolean')
]
if len(attrs) != 102 or len({name for name, _ in attrs}) != 102:
    raise SystemExit(f'attribute registry source drift: {len(attrs)}')

parents = [
('Engine.Actor','Core.Object'),('Engine.GameReplicationInfo','Engine.ReplicationInfo'),('Engine.Info','Engine.Actor'),('Engine.Pawn','Engine.Actor'),('Engine.PlayerReplicationInfo','Engine.ReplicationInfo'),('Engine.ReplicationInfo','Engine.Info'),('Engine.TeamInfo','Engine.Info'),('ProjectX.GRI_X','Engine.GameReplicationInfo'),('ProjectX.NetModeReplicator_X','Engine.ReplicationInfo'),('ProjectX.PRI_X','Engine.PlayerReplicationInfo'),('ProjectX.Pawn_X','Engine.Pawn'),('TAGame.Ball_TA','TAGame.RBActor_TA'),('TAGame.CameraSettingsActor_TA','Engine.ReplicationInfo'),('TAGame.CarComponent_AirActivate_TA','TAGame.CarComponent_TA'),('TAGame.CarComponent_Boost_TA','TAGame.CarComponent_AirActivate_TA'),('TAGame.CarComponent_Dodge_TA','TAGame.CarComponent_AirActivate_TA'),('TAGame.CarComponent_DoubleJump_TA','TAGame.CarComponent_AirActivate_TA'),('TAGame.CarComponent_FlipCar_TA','TAGame.CarComponent_TA'),('TAGame.CarComponent_Jump_TA','TAGame.CarComponent_TA'),('TAGame.CarComponent_TA','Engine.ReplicationInfo'),('TAGame.Car_TA','TAGame.Vehicle_TA'),('TAGame.CrowdActor_TA','Engine.ReplicationInfo'),('TAGame.CrowdManager_TA','Engine.ReplicationInfo'),('TAGame.GRI_TA','ProjectX.GRI_X'),('TAGame.GameEvent_Soccar_TA','TAGame.GameEvent_Team_TA'),('TAGame.GameEvent_TA','Engine.ReplicationInfo'),('TAGame.GameEvent_Team_TA','TAGame.GameEvent_TA'),('TAGame.InMapScoreboard_TA','Engine.Actor'),('TAGame.PRI_TA','ProjectX.PRI_X'),('TAGame.RBActor_TA','ProjectX.Pawn_X'),('TAGame.RumblePickups_TA','Engine.Actor'),('TAGame.Team_Soccar_TA','TAGame.Team_TA'),('TAGame.Team_TA','Engine.TeamInfo'),('TAGame.VehiclePickup_Boost_TA','TAGame.VehiclePickup_TA'),('TAGame.VehiclePickup_TA','Engine.ReplicationInfo'),('TAGame.Vehicle_TA','TAGame.RBActor_TA'),('TAGame.ViralItemActor_TA','Engine.Actor'),
('Archetypes.Ball.Ball_Default','TAGame.Ball_TA'),('Archetypes.Ball.Ball_Puck','TAGame.Ball_TA'),('Archetypes.Car.Car_Default','TAGame.Car_TA'),('Archetypes.CarComponents.CarComponent_Boost','TAGame.CarComponent_Boost_TA'),('Archetypes.CarComponents.CarComponent_Dodge','TAGame.CarComponent_Dodge_TA'),('Archetypes.CarComponents.CarComponent_DoubleJump','TAGame.CarComponent_DoubleJump_TA'),('Archetypes.CarComponents.CarComponent_FlipCar','TAGame.CarComponent_FlipCar_TA'),('Archetypes.CarComponents.CarComponent_Jump','TAGame.CarComponent_Jump_TA'),('Archetypes.GameEvent.GameEvent_Soccar','TAGame.GameEvent_Soccar_TA'),('Archetypes.Teams.Team0','TAGame.Team_Soccar_TA'),('Archetypes.Teams.Team1','TAGame.Team_Soccar_TA'),('GameInfo_Soccar.GameInfo.GameInfo_Soccar:GameReplicationInfoArchetype','TAGame.GRI_TA'),('Gameinfo_Hockey.GameInfo.Gameinfo_Hockey:Archetype','TAGame.GameEvent_Soccar_TA'),('Gameinfo_Hockey.GameInfo.Gameinfo_Hockey:GameReplicationInfoArchetype','TAGame.GRI_TA'),('ProjectX.Default__NetModeReplicator_X','ProjectX.NetModeReplicator_X'),('TAGame.Default__CameraSettingsActor_TA','TAGame.CameraSettingsActor_TA'),('TAGame.Default__PRI_TA','TAGame.PRI_TA'),('TAGame.Default__RumblePickups_TA','TAGame.RumblePickups_TA'),('TAGame.Default__ViralItemActor_TA','TAGame.ViralItemActor_TA'),('TAGame.ProductAttribute_Painted_TA','TAGame.ProductAttribute_TA'),('TAGame.ProductAttribute_TA','Core.Object'),('TAGame.ProductAttribute_TeamEdition_TA','TAGame.ProductAttribute_TA'),('TAGame.ProductAttribute_TitleID_TA','TAGame.ProductAttribute_TA'),('TAGame.ProductAttribute_UserColor_TA','TAGame.ProductAttribute_TA'),('TheWorld:PersistentLevel.CrowdActor_TA','TAGame.CrowdActor_TA'),('TheWorld:PersistentLevel.CrowdManager_TA','TAGame.CrowdManager_TA'),('TheWorld:PersistentLevel.InMapScoreboard_TA','TAGame.InMapScoreboard_TA'),('TheWorld:PersistentLevel.VehiclePickup_Boost_TA','TAGame.VehiclePickup_Boost_TA')
]
if len(parents) != 65 or len({child for child, _ in parents}) != 65:
    raise SystemExit(f'parent registry source drift: {len(parents)}')

spawns = [
('Engine.Actor','Location'),('Engine.ZoneInfo','None'),('TAGame.BreakOutActor_Platform_TA','None'),('TAGame.CrowdActor_TA','None'),('TAGame.CrowdManager_TA','None'),('TAGame.HauntedBallTrapTrigger_TA','None'),('TAGame.InMapScoreboard_TA','None'),('TAGame.PlayerStart_Platform_TA','None'),('TAGame.RBActor_TA','LocationAndRotation'),('TAGame.VehiclePickup_Boost_TA','None'),('TAGame.KeepUpIndicator_TA','LocationAndRotation')
]

variants = ['ActiveActor','Boolean','Byte','CamSettings','ClubColors','DemolishExtended','DemolishFx','Enum','ExtendedExplosion','Float','Int','Int64','LoadoutsOnline','Location','PartyLeader','PickupNew','PlayerHistoryKey','QWordString','ReplicatedBoost','Reservation','RigidBody','StatEvent','String','TeamLoadout','TeamPaint','UniqueId','NotImplemented']
attr_rows = '\n'.join(f'    ("{name}", ReplayNetworkAttributeTagV1::{tag}),' for name, tag in attrs)
parent_rows = '\n'.join(f'    ("{child}", "{parent}"),' for child, parent in parents)
spawn_rows = '\n'.join(f'    ("{name}", ReplayNetworkSpawnTrajectoryV1::{kind}),' for name, kind in spawns)
variant_rows = '\n'.join(f'    {name},' for name in variants)

registry = f'''/// Conservative network attribute wire-tag registry admitted from the supported replay lane.\n///\n/// Only the 102 attribute names observed in successfully decoded updates are explicitly admitted.\n/// Every other name maps to `NotImplemented`, even if a broader external registry knows it.\n/// This layer performs lookup only; it does not consume network bits or decode payload values.\n#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord, Hash)]\n#[serde(rename_all = "snake_case")]\npub enum ReplayNetworkAttributeTagV1 {{\n{variant_rows}\n}}\n\n#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord, Hash)]\n#[serde(rename_all = "snake_case")]\npub enum ReplayNetworkSpawnTrajectoryV1 {{\n    None,\n    Location,\n    LocationAndRotation,\n}}\n\nconst OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1: [(&str, ReplayNetworkAttributeTagV1); 102] = [\n{attr_rows}\n];\n\nconst OBSERVED_NETWORK_PARENT_CLASSES_V1: [(&str, &str); 65] = [\n{parent_rows}\n];\n\nconst PINNED_NETWORK_SPAWN_STATS_V1: [(&str, ReplayNetworkSpawnTrajectoryV1); 11] = [\n{spawn_rows}\n];\n\nconst NETWORK_INSTANCE_NORMALIZATION_KINDS_V1: [&str; 6] = [\n    "CrowdActor_TA",\n    "CrowdManager_TA",\n    "VehiclePickup_Boost_TA",\n    "InMapScoreboard_TA",\n    "BreakOutActor_Platform_TA",\n    "PlayerStart_Platform_TA",\n];\n\nconst RL_223_BUILD_VERSION_THRESHOLD_V1: &str = "221120.42953.406184";\n\npub fn replay_network_attribute_tag_v1(name: &str) -> ReplayNetworkAttributeTagV1 {{\n    OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1\n        .iter()\n        .find_map(|(candidate, tag)| (*candidate == name).then_some(*tag))\n        .unwrap_or(ReplayNetworkAttributeTagV1::NotImplemented)\n}}\n\npub fn replay_network_object_name_v1(name: &str) -> String {{\n    const PERSISTENT_LEVEL_PREFIX: &str = "TheWorld:PersistentLevel.";\n\n    let persistent_tail = if let Some(rest) = name.strip_prefix(PERSISTENT_LEVEL_PREFIX) {{\n        Some(rest)\n    }} else if let Some((_, suffix)) = name.split_once('.') {{\n        suffix.strip_prefix(PERSISTENT_LEVEL_PREFIX)\n    }} else {{\n        None\n    }};\n\n    if let Some(rest) = persistent_tail {{\n        for kind in NETWORK_INSTANCE_NORMALIZATION_KINDS_V1 {{\n            if rest.starts_with(kind) {{\n                return format!("{{PERSISTENT_LEVEL_PREFIX}}{{kind}}");\n            }}\n        }}\n    }}\n\n    name.to_string()\n}}\n\npub fn replay_network_parent_class_v1(name: &str) -> Option<&'static str> {{\n    let normalized = replay_network_object_name_v1(name);\n    OBSERVED_NETWORK_PARENT_CLASSES_V1\n        .iter()\n        .find_map(|(child, parent)| (*child == normalized.as_str()).then_some(*parent))\n}}\n\npub fn replay_network_spawn_trajectory_class_v1(\n    class_name: &str,\n) -> Option<ReplayNetworkSpawnTrajectoryV1> {{\n    PINNED_NETWORK_SPAWN_STATS_V1\n        .iter()\n        .find_map(|(candidate, trajectory)| (*candidate == class_name).then_some(*trajectory))\n}}\n\npub fn replay_network_qword_string_uses_text_v1(build_version: &str) -> bool {{\n    build_version >= RL_223_BUILD_VERSION_THRESHOLD_V1\n}}\n\n'''
text = text.replace(marker, registry + marker)

tests = r'''

    #[test]
    fn network_lookup_registry_has_exact_observed_attribute_surface() {
        assert_eq!(OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1.len(), 102);
        let names = OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
            .iter()
            .map(|(name, _)| *name)
            .collect::<BTreeSet<_>>();
        assert_eq!(names.len(), 102);
        assert!(OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
            .iter()
            .all(|(_, tag)| *tag != ReplayNetworkAttributeTagV1::NotImplemented));
        assert_eq!(
            OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
                .iter()
                .map(|(_, tag)| *tag)
                .collect::<BTreeSet<_>>()
                .len(),
            26
        );
    }

    #[test]
    fn network_lookup_registry_preserves_qword_string_wire_tag() {
        assert_eq!(
            replay_network_attribute_tag_v1("ProjectX.GRI_X:GameServerID"),
            ReplayNetworkAttributeTagV1::QWordString
        );
        assert_eq!(
            replay_network_attribute_tag_v1("TAGame.RBActor_TA:ReplicatedRBState"),
            ReplayNetworkAttributeTagV1::RigidBody
        );
    }

    #[test]
    fn network_lookup_registry_fails_closed_to_not_implemented() {
        assert_eq!(
            replay_network_attribute_tag_v1("TAGame.FutureClass:UnknownProperty"),
            ReplayNetworkAttributeTagV1::NotImplemented
        );
    }

    #[test]
    fn network_lookup_registry_qword_string_build_threshold_is_exact() {
        assert!(!replay_network_qword_string_uses_text_v1("221120.42953.406183"));
        assert!(replay_network_qword_string_uses_text_v1("221120.42953.406184"));
        assert!(replay_network_qword_string_uses_text_v1("230113.44243.411503"));
        assert!(!replay_network_qword_string_uses_text_v1("220826.56130.393105"));
    }

    #[test]
    fn network_lookup_registry_parent_surface_is_unique_and_acyclic() {
        assert_eq!(OBSERVED_NETWORK_PARENT_CLASSES_V1.len(), 65);
        let children = OBSERVED_NETWORK_PARENT_CLASSES_V1
            .iter()
            .map(|(child, _)| *child)
            .collect::<BTreeSet<_>>();
        assert_eq!(children.len(), 65);
        for (start, _) in OBSERVED_NETWORK_PARENT_CLASSES_V1 {
            let mut seen = BTreeSet::new();
            let mut current = start.to_string();
            while let Some(parent) = replay_network_parent_class_v1(&current) {
                assert!(seen.insert(current.clone()), "parent cycle at {current}");
                current = parent.to_string();
                assert!(seen.len() <= 65);
            }
        }
    }

    #[test]
    fn network_lookup_registry_normalizes_observed_persistent_instances() {
        assert_eq!(
            replay_network_object_name_v1("TheWorld:PersistentLevel.VehiclePickup_Boost_TA_37"),
            "TheWorld:PersistentLevel.VehiclePickup_Boost_TA"
        );
        assert_eq!(
            replay_network_object_name_v1("Stadium_P.TheWorld:PersistentLevel.CrowdActor_TA_12"),
            "TheWorld:PersistentLevel.CrowdActor_TA"
        );
        assert_eq!(
            replay_network_parent_class_v1("TheWorld:PersistentLevel.VehiclePickup_Boost_TA_37"),
            Some("TAGame.VehiclePickup_Boost_TA")
        );
        assert_eq!(replay_network_object_name_v1("TAGame.Car_TA"), "TAGame.Car_TA");
    }

    #[test]
    fn network_lookup_registry_spawn_surface_matches_pinned_source() {
        assert_eq!(PINNED_NETWORK_SPAWN_STATS_V1.len(), 11);
        assert_eq!(
            replay_network_spawn_trajectory_class_v1("Engine.Actor"),
            Some(ReplayNetworkSpawnTrajectoryV1::Location)
        );
        assert_eq!(
            replay_network_spawn_trajectory_class_v1("TAGame.RBActor_TA"),
            Some(ReplayNetworkSpawnTrajectoryV1::LocationAndRotation)
        );
        assert_eq!(
            replay_network_spawn_trajectory_class_v1("TAGame.KeepUpIndicator_TA"),
            Some(ReplayNetworkSpawnTrajectoryV1::LocationAndRotation)
        );
        assert_eq!(replay_network_spawn_trajectory_class_v1("Unknown.Class"), None);
    }

    #[test]
    fn network_lookup_registry_explicit_surface_is_present_in_supported_footer_lane() {
        let mut paths = vec![
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_002.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_003.replay"),
        ];
        let root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() || paths.iter().any(|path| !path.is_file()) {
            eprintln!("skipping R3.12 corpus registry regression; fixtures are absent");
            return;
        }
        let mut corpus = std::fs::read_dir(&root)
            .expect("largest_100 should be readable")
            .map(|entry| entry.expect("corpus entry should be readable").path())
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        corpus.sort();
        assert_eq!(corpus.len(), 100);
        paths.extend(corpus);

        let mut supported = 0usize;
        let mut explicit_names = BTreeSet::new();
        let mut fallback_names = BTreeSet::new();
        for path in paths {
            let bytes = std::fs::read(&path).expect("replay should be readable");
            let label = path.file_name().unwrap().to_string_lossy().into_owned();
            let input = ReplayInput::Memory { label, bytes };
            if MinimalReplayHeaderReader.read_header(&input).is_err() {
                continue;
            }
            supported += 1;
            let lookup = MinimalReplayFooterLookupMaterializationReader
                .read_footer_lookup_materialization(&input)
                .expect("supported replay footer lookup should materialize");
            for cache in lookup.net_cache {
                for property in cache.properties {
                    let name = &lookup.objects[property.object_index as usize];
                    if replay_network_attribute_tag_v1(name)
                        == ReplayNetworkAttributeTagV1::NotImplemented
                    {
                        fallback_names.insert(name.clone());
                    } else {
                        explicit_names.insert(name.clone());
                    }
                }
            }
        }
        assert_eq!(supported, 47);
        assert_eq!(explicit_names.len(), 102);
        assert_eq!(
            explicit_names,
            OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
                .iter()
                .map(|(name, _)| (*name).to_string())
                .collect::<BTreeSet<_>>()
        );
        assert!(!fallback_names.is_empty());
    }
'''
last = text.rfind('\n}')
if last < 0:
    raise SystemExit('tests module closing brace not found')
text = text[:last] + tests + text[last:]
path.write_text(text, encoding='utf-8')
print('PASS: applied bounded R3.12 network lookup registry patch')
