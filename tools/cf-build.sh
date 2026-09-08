#!/usr/bin/env bash
# Cloudflare build step. Assembles dist/ from an explicit allowlist.
#
# Why an allowlist and not .assetsignore: .assetsignore was tested here and did
# not filter (331 files read without it, 332 with). Pointing Cloudflare at the
# repo root would therefore have published .git — the entire repository history,
# publicly downloadable. Naming the files means nothing can leak by accident;
# a new asset simply has to be added below.
set -euo pipefail

SITE_FILES=(
  index.html
  privacy.html
  terms.html
  thank-you.html
  robots.txt
  sitemap.xml
  three.min.js
  manzil-mark.png
  favicon-64.png
  favicon-180.png
  favicon-512.png
  social-card.png
)

rm -rf dist
mkdir -p dist
for f in "${SITE_FILES[@]}"; do
  [[ -f "$f" ]] || { echo "cf-build: missing $f" >&2; exit 1; }
  cp "$f" dist/
done

echo "cf-build: staged ${#SITE_FILES[@]} files"
ls -1 dist
