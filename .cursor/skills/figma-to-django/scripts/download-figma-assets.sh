#!/usr/bin/env bash
# Download Figma MCP asset URLs into website/static/images/<section>/
# Usage: ./scripts/download-figma-assets.sh <section-name> <url1> [url2] ...
#
# Example:
#   ./scripts/download-figma-assets.sh about \
#     "https://www.figma.com/api/mcp/asset/abc..." \
#     "https://www.figma.com/api/mcp/asset/def..."

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <section-name> <asset-url> [asset-url...]" >&2
  exit 1
fi

SECTION="$1"
shift
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
DEST="${ROOT}/website/static/images/${SECTION}"
mkdir -p "$DEST"

i=1
for url in "$@"; do
  out="${DEST}/asset-$(printf '%02d' "$i")"
  curl -sL "$url" -o "${out}"
  # Detect type and add extension
  mime=$(file -b --mime-type "$out")
  case "$mime" in
    image/jpeg) mv "$out" "${out}.jpg" ;;
    image/png)  mv "$out" "${out}.png" ;;
    image/svg+xml) mv "$out" "${out}.svg" ;;
    image/webp) mv "$out" "${out}.webp" ;;
    *) echo "asset-$(printf '%02d' "$i"): unknown type $mime" ;;
  esac
  echo "Saved: ${DEST}/asset-$(printf '%02d' "$i").*"
  i=$((i + 1))
done

echo "Done. Files in ${DEST}:"
ls -la "$DEST"
