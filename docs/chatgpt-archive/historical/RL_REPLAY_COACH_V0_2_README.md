# RL Replay Coach V0.2

Bu paket Rocket League `.replay` dosyasından header + footer seviyesinde koçluk ön-raporu üretir.

## Ne çıkarır?

- Maç meta bilgisi: map, tarih, skor, frame sayısı, FPS
- Oyuncu scoreboard'u: gol/asist/save/şut/puan
- Gol zaman çizelgesi
- Tick mark eşleşmeleri: Team0Goal, Team1Save vb.
- Gol dışı highlight adayları
- V1 için analiz pencereleri: her kritik olay için `[-5s,+2s]`
- Body/footer parse: keyframes, network stream hash/uzunluk, packages, object/name/class tabloları

## Ne çıkarmaz?

V0.2 gerçek network-frame/physics decode yapmaz. Bu yüzden şunlar henüz yoktur:

- Araba/top koordinatı
- Boost miktarı
- Rotation/velocity
- Jump/dodge/input
- Time-to-ball
- Gerçek whiff/miss sebebi

Bunlar için V1 aşamasında network stream parser gerekir.

## Kullanım

```powershell
py .\rl_replay_analyzer_v0_2.py "C:\path\match.replay" --player Naveax --out-prefix "C:\path\out\match_v0_2" --zip
```

Linux/WSL:

```bash
python3 ./rl_replay_analyzer_v0_2.py ./match.replay --player Naveax --out-prefix ./match_v0_2 --zip
```

## Üretilen dosyalar

- `.coach_summary.md` kısa koçluk özeti
- `.report.md` tam rapor
- `.analysis.json` ana analiz JSON'u
- `.events.jsonl` V1'e verilecek kompakt olay pencereleri
- `.body_footer.json` body/footer parse çıktısı
- `.parsed_header.json` header/property çıktısı

## Test

Bu fixture ile doğrulama:

```bash
python3 ./test_rl_replay_analyzer_v0_2.py
```

Beklenen:

```text
PASS test_body_footer_sections
PASS test_event_windows_priority
PASS test_header_core_fields
PASS test_players_and_goals
```
