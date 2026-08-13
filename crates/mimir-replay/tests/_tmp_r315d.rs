use mimir_replay::{MinimalReplayNetworkFirstNewActorEnvelopeReader as R,ReplayInput,ReplayNetworkFirstNewActorEnvelopeReader,ReplayNetworkSpawnTrajectoryV1 as S};
use std::{fs,path::PathBuf};

const E:[&str;5]=[
 include_str!("_tmp_r315d_expected_1.tsv"),include_str!("_tmp_r315d_expected_2.tsv"),
 include_str!("_tmp_r315d_expected_3.tsv"),include_str!("_tmp_r315d_expected_4.tsv"),
 include_str!("_tmp_r315d_expected_5.tsv"),
];
fn b(s:&str)->bool{match s{"true"=>true,"false"=>false,_=>panic!("bad bool")}}
fn i32o(s:&str)->Option<i32>{if s=="null"{None}else{Some(s.parse().unwrap())}}
fn i8o(s:&str)->Option<i8>{if s=="null"{None}else{Some(s.parse().unwrap())}}
fn sp(s:&str)->S{match s{"none"=>S::None,"location"=>S::Location,"location_rotation"=>S::LocationAndRotation,_=>panic!("bad spawn")}}

#[test]
fn r3_15d_47_of_47_first_newactor_matches_pinned_oracle(){
 let root=PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
 let mut total=0usize; let mut counts=[0usize;3];
 for chunk in E{
  for line in chunk.lines().filter(|x|!x.is_empty()){
   let f:Vec<&str>=line.split('\t').collect(); assert_eq!(f.len(),18);
   let path=f[0]; assert_eq!(f[1].len(),64);
   let actor_id:u32=f[2].parse().unwrap(); let start:u64=f[3].parse().unwrap();
   let name:i32=f[4].parse().unwrap(); let opaque=b(f[5]); let object:i32=f[6].parse().unwrap();
   let spawn=sp(f[7]);
   let loc=if f[8]=="null"{None}else{Some((f[8].parse::<i32>().unwrap(),f[9].parse::<i32>().unwrap(),f[10].parse::<i32>().unwrap()))};
   let yaw=i8o(f[12]); let pitch=i8o(f[14]); let roll=i8o(f[16]);
   assert_eq!(b(f[11]),yaw.is_some()); assert_eq!(b(f[13]),pitch.is_some()); assert_eq!(b(f[15]),roll.is_some());
   let rot=if spawn==S::LocationAndRotation{Some((yaw,pitch,roll))}else{None};
   let end:u64=f[17].parse().unwrap();
   let bytes=fs::read(root.join(path)).unwrap_or_else(|e|panic!("{path}: {e}"));
   let input=ReplayInput::Memory{label:path.to_owned(),bytes};
   let d=R.read_network_first_new_actor_envelope(&input).unwrap_or_else(|e|panic!("{path}: {e}"));
   assert!(d.envelope.actor_present); assert_eq!(d.envelope.actor_id,Some(actor_id));
   assert_eq!(d.envelope.alive,Some(true)); assert_eq!(d.envelope.is_new,Some(true)); assert_eq!(d.envelope.stop_bit,start);
   let a=d.new_actor.expect("NewActor"); assert_eq!(a.name_id,name); assert_eq!(a.opaque_post_name_bit,opaque);
   assert_eq!(a.object_id,object); assert_eq!(a.spawn_kind,spawn); assert_eq!(a.stop_bit,end);
   assert_eq!(a.location.map(|v|(v.x,v.y,v.z)),loc); assert_eq!(a.rotation.map(|r|(r.yaw,r.pitch,r.roll)),rot);
   counts[match spawn{S::None=>0,S::Location=>1,S::LocationAndRotation=>2}]+=1; total+=1;
  }
 }
 assert_eq!(total,47); assert_eq!(counts,[5,11,31]);
 println!("R3_15D_DIFFERENTIAL=PASS rows=47 none=5 location=11 location_rotation=31");
}
