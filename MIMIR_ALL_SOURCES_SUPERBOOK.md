# MIMIR — ALL SOURCES SUPERBOOK

> **Role:** Canonical multi-source synthesis.
>
> This file combines the current GitHub truth, ChatGPT File Library discoveries,
> historical prototype evidence, design intent, migration candidates, and the end-to-end
> MIMIR roadmap. It MUST NOT override fresh source/tests. Current source/tests and exact-SHA
> evidence remain the highest authority.
>
> Cross-check chain:
>
> `MIMIR_KNOWLEDGE_GRAPH.md`
> → `MIMIR_CONTINUE_HERE.md`
> → `docs/chatgpt-archive/SOURCE_REGISTRY.md`
> → archived/sanitized source snapshots
> → `docs/chatgpt-archive/VALIDATION_MATRIX.md`
> → this superbook
>
> Archive verification:
> `scripts/verify_mimir_knowledge_archive.ps1`
>
> Machine-readable archive manifest:
> `docs/chatgpt-archive/MANIFEST.json`

---

## Güncel Durum + Tarihsel Prototipler + Tam Hedef Mimari + Execution Manual

**Tarih:** 2026-08-13
**Proje:** MIMIR
**Kanonik repository:** `Naveax/MIMIR`
**Yerel tarihsel kök:** `D:\RocketLeague bot\MIMIR`
**Ana uygulama dili:** Rust
**Belge amacı:** ChatGPT File Library / konuşma export'ları / generic isimli eski dosyalar / MIMIR tasarım belgeleri / Gabriel ve NX-HyperBot ile kesişen consumer belgeleri / güncel GitHub repository gerçeği tek bir dosyada birleştirmek.

---

# 0. BU BELGENİN KULLANIM KURALI

Bu dosyanın en önemli görevi MIMIR hakkındaki üç farklı bilgi türünü birbirine karıştırmamaktır:

```text
1. CURRENT VERIFIED PRODUCTION
   Bugünkü GitHub source + tests + admitted evidence ile kanıtlı.

2. HISTORICAL IMPLEMENTED / HISTORICAL EVIDENCE
   MIMIR adı konmadan önce veya ayrı prototiplerde gerçekten kodlanmış/çıktı üretilmiş,
   fakat bugünkü Rust MIMIR production capability'si sayılmayan şeyler.

3. TARGET DESIGN / FUTURE ARCHITECTURE
   Kabul edilmiş vizyon ve roadmap, fakat henüz production capability olmayan şeyler.
```

Bir şeyin eski Python prototipinde yapılmış olması, bugünkü Rust MIMIR'in yaptığı anlamına gelmez.

Bir şeyin Master Blueprint'te yazması, uygulanmış olduğu anlamına gelmez.

Bir şeyin Boxcars oracle tarafından decode edilmesi, native MIMIR decoder'ın decode ettiği anlamına gelmez.

Bir şeyin Rust type/contract olarak var olması da otomatik olarak gerçek end-to-end capability demek değildir.

**Ana precedence:**

```text
fresh GitHub source/tests
> exact-SHA CI/evidence
> canonical continuity
> admitted repo artifacts
> historical implementation/evidence
> design docs
> old chats
```

---

# 1. TARANAN KAYNAK SINIFLARI

Bu belge yalnız adında `MIMIR` bulunan dosyalardan oluşturulmadı.

File Library içinde semantik olarak şu imzalar tarandı:

```text
MIMIR
CORTEX
Replay Brain
Replay Coach
Rocket League replay parser
ReplayHeader
ReplayInput
Boxcars
Rattletrap
rrrocket
carball
network stream
actor envelope
RigidBody
CameraSettingsActor
PRI
replay slice
event window
anchor
Control-Onset Rewind
counterfactual
teacher factory
skill compiler
skill forge
low_boost_recovery
double wave dash
rare flick
curriculum
BC
DAgger
PPO
RocketSim
Gabriel
Scout Engine
Player War Map
Fast384ObsBuilder
212k replay
RLCS_REPLAYS_1V1
```

Bu yaklaşım özellikle şu generic dosyaları yakaladı:

```text
conversations-011.json
codex.txt
Yapıştırılan metin (3).txt
AE6DD28411F1508AD67AA6A178296A08_v0_2.events.jsonl
Naveax_replay_extracted_settings.json
rl_replay_analyzer_v0_2.py
rl_replay_event_coach_v1_adapter.py
test_rl_replay_analyzer_v0_2.py
```

Dolayısıyla filename-only arama MIMIR tarihinin ciddi bir bölümünü kaçırırdı.

---

# 2. CURRENT VERIFIED PRODUCTION — 2026-08-13

## 2.1 GitHub

```text
Repository:
Naveax/MIMIR

Default branch:
main

Latest main at audit time:
9d0060740d3e1f550f223a62b1407d5fd4ad9f9a
```

Bu son `main` commit'i continuity handbook genişletmesidir.

Current continuity'nin işaret ettiği son production-code checkpoint:

```text
ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
```

Production milestone:

```text
R3.13 — static replay network lookup plan
```

Son tamamlanan read-only format audit:

```text
R3.14 — first native network bitstream format audit
```

Şu anki exact pass:

```text
R3.14A — first frame + first actor envelope differential evidence
```

Pass türü:

```text
evidence-only
pinned-oracle instrumentation
NO production Rust change
```

Current supported replay lane:

```text
47 replays
```

Checked-in replay set:

```text
103 total
= 3 historical fixtures
+ largest_100 stress corpus
```

Pinned oracle:

```text
nickbabcock/boxcars
SHA:
c70e77df7af81b436cb545d070bb90c82f562d0b
```

Current evidence branch:

```text
agent/r3-14a-first-actor-envelope-evidence
```

Continuity'de kayıtlı branch head:

```text
f5713deee1a5a41620be257f07163cb33605c758
```

---

# 3. BUGÜNKÜ REPLAY STACK GERÇEKTE NEREYE KADAR GELDİ?

Eski handoff'larda MIMIR yalnız üç fixture'lı header parser gibi görünüyordu.

Bu artık güncel değil.

Bugünkü production replay katmanında aşağıdaki dar fakat gerçek katmanlar vardır.

## 3.1 Replay header

`ReplayHeader`

Temel alanlar:

```text
replay_id
source_label
total_frames
metadata
```

Header desteği fail-closed/admission tabanlıdır.

Broad wildcard desteği varmış gibi düşünülmemelidir.

---

## 3.2 Replay body structural boundary

Production type:

```text
ReplayBodyBoundaryV1
```

Taşıdığı şeyler:

```text
source_label
header_size
header_end
content_size
content_crc
content_start
content_end
input_len
```

Kritik ayrım:

```text
content_crc field okunabiliyor / taşınıyor
!=
CRC doğrulanıyor
```

Reader structural boundary kuruyor; CRC-validity capability claim edilmemeli.

---

## 3.3 Content scaffold

Production type:

```text
ReplayContentScaffoldV1
```

Taşıdığı structural offset/count bilgileri:

```text
levels
keyframes
network_size
network_start
network_end
footer_start
footer_size
```

Bu layer:

```text
network payload'un nerede olduğunu bilir
```

ama:

```text
network actor/property bitlerini native decode etmez
```

---

## 3.4 Footer scaffold

Production type:

```text
ReplayFooterScaffoldV1
```

Structural footer alanları:

```text
debug_info
tickmarks
packages
objects
names
class_indices
net_cache
opaque tail
footer end
```

Burada da structural/materialization ile semantic decode ayrımı korunur.

---

## 3.5 Footer lookup materialization

Production concepts:

```text
ReplayClassIndexV1
ReplayNetCachePropertyV1
ReplayNetCacheEntryV1
ReplayFooterLookupMaterializationV1
```

MIMIR artık footer'daki:

```text
object table
name table
class index
network cache
stream/property ilişkileri
```

için typed raw lookup tabloları oluşturabiliyor.

Bu production layer önemli, çünkü native network decoder'a statik schema/lookup bağlamı hazırlıyor.

Ancak:

```text
lookup table var
!=
network payload decode var
```

---

## 3.6 First-frame timing preamble

Production type:

```text
ReplayNetworkTimingPreambleV1
```

Şu anda native network payload'dan production'ın tüketmesine izin verilen dar bölüm:

```text
f32 first_frame_time
f32 first_frame_delta
```

Bu reader actor bitlerine geçmez.

Aynı zamanda header'dan:

```text
NumFrames
MaxChannels
channel_bits
```

gibi decoder prerequisites taşınır.

---

## 3.7 Network attribute tag registry

Production type:

```text
ReplayNetworkAttributeTagV1
```

Gözlenmiş/admitted exact property isimleri için tag registry vardır.

Tag aileleri arasında:

```text
ActiveActor
Boolean
Byte
CamSettings
ClubColors
DemolishExtended
DemolishFx
Enum
ExtendedExplosion
Float
Int
Int64
LoadoutsOnline
Location
PartyLeader
PickupNew
PlayerHistoryKey
QWordString
ReplicatedBoost
Reservation
RigidBody
StatEvent
String
TeamLoadout
TeamPaint
UniqueId
NotImplemented
```

yer alır.

Registry'de supported lane'de başarıyla gözlenmiş 102 exact attribute name admitted edilmiştir.

Bilinmeyen attribute:

```text
NotImplemented / fail-closed boundary
```

olmalıdır.

---

## 3.8 Spawn trajectory registry

Separate production concept:

```text
ReplayNetworkSpawnTrajectoryV1
```

Örnek varyantlar:

```text
None
Location
LocationAndRotation
```

Spawn trajectory semantics object cache availability ile tek bir kaba varsayımda birleştirilmemelidir.

---

## 3.9 Static network lookup plan

R3.13'ün esas production sonucu budur.

Concepts:

```text
ReplayNetworkResolvedPropertyV1
ReplayNetworkObjectLookupV1
ReplayNetworkLookupPlanV1
```

Per replay static plan şunları hazırlar:

```text
ReplayHeader
footer lookup materialization
NumFrames
MaxChannels
channel/build-derived flags
spawn-trajectory lookup
effective inherited properties
max_prop_id
prop_id_bits
stream_id -> property object/tag lookup
```

Bunu **network payload bitlerini tüketmeden** yapar.

---

# 4. R3.13 DIFFERENTIAL EVIDENCE

Pinned Boxcars oracle ile current supported lane üzerinde:

```text
supported replays:
47

attribute updates checked:
3,990,310

attribute updates matched:
3,990,310

unresolved_stream:
0

property_object_mismatch:
0

decoded_not_implemented_hits:
0
```

Bunun doğru yorumu:

> Static lookup plan, oracle'ın başarıyla decode ettiği attribute update'larda stream/property object çözümünü birebir eşleştirdi.

Yanlış yorum:

> MIMIR 3.99 milyon network attribute payload'unu native decode ediyor.

Native payload decode henüz production capability değildir.

---

# 5. ACTOR LIFECYCLE İÇİN KRİTİK FORMAT GERÇEĞİ

Supported corpus evidence:

```text
same actor ID
+ NewActor
+ same class overwrite
=
141,511 observation

same actor ID
+ NewActor
+ class-changing overwrite
=
0 observation
```

Bu nedenle gelecekte native lifecycle kodu şu hatayı yapmamalıdır:

```text
if actor_id already exists:
    malformed
```

Minimum lifecycle state machine ayrı ayrı düşünmelidir:

```text
new on unused id
same-class NewActor overwrite/replacement
class-changing overwrite
normal update
delete
update/delete missing actor
```

Şu an kanıtlanan tek önemli negatif kural:

```text
duplicate actor id alone != malformed
```

---

# 6. NATIVE NETWORK BITSTREAM — R3.14 FORMAT GERÇEĞİ

Read-only format audit ile admitted high-level order:

```text
frame
├─ f32 time
├─ f32 delta
└─ actor loop
   ├─ actor_present bit
   └─ if present
      ├─ bounded actor_id
      ├─ alive bit
      └─ if alive
         ├─ new bit
         ├─ if new
         │  ├─ version-gated name_id
         │  ├─ one additional bit
         │  ├─ object_id
         │  └─ spawn trajectory
         └─ else
            ├─ property_present bit loop
            ├─ bounded stream_id
            └─ attribute payload
```

Bu sıra roadmap'tir.

Bir kerede full decoder implement etme izni değildir.

---

# 7. BOUNDED INTEGER — ÇOK KRİTİK PROTOKOL KURALI

Actor ID ve stream ID ordinary fixed-width integer değildir.

Format davranışı:

```text
1. bound'a göre low bits okunur
2. candidate upper value hesaplanır
3. candidate/bound ilişkisine göre
   ek discriminator bit gerekebilir
4. low veya upper value seçilir
```

Bu nedenle yanlış implementasyon:

```text
read_bits(channel_bits)
```

veya:

```text
read_bits(prop_id_bits)
```

deyip bitirmektir.

Tek bir discriminator bit kaçırılması kalan bütün replay frame'ini kaydırabilir.

Bu yüzden R3.14A önce oracle ile cursor/evidence toplamaktadır.

---

# 8. CURRENT PASS — R3.14A

Amaç:

```text
47/47 supported replay üzerinde
ilk frame
+ ilk actor envelope header
bit cursor'ını
pinned Boxcars oracle ile differential olarak kanıtlamak
```

Bu pass'te evidence fields:

```text
first_frame.time
first_frame.delta
first_actor.actor_present
first_actor.actor_id
first_actor.alive
first_actor.new
```

Hard stop:

```text
name_id
unnamed bit after name_id
object_id
spawn payload
property-present loop
stream_id
attribute payload
next actor
next frame
raw state
```

R3.14A production Rust source değiştirmemelidir.

Outcome A olursa:

```text
R3.14B
evidence admission
+
native bit cursor / bounded integer contract
```

---

# 9. R3.14 SONRASI DAR NATIVE DECODER SIRASI

Current continuity ile en mantıklı dar zincir:

```text
R3.14A
first-frame + first-actor evidence

R3.14B
evidence admission + bit cursor/bounded-int contract

R3.14C
native bit cursor + bounded integer primitive

R3.14D
first actor envelope native reader

R3.14E
47-replay differential audit

R3.15A
new-actor spawn header / trajectory evidence

R3.15B
narrow native new-actor spawn envelope

R3.16A
existing-actor first-property envelope evidence

R3.16B
narrow native property envelope

R3.17+
attribute payload decoder families
```

Bundan sonra:

```text
multi actor
multi frame
actor state table
semantic entities
raw state
events
slices
skills
```

gelmelidir.

---

# 10. CURRENT CLOSED BOUNDARIES

Şu an production'da yapılmış SAYILMAMASI gerekenler:

```text
native actor_present reader admission
native bounded actor_id reader
native alive/new actor envelope production decoder
native name_id
native new actor object payload
native spawn payload
native existing actor property loop
native stream_id payload traversal
native attribute payload decode
actor lifecycle mutation from network bits
complete multi-actor iteration
complete multi-frame iteration
complete network trailer/end handling
canonical ball/car/player raw-state timeline
semantic event extraction
automatic replay slicing
native replay state -> skill mining
native replay state -> counterfactual simulation
```

---

# 11. CHATGPT STORAGE'TA BULUNAN PRE-MIMIR PROTOTİP: RL REPLAY COACH V0.2

Bu en önemli filename-independent bulgulardan biridir.

Dosya adı MIMIR değildir.

Tarih:

```text
2026-05-20
```

Ana dosyalar:

```text
rl_replay_analyzer_v0_2.py
test_rl_replay_analyzer_v0_2.py
RL_REPLAY_COACH_V0_2_README.md
run_rl_replay_coach_v0_2.ps1
rl_replay_event_coach_v1_adapter.py
AE6DD28411F1508AD67AA6A178296A08_v0_2.events.jsonl
```

Bu sistem MIMIR'in tarihsel atalarından biri olarak değerlendirilmelidir.

---

# 12. RL REPLAY COACH V0.2 GERÇEKTEN NE YAPIYORDU?

## 12.1 Header

Python parser şunları okuyordu:

```text
header_size
header_crc
major
minor
network_version
game_type
UE properties
```

Property parser birçok UE property çeşidi için logic içeriyordu:

```text
IntProperty
UIntProperty
FloatProperty
BoolProperty
StrProperty
NameProperty
QWordProperty
ByteProperty
ArrayProperty
StructProperty
```

ve bazı fallback/raw yolları.

---

## 12.2 Body structural parse

V0.2:

```text
body size
body CRC
levels
keyframes
raw network stream
footer
```

alanlarını ayrıştırıyordu.

Keyframe kayıtları:

```text
time_seconds
frame
byte_position
```

taşıyordu.

Network stream'in kendisini semantic decode etmek yerine:

```text
length
hash
raw section location
```

gibi structural evidence üretiyordu.

---

## 12.3 Footer

V0.2 tarafında:

```text
tick marks
packages
object table
dynamic names
class index
network cache related footer data
```

bulunuyordu.

Bu tarihsel kod, bugünkü Rust footer scaffold/materialization ile karşılaştırmalı bir secondary oracle olarak değerlendirilebilir.

Ancak bugünkü Rust implementation onun doğrudan continuation'ı varsayılmamalıdır.

---

# 13. RL REPLAY COACH V0.2 TEST FİXTURE

Historical fixture:

```text
AE6DD28411F1508AD67AA6A178296A08.replay
```

Test dosyasında kullanılan kopya:

```text
AE6DD28411F1508AD67AA6A178296A08(1).replay
```

Test edilen byte size:

```text
1,467,811
```

Header expectations:

```text
Map:
EuroStadium_Dusk_P

Team0Score:
2

Team1Score:
4

NumFrames:
7102
```

Player/goal test:

```text
player count:
4

focus player:
1 goal
3 assists

total goals:
6
```

Body/footer assertions:

```text
body size matches file:
true

network stream:
1,427,456 bytes

tick marks:
11

packages:
3

object table:
443

dynamic names:
249

class index:
43
```

Event windows:

```text
11
```

İlk yüksek negatif review:

```text
goal_against_review
window start:
0:17.53
```

Test script dört ana test için PASS bekliyordu ve conversation artifact'te bu pass'ler kayıtlıdır.

---

# 14. BU HISTORICAL FİXTURE 1V1 CORPUS'A GİRMEMELİ

Testte:

```text
4 players
```

olduğu için fixture 2v2'dir.

MIMIR'in ana corpus hedefi 1v1 olsa bile bu replay çok değerlidir.

Doğru kullanım:

```text
parser-format regression corpus
footer/network-structure regression corpus
historical oracle corpus
semantic parser edge fixture
```

Yanlış kullanım:

```text
1v1 tactical benchmark
1v1 player archetype ground truth
1v1 skill frequency statistics
```

Game-mode semantics ile binary format fixture aynı şey değildir.

---

# 15. HISTORICAL EVENT-WINDOW FİKRİ

V0.2 gerçek bir useful UI/analysis primitive üretmiş:

```text
event
→ pre_seconds = 5.0
→ post_seconds = 2.0
→ analysis window
```

Örnek event kinds:

```text
goal_against_review
focus_goal_finish
team_goal_assist_candidate
save_or_danger_highlight
```

Event artifact'te soru da tutuluyordu.

Örneğin yenen gol için:

```text
son adam kimdi?
challenge acele mi geldi?
boost rotası yanlış mıydı?
clear yerine commit mi denendi?
```

Bu fikir bugünkü MIMIR Replay Slice Engine için değerlidir.

Ama gelecekte fixed `[-5,+2]` tek policy olmamalıdır.

Daha doğru:

```text
event-family-specific window
+
Control-Onset Rewind
+
decision-onset boundary
```

---

# 16. RL REPLAY EVENT COACH V1 ADAPTER

`rl_replay_event_coach_v1_adapter.py` ayrı bir historical katmandır.

Bu script JSONL state-window almayı bekler.

State'te beklediği/işlediği veriler arasında:

```text
position
velocity
rotation-ish context
boost
on_ground
has_flip
ball position
player states
```

vardır.

Heuristic feature'ları:

```text
estimated time-to-ball
fastest player
fastest opponent
fastest teammate
goal angle
own-goal distance
opponent-goal distance
```

Diagnosis örnekleri:

```text
opponent reaches earlier
low boost + high ball
narrow direct-goal angle
own goal near + opponent early
insufficient evidence
```

Bu script:

```text
teacher truth
```

değildir.

Fakat gelecekte:

```text
native MIMIR scorer
vs
historical heuristic baseline
```

regression karşılaştırması için değerlidir.

---

# 17. MAYIS'TAKİ PHYSICS-DERIVED EXTRACTION ÇIKTISI

File Library içinde ayrıca aynı replay için:

```text
Naveax_replay_extracted_settings.json
```

bulunmuştur.

Bu dosyada player-linked replicated setting ve physics-derived özetler vardır.

**Gizlilik nedeniyle account/platform unique ID'leri bu handbook'a kopyalanmamıştır.**

Öne çıkan replicated settings:

```text
steering sensitivity
CameraSettingsActor-linked values:
- FOV
- distance
- height
- angle
- stiffness
- swivel speed
- transition speed
- camera mode flags
```

Ayrıca historical extraction output'ta physics-derived frame/motion özetleri görülmüştür:

```text
~7,097 physics-bearing frames
car position ranges
boost evolution
boost-active frames
powerslide-active frames
jump segments
double-jump segments
dodge segments
speed statistics
supersonic-like frames
touch list
boost pickup events
```

Bu çok önemli bir tarihsel sinyal.

Ancak producer/source provenance net şekilde yeniden bulunmadı.

Bu nedenle classification:

```text
HISTORICAL OUTPUT:
yes

PRODUCER PROVENANCE:
unresolved

CURRENT MIMIR CAPABILITY:
no

USE AS HARD GROUND TRUTH:
no

USE AS REPRODUCTION TARGET:
yes
```

---

# 18. PHYSICS OUTPUT İÇİN MIGRATION/RECOVERY PLANI

Bu historical output çöpe atılmamalı.

Aşağıdaki pass ileride yapılmalıdır:

```text
P1:
exact source replay identity verify

P2:
old JSON schema inventory

P3:
producer candidate search:
- Boxcars
- rrrocket
- rattletrap
- carball
- custom instrumented extractor

P4:
pinned parser revision ile reproduce

P5:
frame/touch/boost counts differential compare

P6:
only if reproducible:
admit as historical oracle fixture

P7:
native MIMIR decoder ile differential compare
```

Bu, native raw-state work açıldığında mükemmel bir bridge olabilir.

---

# 19. PRE-MIMIR PARSER RESEARCH TARİHİ

`conversations-011.json` gibi generic export dosyalarında şu parser adayları araştırılmıştır:

```text
Boxcars
Rattletrap
rrrocket
carball
RocketLeague-ReplayParser
RLGym replay parser tooling
```

Bugünkü doğru karar:

```text
Boxcars = pinned oracle/reference
MIMIR = native production decoder
```

Boxcars'ı production dependency'ye dönüştürmek MIMIR'in native decoder hedefini bozar.

Ama differential oracle olarak çok değerlidir.

---

# 20. ESKİ REPLAY BRAIN / POSITION LIBRARY VİZYONU KORUNMALI

`mimir_sistem_tasarimi.md` MIMIR'in daha eski kimliğini tarif eder:

```text
Replay Brain
+
Position Library
+
Benchmark Engine
```

Bu vizyon yeni Skill Forge tarafından ezilmemeli.

Çünkü Skill Forge'ın kalite kaynağı tam olarak bu corpus intelligence katmanıdır.

---

# 21. POSITION LIBRARY — HEDEF

Replay'ler milyonlarca anlamlı position segment'e dönüşebilir.

Örnek families:

```text
Kickoff
Possession
Challenge
Low 50
Fake Challenge
Shadow Defense
Goal Line Defense
Backboard Defense
Clear Position
Panic Clear
Wall Play
Aerial Challenge
Boost Control
Boost Starvation
Corner Escape
Counter Attack
Pressure Cycle
Shot Selection
Recovery
Demo Avoidance
```

Bir family alt türlere ayrılabilir.

Örnek:

```text
Shadow Defense
├─ Safe Shadow
├─ Too Close
├─ Too Far
├─ Fake Challenge Shadow
├─ Early Dive
├─ Backpost Shadow
└─ Goal Line Panic
```

---

# 22. POSITION OBJECT — HEDEF ŞEMA

Temel object:

```text
position_id
replay_id
slice/frame/time bounds
position family
phase
difficulty
risk
entry metrics
hold metrics
exit metrics
decision
outcome
confidence
provenance
tags
```

Score alanları:

```text
Entry Score
Hold Score
Exit Score
Decision Quality
Mechanical Execution
Risk Control
Boost Economy
Outcome Value
```

Bu score'ların sayısal ağırlıkları blueprint örneği olarak görülmeli; calibration/evidence olmadan hardcoded truth kabul edilmemeli.

---

# 23. MISTAKE PATTERN ENGINE

Hata yalnız bir string label olmamalıdır.

Mistake object:

```text
mistake_id
type
severity
timestamp/state reference
observed action
preferred/teacher action
expected value delta
confidence
supporting evidence
counterfactual evidence
```

Örnek types:

```text
early_challenge
panic_clear
overcommit
boost_waste
weak_recovery
poor_shadow_spacing
unsafe_touch
possession_throwaway
late_save_commit
```

Mistake cluster:

```text
single occurrence
→ repeated local pattern
→ player habit
→ archetype trait
→ targeted curriculum
```

---

# 24. PLAYER ARCHETYPE — RIGID CLASS DEĞİL TRAIT VECTOR

İleride en doğru yapı:

```text
aggression
challenge frequency
challenge patience
fake susceptibility
boost greed
boost starvation response
demo tendency
possession preference
direct-shot preference
wall preference
air preference
recovery quality
risk appetite
overcommit tendency
panic clear tendency
adaptation speed
predictability
```

Rigid label:

```text
"Aggressive Overcommitter"
```

human-readable summary olabilir.

Ama model internals trait-vector taşımalıdır.

---

# 25. GABRIEL / SCOUT / MIMIR SINIRI

Kanonik görev ayrımı:

```text
Gabriel Core
= oynar

Scout Engine
= canlı oyuncuyu probe eder ve telemetry toplar

MIMIR
= corpus knowledge, benchmark, retrieval, teacher/skill intelligence

Trainer/Teacher layer
= rapor/curriculum/coaching
```

Scout Engine'in live görevi MIMIR'e taşınmamalıdır.

---

# 26. PLAYER WAR MAP

Gabriel tasarım dosyalarından MIMIR query/benchmark schema'sına girmesi gereken kategoriler:

```text
Mechanical Map
Decision Map
Rotation Map
Pressure Map
Boost Map
Challenge Map
Possession Map
Defensive Map
Offensive Map
Recovery Map
Adaptation Map
Predictability Map
```

Aggression map alt metrikleri:

```text
First Challenge Speed
Challenge Frequency
Commit Depth
Ball Chase Rate
Boost Steal Intent
Demo Intent
Fake Challenge Discipline
Overcommit Risk
Recovery After Commit
Pressure Conversion
Punish Vulnerability
```

MIMIR bu profile corpus benchmark sağlamalıdır.

Scout, bu profile canlı evidence toplamalıdır.

---

# 27. PROBE CONTROLLER — SCOUT OWNERSHIP

Historical Gabriel idea:

```text
calibration
balanced pressure
fake/challenge tests
boost starvation
defensive weakness tests
exploit validation
final stress
```

Ancak fixed timeline zorunlu değildir.

Dynamic test selection:

```text
early challenge detected
→ more fake/delayed flick probes

passive player
→ boost deny/demo/backboard pressure

boostless panic
→ starvation cycles

weak shadow
→ flick/air/low50 pressure

bad recovery after commit
→ punish transition tests
```

MIMIR'in rolü:

```text
probe result
→ corpus comparison
→ weakness confidence
→ similar historical positions
→ candidate counters
```

---

# 28. MASTER DESIGN — MIMIR NE OLMALI?

Kabul edilmiş nihai identity:

```text
MIMIR =
Replay Intelligence Engine
+ Position Library
+ Benchmark Engine
+ Counterfactual Engine
+ Teacher Factory
+ Skill Compiler / Skill Forge
+ Curriculum Generator
+ Novelty & Mistake Memory
+ Confidence / Abstention Layer
+ Runtime Bridge
+ Policy Export
+ Evaluation & Evidence System
```

MIMIR:

```text
BC değildir
DAgger değildir
PPO değildir
SAC değildir
Gabriel değildir
```

Bunların hepsine adapter sağlayabilir.

---

# 29. REPLAY ABSOLUTE TRUTH DEĞİLDİR

Ana felsefe:

```text
Replay Action != Absolute Teacher Truth
Replay State = Search Seed
```

Replay actor:

```text
doğru yaptı
yanlış yaptı
doğru niyetle başarısız yaptı
rakip hata yaptığı için sonuç iyi göründü
yüksek mekanik ama düşük tactical value üretti
```

olabilir.

MIMIR'in görevi:

```text
observed
→ alternatives
→ physics/reachability
→ outcome comparison
→ reusable knowledge
```

---

# 30. ANCHOR MINING

Ağır counterfactual search her frame'e uygulanmamalıdır.

Anchor candidates:

```text
first_touch_setup
flick_setup
catch_window
low50_window
challenge_window
awkward_recovery
landing_recovery
save_window
near_post_save
wall_takeoff
aerial_intercept
reset_attempt
possession_transition
pressure_escape
bounce_read
preflip_intercept
post_touch_recovery
shadow_to_challenge
clear_window
controlled_touch
fake_window
```

Anchor Miner:

```text
"Bu an araştırmaya değer mi?"
```

Event Interpreter:

```text
"Bu an hangi olay/skill family?"
```

Ayrı sorumluluklar.

---

# 31. TEMPORAL WINDOW

Tek frame çoğu mechanic için yetersiz.

Temporal signals:

```text
ball acceleration delta
car angular velocity spike
jump/dodge timing
wheel contact transitions
relative ball-car velocity trend
relative offset trend
orientation alignment
boost burst
touch impulse
landing stabilization
approach curvature
opponent ETA change
possession transition
```

State contract geçmiş/şimdi/gelecek context'i desteklemelidir.

---

# 32. CONTROL-ONSET REWIND

Bu tasarım özellikle korunmalıdır.

Sorun:

```text
branch yalnız touch/flick/save anında başlarsa
setup hatasını göremez
```

Asıl karar daha önce olabilir:

```text
approach angle
speed
ball-car alignment
carry acquisition
small steering correction
boost schedule
jump preparation
opponent pressure positioning
```

Concept:

```text
t_control_onset
t_rollout_start = t_control_onset - rewind_margin
```

Modes:

```text
none
light
control
intent
```

Family örnekleri:

```text
flick -> control
catch -> control
low50 -> control
save -> light/control
recovery -> light
challenge -> light/intent
aerial -> event-specific
```

---

# 33. RAW STATE TARGET CONTRACT

Native decoder tamamlandıktan sonra canonical raw state, consumer-specific obs formatı olmamalıdır.

Önerilen alanlar:

## Ball

```text
position
linear velocity
angular velocity
rotation/orientation if meaningful
last touch
contact state
```

## Car

```text
position
linear velocity
angular velocity
orientation basis/quaternion
boost
on_ground
supersonic
demolished
jump availability
flip/dodge availability
wheel contact state
team
player identity reference
```

## Game context

```text
time
score
kickoff state
field/map
team direction
boost pads / timers where available
player counts
mutator/context
```

## Provenance per field

```text
DECODED
DERIVED
INFERRED
UNKNOWN
```

Inference confidence ayrı tutulmalıdır.

---

# 34. CANONICALIZATION

Amaç:

```text
aynı davranış farklı dünya koordinatlarında
aynı skill family'ye düşebilsin
```

Transforms:

```text
team-side normalization
field mirror
goal-direction normalization
car-local frame
ball-relative frame
surface-local frame
heading normalization
left/right symmetry where valid
```

Symmetry indiscriminately kullanılmamalıdır.

Potential asymmetry:

```text
boost layout
surface context
goal geometry
opponent arrangement
game-mode context
```

---

# 35. EVENT / CONTACT GRAPH

Nodes örnekleri:

```text
car state
ball state
surface contact
wheel contact
jump
dodge
boost event
touch
challenge
possession transition
goal/save
```

Edges:

```text
precedes
causes
contacts
transitions
constrains
enables
terminates
```

Graph:

```text
raw sequence
→ structured mechanic/tactical shape
```

köprüsüdür.

---

# 36. PHASE SEGMENTATION

Recovery örneği:

```text
airborne
orientation correction
descent
first contact
stabilization
momentum preservation
exit acceleration
```

Flick örneği:

```text
approach
capture
carry
setup/preload
jump
flip/contact
recovery
```

Double wave dash:

```text
setup
first jump
first landing
first dash
reorientation
second landing
second dash
recovery
```

Phases hardcoded yalnız tek replay'in timestamp'lerine bağlı kalmamalıdır.

---

# 37. SKILL PARAMETER INFERENCE

Skill:

```text
fixed input macro
```

olmamalı.

Parameter examples:

```text
entry speed
surface angle
approach angle
pitch
yaw
roll
jump timing
dodge timing
landing timing
powerslide window
boost schedule
ball-relative offset
opponent ETA
exit target vector
```

Skill object family envelope taşımalıdır.

---

# 38. COUNTERFACTUAL ENGINE

Counterfactual sorusu:

```text
"Bu state ailesinde başka ne yapılabilirdi?"
```

Primitive search grammar örneği:

```text
wait
steer
throttle
boost duration
jump timing
flip direction
powerslide
yaw/pitch/roll correction
approach target
intercept target
```

Bounded search zorunlu.

Her state'e 10,000 branch saçmak yasaklanmalıdır.

---

# 39. COMPUTE BUDGETING

Tier model:

```text
Tier 0:
cheap filter

Tier 1:
feature/event analysis

Tier 2:
limited counterfactual

Tier 3:
deep skill candidate

Tier 4:
rare/high-value research
```

Candidate priority:

```text
frequency
× expected match impact
× learnability
× transferability
× confidence
÷ compute cost
```

Rare skill frequency düşük olsa da impact/novelty/transfer yüksekse deep tier'e çıkabilir.

---

# 40. FEASIBILITY / REACHABILITY

Counterfactual branch skill candidate olabilmek için:

```text
physically reachable?
turn in time?
boost budget enough?
jump/flip available?
ball contact possible?
surface collision valid?
event order possible?
exit state stable?
```

Geçmelidir.

Fail:

```text
negative example
anti-target
failure boundary
```

olarak değerlidir.

---

# 41. ROCKETSIM ROLE

RocketSim MIMIR'in kendisi değildir.

Doğru ownership:

```text
mimir-sim-bridge
→ versioned SimBackend adapter
→ RocketSim backend
```

Use cases:

```text
micro rollout
feasibility
counterfactual validation
scenario generation
curriculum
short-horizon prediction
```

Current production'da real RocketSim backend varmış gibi claim edilmemelidir.

---

# 42. SIM-TO-GAME CALIBRATION

RocketSim yalnız "physics var" diye perfect oracle sayılamaz.

Ölç:

```text
position prediction drift
velocity drift
collision/contact drift
timing drift
bounce drift
recovery drift
```

Düşük confidence/OOD durumunda counterfactual claim downgrade edilmelidir.

Long-term:

```text
RocketSim
+
learned residual model
```

değerlendirilebilir.

---

# 43. MULTI-DIMENSIONAL SCORER

Tek scalar reward bilgi kaybettirir.

Score vector:

```text
goal probability / expected goal
concede risk
possession
ball progress
boost economy
recovery quality
goal-side positioning
pressure
future options
risk / variance
time
resource cost
human reachability when coaching
```

Aggregate score olabilir.

Ama decomposition kaybolmamalıdır.

---

# 44. CAUSAL ATTRIBUTION

MIMIR şunu ayırmaya çalışmalıdır:

```text
skill gerçekten iyi olduğu için mi başarılı?
rakip hata yaptığı için mi?
şanslı bounce yüzünden mi?
başka teammate/context yüzünden mi?
```

Bu özellikle replay teacher label kalitesi için önemlidir.

---

# 45. ANTI-TARGET

MIMIR yalnız positive target üretmemelidir.

Örnek:

```text
too early dodge
wrong landing wheel
overboost
unsafe challenge
panic clear
possession throwaway
late recovery
fake success due to opponent error
```

Kullanımlar:

```text
negative BC example
ranking loser
preference pair
penalty mask
hard exclusion
failure classifier
```

---

# 46. TEACHER FACTORY

Teacher source ensemble:

```text
human replay
counterfactual correction
self-play
Gabriel
V1
search
micro-rollout
validated skill
multi-source agreement
```

Teacher output:

```text
state/action label
option label
trajectory/subgoal
phase label
ranking pair
anti-target
confidence
abstain
expected value
risk
reason/evidence
```

---

# 47. CONFIDENCE + ABSTAIN

Confidence decomposition:

```text
parser confidence
state quality
event confidence
segment confidence
intent confidence
physics confidence
counterfactual confidence
corpus support
OOD score
teacher agreement
```

ABSTAIN geçerli ve beklenen output'tur.

Kötü hard label üretmekten iyidir.

Threshold'lar design example olabilir; calibration ile öğrenilmelidir.

---

# 48. HUMAN OPTIMAL VS BOT OPTIMAL

Teacher Mode için iki ayrı objective profile gerekli olabilir:

```text
BOT_OPTIMAL
HUMAN_OPTIMAL
```

Human model içine:

```text
reaction time
mechanical consistency
controller limits
execution variance
learnability
```

girmelidir.

Teacher:

```text
"37 ms içinde kusursuz flip yapmalıydın"
```

gibi insan için anlamsız öneriler üretmemelidir.

---

# 49. SKILL FORGE

Ana pipeline:

```text
Replay Slice
→ Candidate Detection
→ Skill Seed
→ Canonicalization
→ Event/Contact Graph
→ Phase Segmentation
→ Intent
→ Parameters
→ Counterfactual/Physics Expansion
→ Feasibility
→ Skill Synthesis
→ Curriculum
→ Export
→ Eval
→ Library Admission
```

Tek replay moment:

```text
skill seed
```

olabilir.

Doğrudan tam skill değildir.

---

# 50. FIRST VERTICAL SLICE — LOW BOOST RECOVERY

MIMIR tarihçesiyle uyumlu ilk family:

```text
low_boost_recovery
```

Acceptance output:

```text
exact source provenance
real replay slice
canonical state
event/contact graph
phase segmentation
parameters
success objective
failure objective
generated variants
validation results
curriculum
export artifact
evaluation report
```

Reject:

```text
source drift
missing state
impossible timing
insufficient evidence
physics invalid
confidence too low
```

---

# 51. DOUBLE WAVE DASH — PROOF OF GENERALIZATION

Vitrin deneyi:

```text
one observed rare seed
→ canonical family
→ variants
→ held-out perturbations
```

Held-out dimensions:

```text
unseen angles
unseen speeds
unseen landing offsets
unseen boost states
```

Success claim:

```text
"MIMIR, bir observed seed'den physics-validated varyasyonlar ve curriculum
üzerinden unseen valid states'e transfer eden skill family üretti."
```

Yasak success claim:

```text
"MIMIR bir replay gördü ve double wave dash'i her durumda öğrendi."
```

---

# 52. RARE FLICK / BILLION-IN-ONE

Rare mechanic admission:

```text
slice
intent
ball-car geometry
opponent context
contact mechanics
parameters
variation
tactical validation
transferability
skill admission
```

Yalnız mechanic execution yeterli değildir.

Ölç:

```text
goal value
possession value
opponent dependency
failure cost
recovery cost
repeatability
```

---

# 53. SKILL LIFECYCLE

Library sonsuza kadar büyüyemez.

Gerekli:

```text
fingerprint
similarity
deduplication
merge
split
versioning
coverage stats
success stats
aging
dominance
retirement
revival
novelty
```

Skill B aynı envelope'da sürekli A'yı domine ediyorsa A aktif library'den düşebilir.

---

# 54. ADVANCED SKILL ECOSYSTEM

Later systems:

```text
Skill Composer
Counter-Skill Miner
Skill Mutation
Skill Distillation
Skill Internalization Detector
Adversarial Curriculum
Opponent-Conditioned Skill Variants
Causal Attribution
Skill Value per Compute
```

Bunlar first vertical slice'ın önüne geçmemeli.

---

# 55. CURRICULUM

Generic progression:

```text
easy deterministic
→ low variance
→ medium perturbation
→ hard perturbation
→ opponent pressure
→ adversarial
→ match distribution
```

Difficulty manual hardcode + automatic calibration hybrid başlayabilir.

Performance distribution'a göre ileride auto-tune edilir.

---

# 56. NX-HYPERBOT CONSUMER EVIDENCE — DOSYA ADI MIMIR DEĞİL

Generic `codex.txt` / `Yapıştırılan metin (3).txt` dosyalarında gerçek Rocket League training consumer örnekleri bulundu.

Historical reset/curriculum families arasında:

```text
midfield_loose_ball
shadow_defense
goal_line_save
low_boost_recovery
corner_clear
full_match
opponent_breakaway
open_net_convert
transition_break
midfield_5050
```

vardır.

Bu önemli çünkü:

```text
MIMIR curriculum family
→ consumer adapter
→ existing reset/scenario family
```

bridge'i gerçek bir consumer yüzeyine map edilebilir.

Ama NX reward/trainer logic MIMIR core'a gömülmemelidir.

---

# 57. FAST384 CONSUMER CONTRACT DERSİ

Historical Fast384 implementation farklı revizyonlardan geçmiş.

Bir sonraki MIMIR canonical state'i:

```text
384 dimension
```

diye hard-lock edilmemelidir.

Doğru:

```text
rich canonical state
→ versioned Fast384 adapter
```

Fast384 consumer'ın kullandığı semantik kategoriler:

```text
self car
opponent
ball
relative geometry
local alignment
boost pads/topology
temporal history
ball prediction
tactical/game context
previous action
```

MIMIR raw state bu bilgileri sağlayabilmeli veya explicit UNKNOWN bırakabilmelidir.

---

# 58. OBSERVATION EXPORT QUALITY GATES

NX-HyperBot tarihsel hatalarından çıkan MIMIR adapter dersleri:

```text
dimension drift checkpoint bozabilir
dead features eğitim kalitesini düşürür
NaN/Inf fail-closed olmalı
team mirroring doğrulanmalı
feature versioning gerekli
consumer schema exact olmalı
```

MIMIR export validation:

```text
schema version
shape
finite values
range policy
feature availability mask
provenance
source distribution
consumer compatibility
```

taşımalıdır.

---

# 59. BC EXPORT

MIMIR core BC'ye bağlı değildir.

Adapter:

```text
canonical state / teacher / skill
→ BC sample
```

Önerilen fields:

```text
observation
action
skill_id
phase
weight
confidence
provenance
anti-target/ranking context
```

Low-confidence output hard label olmamalıdır.

---

# 60. DAGGER EXPORT

Pipeline:

```text
student rollout state
→ MIMIR teacher query
→ correction / option
→ confidence / abstain
→ aggregate dataset
```

MIMIR'in BC↔DAgger bridge rolü burada gerçek olur.

---

# 61. PPO / RL AUXILIARY EXPORT

MIMIR PPO trainer'ın kendisi değildir.

Sağlayabilir:

```text
skill labels
phase labels
auxiliary targets
state-value hints
preference pairs
anti-targets
curriculum scenarios
reward shaping candidates
```

Reward change otomatik ve limitsiz mutate edilmemelidir.

Admission/eval gate şarttır.

---

# 62. RUNTIME BRIDGE

Runtime ağır MIMIR search engine değildir.

Offline:

```text
parse
mine
simulate
validate
compile
```

Online:

```text
classify state
lookup
check eligibility
check confidence
choose option
fallback/abort
```

Runtime packages:

```text
skill library subset
preconditions
parameter policy
abort rules
fallback
confidence calibration
opponent priors
scenario classifier
```

---

# 63. RUNTIME FALLBACK TYPES

Örnek:

```text
Recovery Fallback
Defensive Safety
Boostless Escape
Goal-side Restore
Possession Preservation
Abort Unsafe Mechanic
```

False activation rate ayrıca benchmark edilmelidir.

---

# 64. MEMORY

MIMIR memory katmanları:

```text
Episodic Memory
= exact replay/state/slice

Semantic Memory
= generalized learned relationships

Skill Memory
= reusable skill families

Novelty Memory
= rare/new/unknown cases
```

Novelty candidates:

```text
rare recovery
strange fake
unusual kickoff
double wave dash
unexpected pinch
bizarre save
new opponent behavior
new failure cluster
```

---

# 65. SEARCH / RETRIEVAL INDEX

212k corpus'ta her query'de full replay taranmaz.

Index keys:

```text
mode
rank
player
skill
event
field region
boost
ball height
car speed
score
time remaining
pressure
mechanic
outcome
confidence
source type
```

Semantic query example:

```text
"low boost backboard recovery under pressure"
```

---

# 66. 212K CORPUS

Historical local audit:

```text
RLCS_REPLAYS_1V1:
212,339 replay
~148.14 GB
```

Checked-in largest_100:

```text
stress/regression corpus
```

olmalıdır.

"100 largest":

```text
semantic diversity
```

kanıtı değildir.

Ek benchmark corpora gerekli:

```text
version/build coverage
malformed/truncated
event ground truth
skill ground truth
mechanic diversity
tactical diversity
rare events
sim differential
```

---

# 67. TIERED CORPUS MINING

Full corpus pipeline:

```text
file discovery
→ identity/hash
→ cheap structural/header scan
→ candidate filter
→ deeper native decode
→ event extraction
→ slice mining
→ dedup
→ cluster
→ deep skill/teacher analysis
```

Her replay'e aynı compute verilmemelidir.

---

# 68. INCREMENTAL INDEX

Per replay:

```text
path/reference
size
mtime
hash
replay_id
version/build
parse stage
parse status
last processed code/schema version
failure reason
```

Unchanged replay skip edilir.

Schema/code değişince deterministic invalidation gerekir.

---

# 69. PARALLELISM

212k replay için:

```text
bounded worker pool
backpressure
deterministic sharding
resume/checkpoint
failure quarantine
batching
sequential I/O planning
cache
```

Parser CPU-first olabilir.

GPU yalnız faydalı katmanlarda:

```text
embeddings
similarity
learned classifiers
policy evaluation
batch scoring
```

kullanılmalıdır.

---

# 70. CACHE HIERARCHY

Öneri:

```text
replay bytes identity
→ structural parse
→ native network parse
→ raw timeline
→ events
→ slices
→ canonical features
→ skill candidates
→ counterfactual results
→ teacher/export
```

Her katman:

```text
code/schema/config version
+
source hash
```

ile invalidatable olmalıdır.

---

# 71. PROVENANCE

Her önemli output geriye trace edilebilmeli:

```text
runtime package
→ skill
→ validated variant
→ counterfactual result
→ canonical state
→ slice
→ frame range
→ replay id
→ replay SHA
```

Export sample:

```text
BC sample
→ teacher label
→ counterfactual result
→ replay slice
→ replay hash
```

---

# 72. PROVENANCE TRUST LEVELS

Blueprint'ten yararlı model:

```text
T0
synthetic/unverified

T1
parsed replay

T2
validated replay segment

T3
counterfactual physics validated

T4
multi-source corroborated

T5
live-eval proven
```

Bu exact thresholds başlangıç tasarımıdır; implementation'da versioned policy gerekir.

---

# 73. DATA SOURCE TYPE

Her sample source type taşımalı:

```text
Human Replay
Bot Self-Play
Live Bot Trace
Synthetic Physics Variation
Counterfactual Rollout
```

Synthetic sample gerçek human evidence gibi sunulmamalıdır.

---

# 74. DATA LEAKAGE

Train/eval split:

```text
match-aware
player-aware
time-aware
session-aware
seed-neighborhood-aware
```

Aynı replay'in neredeyse aynı framelerini train/test'e koyup generalization claim etmek yasaktır.

Skill eval split:

```text
seed neighborhood train
boundary validation
held-out perturbations
different replay contexts
live rollout
```

---

# 75. CALIBRATION

Confidence yalnız güzel görünen sayı olmamalıdır.

Teacher/event/skill confidence için ileride:

```text
Brier score
ECE
reliability curves
coverage vs accuracy
abstention curve
OOD false activation
```

gibi metrikler eklenebilir.

---

# 76. FAILURE ARTIFACT

Başarısız branch çöpe gitmemelidir.

Record:

```text
state
attempt
failure reason
physics result
recovery consequence
score vector
boundary
```

Kullanım:

```text
anti-target
hard negative
failure classifier
skill envelope
curriculum boundary
```

---

# 77. EVIDENCE PACKET

Her major teacher/skill:

```text
why selected
source replay/slice
what alternatives tested
what failed
counterfactual support
physics status
confidence
OOD
runtime restrictions
consumer restrictions
```

taşıyabilir.

---

# 78. MIMIR'İN KENDİ BENCHMARK'I

Ölç:

```text
parser coverage
native decoder differential agreement
event precision/recall
skill extraction accuracy
teacher correctness
counterfactual calibration
retrieval recall
runtime export success
false activation
curriculum efficiency
task gain
win rate/Elo gain where relevant
catastrophic error reduction
```

---

# 79. MANUAL GROUND TRUTH SET

Küçük fakat yüksek kaliteli manual set tutulmalı:

```text
known touches
known saves
known goals
known challenge onset
known recovery phases
known skill labels
known player archetype examples
```

Büyük noisy corpus, küçük precise benchmark'ın yerine geçmez.

---

# 80. SECURITY / PRIVACY / PUBLIC REPO

GitHub repository public'tir.

Bu nedenle File Library'deki tarihsel player/account metadata doğrudan repo'ya kopyalanmamalıdır.

Özellikle:

```text
platform account unique IDs
private local identifiers
personal paths when unnecessary
session-specific private metadata
```

redact edilmelidir.

Fixture provenance için gerekli local path dokümantasyonu da mümkünse portable label/hash ile değiştirilmelidir.

---

# 81. HISTORICAL FILE CLASSIFICATION

## CURRENT/REFERENCE DESIGN

```text
MIMIR_MASTER_DESIGN_SPEC_2026-08-12.md
MIMIR_MASTER_BLUEPRINT_2026-08-12.md
MIMIR_Gabriel_V1_Tam_Mimari_ve_Yol_Haritasi.md
mimir_sistem_tasarimi.md
gabriel_sistem_tasarimi.md
MIMIR_DETAILED_EXECUTION_ROADMAP.md
```

Bunların current-state bölümleri tarihsel olabilir; design intent bölümleri değerlidir.

## HISTORICAL EXACT EXECUTION / SUPERSEDED CURRENT STATE

```text
MIMIR_TAM_PLAN_TEK_DOSYA.md
MIMIR_NEXT_CHAT_HANDOFF_FULL.md
MIMIR_NEW_CHAT_START_PROMPT.md
fixture_001/002/003 era executor artifacts
```

Bu belgeler process/evidence discipline için değerlidir.

Ama R3.13/R3.14A'nın current state'i üzerine yazamaz.

## PRE-MIMIR IMPLEMENTED PROTOTYPE

```text
rl_replay_analyzer_v0_2.py
test_rl_replay_analyzer_v0_2.py
RL_REPLAY_COACH_V0_2_README.md
run_rl_replay_coach_v0_2.ps1
rl_replay_event_coach_v1_adapter.py
AE6DD...events.jsonl
```

## HISTORICAL OUTPUT — PRODUCER UNRESOLVED

```text
Naveax_replay_extracted_settings.json
```

## CONSUMER-ADJACENT

```text
NX-HyperBot fast384/curriculum codex dumps
Gabriel Scout Engine design
RocketSim integration design
```

## NOISY BUT USEFUL SEARCH CONTAINER

```text
conversations-011.json
```

---

# 82. CORTEX SEARCH RESULT

MIMIR'in eski isim alternatifi olarak CORTEX geçmiş konuşmalarda konsept olarak anılmış olabilir.

Ancak File Library semantik taramasında ayrı ve güçlü bir `CORTEX` implementation/spec corpus'u bulunmuş kabul edilmemelidir.

Bu nedenle:

```text
CORTEX = historical naming lead
```

olarak tutulmalı;

```text
CORTEX = missing predecessor codebase
```

diye hayali migration planı üretilmemelidir.

---

# 83. BUGÜNKÜ CAPABILITY MATRIX

| Capability | Durum | Açıklama |
|---|---|---|
| Replay header parsing | PARTIAL / PRODUCTION | Admitted lane |
| Body boundary | YES / STRUCTURAL | CRC validity claim yok |
| Content scaffold | YES / STRUCTURAL | network section locates |
| Footer scaffold | YES / STRUCTURAL | offsets/counts |
| Footer object/name/class/net-cache lookup | YES / PRODUCTION | typed raw materialization |
| First-frame time/delta | YES / NARROW | timing preamble |
| Static network attribute tag registry | YES | 102 observed names + fail closed |
| Static stream/property lookup plan | YES | R3.13 |
| Static lookup differential evidence | STRONG | 3,990,310/3,990,310 |
| Native actor_present bit decode | NO / CURRENT EVIDENCE PASS | R3.14A |
| Native bounded actor_id | NO | next contract/primitive stages |
| Native alive/new envelope | NO | planned narrow pass |
| Native new actor spawn | NO | planned |
| Native property loop | NO | planned |
| Native attribute payloads | NO | planned family by family |
| Multi-frame native decoder | NO | later |
| Actor lifecycle state table | NO | evidence policy partially known |
| Canonical raw state | NO | after native decoder |
| Semantic events | NO | target |
| Replay slices | CONTRACT/VISION, NOT NATIVE END-TO-END | historical prototype windows exist |
| Position Library | TARGET | old design preserved |
| Counterfactual engine | CONTRACT/VISION | no real RocketSim-backed production |
| Skill Forge | CONTRACT/VISION PARTIAL | structures exist, not native replay-derived end-to-end |
| Low Boost Recovery end-to-end | NO | first planned vertical slice |
| Teacher Factory end-to-end | NO | contracts/design exist |
| BC export | PARTIAL CONTRACT SURFACE | not full native replay teacher dataset |
| DAgger export | TARGET | not current full consumer loop |
| PPO auxiliary export | TARGET | not current full consumer loop |
| Runtime bridge | TARGET | offline-heavy design |
| Closed-loop refresh | TARGET | not current |
| 212k index/mass scan | TARGET | local corpus exists |
| RocketSim backend | NO CURRENT PRODUCTION | explicit future adapter |
| Player War Map | TARGET / SCOUT+MIMIR ecosystem | design only |
| Rare-skill factory | TARGET | after vertical slice maturity |

---

# 84. ESKİ ROADMAP'İ GÜNCELLEMEK

Eski roadmap'teki:

```text
R1 = 100 replay header compatibility scanner
```

artık exact next step değildir.

Çünkü current production R3.13/R3.14 seviyesine ulaşmıştır.

Yeni immediate chain:

```text
R3.14A
first actor-envelope differential evidence

R3.14B
evidence admission + bit cursor/bounded-int contract

R3.14C
bit cursor + bounded-int primitive

R3.14D
first actor envelope reader

R3.14E
47 replay differential audit

R3.15
new actor spawn

R3.16
existing actor property envelope

R3.17+
payload tag families

then:
multi actor
multi frame
actor reconstruction
raw state
events
slices
```

---

# 85. RAW STATE SONRASI KANONİK UZUN YOL

Native network decode kapandıktan sonra:

```text
P1
Actor lifecycle reconstruction

P2
Semantic entity binding
ball/car/player/game

P3
Canonical Raw State

P4
Exact decoded events

P5
Inferred tactical events

P6
Replay Slice Engine

P7
Anchor Miner

P8
Control-Onset Rewind

P9
Position Library + Benchmark baseline

P10
Low Boost Recovery real seed

P11
Canonicalization

P12
Contact/Event Graph

P13
Phase Segmentation

P14
Parameter Inference

P15
RocketSim SimBackend

P16
Counterfactual Brancher

P17
Feasibility

P18
Multi-dimensional Scorer

P19
Skill Family Synthesis

P20
Anti-targets

P21
Curriculum

P22
Teacher Factory

P23
BC export

P24
DAgger export

P25
PPO/RL auxiliary export

P26
Runtime Bridge

P27
Gabriel Rollout Ingestion

P28
Novelty/Failure Refresh

P29
Skill lifecycle

P30
Rare skill mining

P31
212k tiered mass scan

P32
Parallelism/caching

P33
Production hardening
```

---

# 86. PRODUCTION HARDENING

Gerekli:

```text
schema migration
versioning
determinism tests
property-based tests
fuzzing
malformed replay corpus
truncation tests
bit cursor diagnostics
crash recovery
resume
observability
metrics
artifact lineage
reproducible runs
backup/export
```

---

# 87. PASS PROTOCOL

Network-format alanında önerilen sürekli discipline:

```text
read-only audit
→ oracle/corpus evidence
→ policy/contract
→ narrow implementation
→ focused tests
→ corpus differential
→ clean reconstruction
→ exact publication
→ continuity update
```

Bir pass başarısızsa:

```text
expand blindly
```

yerine:

```text
classify exact failure
→ patch smallest boundary
→ rerun
```

---

# 88. POWERSHELL / CI DERSİ

Geçmiş GitHub publish sürecinde bir önemli hata yaşandı:

PowerShell wrapper native cargo argümanlarını yanlış forward ettiği için ilk green CI gerçek validation çalıştırmamıştı.

Kalıcı kural:

```text
native tool
→ explicit arguments
→ explicit $LASTEXITCODE check
→ non-zero propagated
```

Green CI:

```text
native failure propagation yoksa
```

kanıt değildir.

---

# 89. CLEAN RECONSTRUCTION / PUBLICATION

Production format work için:

```text
evidence branch
→ validate
→ production source blob
→ fresh main ancestry
→ reconstruct clean commit
→ exact diff audit
→ force-free publish
→ verify exact published SHA
```

Temporary evidence workflows production commit'e sızmamalıdır.

---

# 90. MIMIR DONE DEFINITION

MIMIR parser çalışınca bitmiş değildir.

Minimum end-to-end done:

```text
real replay
→ native decode
→ actor lifecycle
→ raw state
→ exact/inferred events
→ replay slice
→ canonicalization
→ contact graph
→ phases
→ skill seed
→ parameters
→ counterfactual variants
→ feasibility
→ scoring/ranking
→ reusable skill
→ anti-target
→ curriculum
→ teacher
→ BC/DAgger/PPO/runtime export
→ Gabriel/V1 consumer
→ new rollout
→ failure/novelty
→ refresh
→ aging/dedup/retirement
```

Ve:

```text
one low_boost_recovery vertical slice
+
one mechanically/tactically different family
+
controlled measurable gain
```

ile generality kanıtlanmalıdır.

---

# 91. "NE YAPMAYACAĞIZ?"

```text
Boxcars'ı gizli production decoder yapmayacağız.
Eski Python output'u bugünkü MIMIR capability diye sunmayacağız.
Design doc'u implementation diye sunmayacağız.
Raw state gelmeden fake semantic skill üretmeyeceğiz.
Unknown formatı guess etmeyeceğiz.
Every replay'e unlimited counterfactual compute vermeyeceğiz.
NX-HyperBot obs schema'sını MIMIR canonical schema yapmayacağız.
Gabriel Scout live probe logic'ini MIMIR core'a gömmeyeceğiz.
RocketSim'i kopyalayıp core'a yapıştırmayacağız.
Synthetic evidence'i human replay evidence gibi etiketlemeyeceğiz.
Train/test leakage'i başarı diye satmayacağız.
Low confidence teacher'a zorla label verdirmeyeceğiz.
Runtime içinde dev offline MIMIR search çalıştırmayacağız.
```

---

# 92. HISTORICAL MIGRATION CANDIDATES — PRIORITY

## H1 — RL Replay Coach V0.2 secondary structural oracle

Amaç:

```text
same replay
Python historical parser
vs
current Rust scaffold/materialization
```

Compare:

```text
header boundaries
keyframes
network size
tickmarks
packages
objects
names
class index
net cache counts
```

Bu production dependency değil, regression oracle.

## H2 — AE6DD replay parser fixture lane

2v2 olduğu için:

```text
binary format fixture
```

olarak eklenebilir.

1v1 semantic benchmark'a girmez.

## H3 — old physics JSON producer recovery

Producer reproducible olursa:

```text
historical physics oracle
```

haline gelebilir.

## H4 — V1 event coach heuristic baseline

Gelecekte:

```text
MIMIR scorer
vs
simple time-to-ball/goal-angle heuristic
```

benchmark.

## H5 — Fast384 consumer adapter

Canonical state'ten:

```text
NX/Gabriel observation
```

adapter contract.

## H6 — historical event-window UX

Replay Slice CLI/UI:

```text
event-centered window
+
user-selected exact time
+
control-onset rewind
```

üçünü birleştirmeli.

---

# 93. SOURCE INVENTORY — MIMIR ADI OLMAYAN ÖNEMLİ DOSYALAR

```text
conversations-011.json
- devasa conversation export
- replay parser research
- MIMIR explanations
- old replay extraction history
- filename-based searchte görünmez

rl_replay_analyzer_v0_2.py
- historical working structural replay analyzer

test_rl_replay_analyzer_v0_2.py
- real fixture regression tests

RL_REPLAY_COACH_V0_2_README.md
- exact historical capability boundary

run_rl_replay_coach_v0_2.ps1
- historical Windows wrapper

rl_replay_event_coach_v1_adapter.py
- heuristic state-window analysis prototype

AE6DD28411F1508AD67AA6A178296A08_v0_2.events.jsonl
- concrete event windows and questions

Naveax_replay_extracted_settings.json
- replicated settings + physics-derived output
- producer provenance unresolved
- private unique IDs intentionally omitted here

codex.txt / generic pasted Codex transcripts
- NX/Gabriel consumer behavior
- curriculum/reset examples
- observation/export lessons

gabriel_sistem_tasarimi.md
- MIMIR/Scout responsibility boundary
- Player War Map
- probe and benchmark requirements
```

---

# 94. SOURCE INVENTORY — DIRECT MIMIR MASTER FILES

```text
MIMIR_MASTER_DESIGN_SPEC_2026-08-12.md
MIMIR_MASTER_BLUEPRINT_2026-08-12.md
MIMIR_Gabriel_V1_Tam_Mimari_ve_Yol_Haritasi.md
MIMIR_DETAILED_EXECUTION_ROADMAP.md
MIMIR_TAM_PLAN_TEK_DOSYA.md
MIMIR_NEXT_CHAT_HANDOFF_FULL.md
MIMIR_NEW_CHAT_START_PROMPT.md
mimir_sistem_tasarimi.md
MIMIR_FULL_DEPENDENCY_AUDIT.txt
```

Eski current-state blokları superseded olabilir.

Design intent ve historical admission facts yine değerlidir.

---

# 95. YENİ BİR CHAT İÇİN TEK SAYFALIK CONTINUATION PROTOCOL

Yeni chat:

```text
1. GitHub Naveax/MIMIR main fetch.
2. exact main SHA kaydet.
3. MIMIR_CONTINUE_HERE.md oku.
4. docs/continuity/MIMIR_CURRENT_STATE.md oku.
5. current pass'i source/tests ile verify et.
6. in-flight branch varsa inspect et.
7. historical File Library'yi yalnız:
   - evidence
   - design
   - migration candidate
   için kullan.
8. old handoff'u current state sanma.
9. code/test source-of-truth.
10. exact first incomplete current-pass checklist'ten devam et.
```

Current continuation:

```text
R3.14A evidence
```

---

# 96. SON KANONİK ÖZET

MIMIR'in bugünkü gerçek hali:

> Header/body/footer/network prerequisites konusunda artık ciddi bir native Rust replay-ingestion temeline sahip; 47 replay üzerinde static network lookup planı pinned Boxcars oracle'ın 3,990,310 attribute update'ıyla birebir eşleştirilmiş durumda. Buna rağmen native actor/property payload bit decoder henüz production'a admit edilmedi. Şu an doğru iş R3.14A first-frame/first-actor differential evidence'dir.

MIMIR'in tarihsel gizli mirası:

> Adında MIMIR geçmeyen Mayıs 2026 RL Replay Coach V0.2 ailesinde gerçek Python header/body/footer parser'ı, replay fixture testleri, event window üretimi ve heuristic coach adapter bulunuyor. Aynı dönem ayrıca replicated settings ve physics-derived replay çıktısı üretilmiş, fakat bu physics çıktısının producer provenance'ı yeniden kanıtlanmadan current MIMIR capability veya hard oracle sayılamaz.

MIMIR'in nihai kimliği:

> Replay Intelligence + Position Library + Benchmark + Counterfactual Engine + Teacher Factory + Skill Forge + Curriculum + Memory + Confidence/Abstention + Policy/Runtime Export + Closed-Loop Refresh.

Uygulama felsefesi:

```text
Truth before capability.
Evidence before widening.
Native decode before semantic claims.
Semantic state before real skill claims.
Physics validation before teacher certainty.
Vertical slice before horizontal explosion.
Offline intelligence, online minimalism.
```

Nihai başarı ölçüsü:

```text
1 değerli gameplay anı
→ güvenilir state/evidence
→ reusable skill/teacher
→ controlled measurable gain
```

Bu zincir tekrar tekrar, farklı skill families üzerinde ve büyük corpus ölçeğinde çalışıyorsa MIMIR gerçekten olgunlaşmış sayılır.

---

## CANONICAL MULTI-STAGE CROSS-LINKS

This all-in-one synthesis is part of a multi-stage validation graph. Read and verify it against:

- [Primary execution/continuity handbook](MIMIR_CONTINUE_HERE.md)
- [Knowledge graph](MIMIR_KNOWLEDGE_GRAPH.md)
- [ChatGPT archive source registry](docs/chatgpt-archive/SOURCE_REGISTRY.md)
- [Cross-source validation matrix](docs/chatgpt-archive/VALIDATION_MATRIX.md)
- [Historical-to-current migration map](docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md)
- [Archive manifest](docs/chatgpt-archive/MANIFEST.json)
- [Archive verifier](scripts/verify_mimir_knowledge_archive.ps1)

Current GitHub source/tests remain higher authority than historical snapshots when they conflict.


---

## CURRENT REPLAY DECODER ADMISSION UPDATE — R3.14A/B

As of 2026-08-13, current GitHub/evidence truth adds this admission chain:

```text
R3.13 production static network lookup plan
→ R3.14 read-only bitstream order audit
→ R3.14A Outcome A: 47/47 pinned-oracle first-envelope evidence
→ R3.14B admitted native bit-cursor / bounded-int contract
→ ACTIVE: R3.14C private primitive implementation
```

Durable current artifacts:

- `docs/continuity/MIMIR_R3_14A_DECISION.md`
- `docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md`
- `docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md`

Production replay capability still stops at R3.13 until R3.14C is implemented, audited and published. R3.14A/B evidence and contracts are not themselves native actor-envelope parsing.
