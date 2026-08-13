# MIMIR — Next Chat Handoff

Bu dosyadaki prompt yeni bir ChatGPT/Codex konuşmasına doğrudan verilebilir.

---

# Copy/paste prompt

```text
MIMIR projesine mevcut GitHub gerçeğinden devam ediyoruz.

Repository:
Naveax/MIMIR

ÖNEMLİ:
Önceki chat hafızasına veya eski executor_next dosyalarına güvenerek başlamayacaksın. Önce fresh GitHub main'i okuyacaksın.

İlk zorunlu okuma sırası:
1. MIMIR_CONTINUE_HERE.md
2. docs/continuity/MIMIR_CONTINUITY_STATE.json
3. docs/continuity/MIMIR_CURRENT_STATE.md
4. docs/continuity/MIMIR_R3_14A_EXECUTION_SPEC.md
5. docs/continuity/MIMIR_PASS_PROTOCOL.md
6. docs/continuity/MIMIR_BOUNDARY_LOCKS.md
7. docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md
8. docs/continuity/MIMIR_PROGRESS_LEDGER.md

Son production code checkpoint continuity'ye göre:
ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
R3.13 — static replay network lookup plan.

Continuity dokümanları production commit'ten sonra docs-only commitler oluşturmuş olabilir. Bu yüzden main SHA'nın ee23... olmaması tek başına drift değildir. Latest commits'i inspect et. Eğer ee23... sonrasında yalnız continuity docs değişmişse R3.13 production base'i geçerlidir. Eğer Rust/production code değişmişse continuity'yi repo gerçeğinden re-audit etmeden R3.14A'ya başlama.

R3.13 continuity facts:
- current supported replay lane: 47 replay
- static object_lookups/inherited stream maps/max_prop_id/prop_id_bits/spawn trajectory table/channel-build flags production'da
- network payload bits R3.13 katmanında okunmuyor
- pinned Boxcars differential attribute updates: 3,990,310 / 3,990,310 matched
- unresolved_stream=0
- property_object_mismatch=0
- decoded_not_implemented_hits=0

Actor lifecycle anti-regression:
- same actor ID için tekrar NewActor normal olabilir
- same-class overwrite observed: 141,511
- class-changing overwrite observed: 0
- duplicate actor ID tek başına malformed DEĞİL

R3.14 read-only format order:
frame:
  f32 time
  f32 delta
  actor_present bit
  if actor_present:
      bounded actor_id
      alive bit
      if !alive: delete
      if alive:
          new bit
          if new:
              version-gated name_id
              1 bit
              object_id
              spawn trajectory
          else:
              property_present loop
              bounded stream_id
              attribute payload

Çok önemli bounded integer kuralı:
Actor ID ve stream ID normal sabit-bit integer değildir. Low bits sonrası bound/value durumuna göre ekstra discriminator bit tüketilebilir. read_bits(width) diyerek geçme.

ŞU AN YAPILACAK EXACT PASS:
R3.14A

PASS TYPE:
evidence-only, production Rust değişikliği YOK.

GOAL:
Zaten pinned olan Boxcars revision'ını temporary instrument ederek mevcut 47 supported replay'in tamamında ilk frame + ilk actor envelope header differential evidence üret.

Evidence fields:
- first frame time
- first frame delta
- actor_present
- actor_id if present
- alive if present
- new if alive
- exact bit offsets / cursor positions
- actor_id bounded integer için bound/start/end/bits consumed ve mümkünse discriminator davranışı

HARD STOP:
- name_id OKUMA YOK
- post-name_id one-bit field YOK
- object_id YOK
- spawn payload YOK
- property_present loop YOK
- stream_id YOK
- attribute payload YOK
- second actor YOK
- second frame YOK
- raw-state YOK

Oracle rule:
- latest Boxcars kullanma
- repo/evidence history'den exact pinned SHA'yı kanıtla
- pin bulunamazsa Outcome B/BLOCKED: ORACLE_PIN_NOT_PROVEN
- production dependency ekleme
- instrumentation observation-only olsun

Process rules:
- fresh main audit
- exact corpus identity
- all native commands fail-fast
- PowerShell kullanıyorsan her cargo/git/python/oracle command sonrası LASTEXITCODE kontrol et
- temporary workflows/scripts clean production commit'e girmeyecek
- R3.14A production code değiştirmeyecek
- evidence ve implementation claim'lerini karıştırma

R3.14A Outcome A olursa sıradaki pass R3.14B:
evidence admission + native bit cursor/bounded integer contract planning.

R3.14A'dan direkt full actor/frame decoder'a geçme.

İlk cevapta bana sadece şunları ver:
1. fresh main SHA
2. ee23... sonrası production-code drift var mı
3. continuity state ile repo truth uyuşuyor mu
4. exact pinned Boxcars SHA bulundu mu
5. 47 supported replay corpus kimliği nasıl seçiliyor
6. R3.14A'ya başlamaya engel var mı

Sonra aynı konuşmada engel yoksa R3.14A'yı GitHub üzerinde yapmaya başla.
```

---

# Handoff interpretation notes

Yeni chat yukarıdaki promptu aldıktan sonra kullanıcıdan tekrar “repo hangisi?” diye sormamalıdır. Repository açıkça `Naveax/MIMIR`.

Yeni chat şu eski işleri tekrar yapmamalıdır:

```text
fixture_003 BoolProperty implementation
three-fixture header closure
source materialization planning
body boundary discovery
footer scaffold discovery
raw footer lookup materialization
static network tag registry
R3.13 static lookup plan
```

Bunlar tarihsel olarak kapanmış katmanlardır.

Yeni chat ayrıca eski handoff dosyalarında “body/network parsing unimplemented” gibi genel ifadeler görürse bunları güncel state yerine kullanmamalıdır. R3.13'e kadar structural/body/footer/static-network katmanları açılmıştır; native actor payload bit decode ise hâlâ kapalıdır.

---

# If continuity is stale

Fresh repo main continuity dosyalarından daha ilerideyse:

1. newest production code commit'lerini inspect et;
2. CI/evidence'i inspect et;
3. current source/tests üzerinden gerçek active boundary'yi çıkar;
4. continuity docs'a correction sync yap;
5. ancak sonra yeni iş yap.

Do not roll repo backward to match docs.

---

# If the chat is asked to “continue” without more context

Default behavior:

```text
fetch main
→ read continuity control plane
→ verify active pass
→ execute active pass
```

No clarification is needed unless repository access itself fails or repository truth contains an irreducible contradiction.
