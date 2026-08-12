# Checked-in Replay Test Corpus

MIMIR keeps two classes of real replay fixtures:

1. `external_fixtures/`
   - historically admitted parser fixtures
   - preserve their existing identities and evidence chain

2. `test_corpus/largest_100/`
   - 100 largest SHA-256-unique replay files selected from the local RLCS 1v1 corpus
   - intended for broad regression/stress coverage
   - selected by file size, not by gameplay quality or semantic diversity

File size is only a stress-selection heuristic. It does not prove that a replay contains more useful gameplay information.

Every selected replay is recorded in `manifest.jsonl` with size and SHA-256 so the corpus can be reproduced and integrity-checked.

These files are test fixtures, not the production training corpus.