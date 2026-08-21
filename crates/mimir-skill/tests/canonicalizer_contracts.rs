use mimir_skill::{LowercaseTrimCanonicalizer, SkillCanonicalizer, canonicalize_record};
use mimir_types::{FieldValue, Metadata, SkillId, SkillRecord};

fn sample_record() -> SkillRecord {
    SkillRecord {
        id: SkillId::new("skill-identity-1"),
        family: "RecoveryFamilyV1".to_string(),
        canonical_name: "  LOW   Boost Recovery  ".to_string(),
        aliases: vec![
            "  Fast   Recovery ".to_string(),
            "WAVEDASH  RECOVERY".to_string(),
            "  Fast   Recovery ".to_string(),
        ],
        metadata: Metadata::from([
            ("source", FieldValue::Text("explicit".to_string())),
            ("rank", FieldValue::Integer(7)),
        ]),
    }
}

#[test]
fn lowercase_trim_canonicalizer_collapses_whitespace_and_case_only() {
    let canonicalizer = LowercaseTrimCanonicalizer;

    assert_eq!(
        canonicalizer.canonicalize("  LOW\tBoost\nRecovery  "),
        "low boost recovery"
    );
    assert_eq!(canonicalizer.canonicalize("   "), "");
}

#[test]
fn canonicalize_record_changes_only_canonical_name_and_alias_text() {
    let original = sample_record();
    let canonicalized = canonicalize_record(&original, &LowercaseTrimCanonicalizer);

    assert_eq!(canonicalized.id, original.id);
    assert_eq!(canonicalized.family, original.family);
    assert_eq!(canonicalized.metadata, original.metadata);
    assert_eq!(canonicalized.canonical_name, "low boost recovery");
    assert_eq!(
        canonicalized.aliases,
        vec![
            "fast recovery".to_string(),
            "wavedash recovery".to_string(),
            "fast recovery".to_string(),
        ]
    );
}

#[test]
fn canonicalize_record_preserves_alias_order_and_multiplicity() {
    let original = sample_record();
    let canonicalized = canonicalize_record(&original, &LowercaseTrimCanonicalizer);

    assert_eq!(canonicalized.aliases.len(), original.aliases.len());
    assert_eq!(canonicalized.aliases[0], canonicalized.aliases[2]);
    assert_ne!(canonicalized.aliases[0], canonicalized.aliases[1]);
}

#[test]
fn canonicalize_record_does_not_mutate_the_input_record() {
    let original = sample_record();
    let before = original.clone();

    let _ = canonicalize_record(&original, &LowercaseTrimCanonicalizer);

    assert_eq!(original, before);
}
