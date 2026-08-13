# MIMIR Continuity Control Plane

Bu klasör MIMIR'in **güncel devam kontrol katmanıdır**. Tarihsel `docs/` ve `executor_*` dosyaları silinmez; ancak yeni bir ChatGPT/Codex oturumu mevcut kilometre taşını seçmek için önce bu klasörü kullanır.

## Neden var?

MIMIR repo'sunda çok fazla historical planning/admission/implementation artifact vardır. Bu güçlü bir audit trail sağlar, fakat yeni bir oturum en eski uygun-looking `next.txt` dosyasını seçerse tamamlanmış işi tekrar yapabilir. Continuity control plane bunun için tek bir canonical resume surface sağlar.

## Canonical files

### `MIMIR_CONTINUITY_STATE.json`
Machine-readable durum özeti. Yeni chat bunu ilk teknik state kaynağı olarak okumalıdır.

### `MIMIR_CURRENT_STATE.md`
İnsan tarafından okunabilir güncel production state, evidence ve açık/kapalı sınırlar.

### `MIMIR_R3_14A_EXECUTION_SPEC.md`
Şu anda yapılacak exact pass. Bu dosya tamamlandığında bir sonraki exact-pass spec ile değiştirilir veya yeni spec eklenir ve `MIMIR_CONTINUE_HERE.md` pointer'ı güncellenir.

### `MIMIR_PASS_PROTOCOL.md`
Her pass için değişmez çalışma protokolü: re-audit, evidence, implementation isolation, fail-fast CI, clean reconstruction, exact-SHA validation, force-free publication ve continuity sync.

### `MIMIR_BOUNDARY_LOCKS.md`
Açık/kapalı capability sınırları ve bunların reopen koşulları.

### `MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
R3.14A'dan full MIMIR hedef mimarisine kadar uzun vadeli sıra.

### `MIMIR_PROGRESS_LEDGER.md`
Append-only milestone günlüğü. Her production pass sonunda yeni kayıt eklenir; eski kayıtlar rewrite edilmez.

### `MIMIR_NEXT_CHAT_HANDOFF.md`
Yeni ChatGPT konuşmasına kopyalanabilecek hazır continuation promptu.

## Source-of-truth hierarchy

```text
fresh repo code/tests
> exact-SHA CI/evidence
> continuity JSON
> current-state markdown
> active pass spec
> boundary locks
> roadmap
> progress ledger
> historical docs/executor artifacts
> old chat memory
```

## Continuity update policy

Her production milestone tamamlandığında:

1. production commit yayınlanır ve exact-main CI/readback tamamlanır;
2. sonra docs-only continuity sync yapılır;
3. JSON ve markdown state aynı production SHA'yı göstermelidir;
4. progress ledger'a append edilir;
5. next-pass pointer değiştirilir;
6. completed pass tekrar `next` olarak kalmamalıdır.

## Historical docs policy

Historical docs:

- silinmez,
- kanıt olarak değerlidir,
- ancak güncel capability claim'i için tek başına yeterli değildir,
- `docs/continuity/` ile çelişirse fresh repo truth araştırılır.

## Safety / truthfulness rule

Bir layer'ın evidence'i başka layer'ın implementation'ı değildir.

Örnek:

```text
Boxcars oracle decoded actor envelope
!=
MIMIR native actor-envelope parser implemented
```

Aynı şekilde:

```text
static network lookup plan exists
!=
network payload bits decoded
```

Bu ayrım continuity dokümanlarında özellikle korunur.
