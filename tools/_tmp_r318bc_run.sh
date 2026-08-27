#!/usr/bin/env bash
set -euo pipefail

WORK="${RUNNER_TEMP:-/tmp}/r318bc-bootstrap"
ENCODED="$WORK/r318bc-inner.b64"
INNER="$WORK/r318bc-inner.sh"
rm -rf "$WORK"
mkdir -p "$WORK"
: > "$ENCODED"

CHUNKS=(
  17cc7c63b14ac860ec05ab44c54b03ab7936155a
  d37b41b3f144439c02969fd1fc5cceb786531b6e
  cc6404620fc4af4a10a8b317c1324a8b7b327658
  7447d636ecf8a446432ce8255c23a052f4919207
  986b0c3ef4b3a0881c9b3578e7d9e31dae7f19ff
  3f04863060e32dd8c95ae97c4b0a5af6e5546b29
  c4503f167d11be79afce18fa4168697a8959e265
  31a688dbb391b7dbd0c442377c9285b4157c6065
  791d72084d03d07a02993c4996a41d83fcd74da5
  40644127e18a356e4aa957e8b3a6898ce5d528dc
  1d777112a15c54bb114a7599fdb85adcdeb30c6d
  206ac6fe5048844a48b416d3478f7668ad399b5f
  3cdab4a5567e96e9ffe45e1504a76a239c0b7123
  e3e9858c66e129f043cbd286769828c3cfca5edd
  540a3dccfad3e69fecb2c190e8ccae8a422b3c30
  f2cae4460ccc9e6b2770f38279b26f1a65e6b04f
  c15ff2e2703c99868458afd914b46c23c6b83bf7
  39ad02e810aea651f4d2161c822290bd45548e45
  0021fcc177a1d17e9c881f05376b19e67f6b9b70
  cd6e191afc3cb459107853130b1e793deb2e7f78
  a94796e462227fdd38cebda57db5cf4c03d8ec8e
  116c0a643e5f7e2b32c39601f91c2fa69ddce078
  d92e9f7fd93a564b1cbd589dbb352e0fcb340e45
  4b8e1d1585a41bfc32607453423bdb41dbbab933
  4f8a69d7ab84a7025045f21263d38eee5f76fedb
  5c388a6d4af3c93142f3b365a675d6124b122734
  aded5855e3eba01424798af2ff72f0c25b0e6c58
  9745b9322470e293a26775eacba0531e800cb0d3
  a556ad6bae18ba5d82a878297223a6bfc338c6bd
  af44f0d10936111a722c1a66d40612de61c9421c
  dfbf9a2214141881b8add0e2a4e3b57f246111f4
  227caa46e58cd3fd7b7dfa1ccc43c9a95a8f5004
)

for sha in "${CHUNKS[@]}"; do
  json="$(gh api "repos/${GITHUB_REPOSITORY}/git/blobs/${sha}")"
  test "$(jq -r '.sha' <<<"$json")" = "$sha"
  test "$(jq -r '.encoding' <<<"$json")" = base64
  printf '%s' "$(jq -r '.content' <<<"$json" | tr -d '\n')" | base64 -d >> "$ENCODED"
done

encoded_sha="$(sha256sum "$ENCODED" | awk '{print $1}')"
echo "R3_18BC_BOOTSTRAP_ENCODED_SHA256=${encoded_sha}"
test "$encoded_sha" = "724656537e1a1088e85c5a28f7b1bc65318a080293411ff36075b189e088d758"
base64 -d "$ENCODED" | gzip -dc > "$INNER"
inner_sha="$(sha256sum "$INNER" | awk '{print $1}')"
echo "R3_18BC_BOOTSTRAP_INNER_SHA256=${inner_sha}"
test "$inner_sha" = "4fc82c7e6901053641d3ea9dc75d74d0d33bd8316c52b3fd43a9139b5d9f6953"
bash -n "$INNER"
chmod +x "$INNER"
echo "R3_18BC_RUNNER_BOOTSTRAP=PASS chunks=32 encoded_sha256=${encoded_sha} inner_sha256=${inner_sha}"
exec "$INNER"
