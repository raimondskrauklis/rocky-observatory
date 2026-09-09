#!/usr/bin/env bash
# .cursor/skills/md-docx-export/scripts/export_md_to_docx.sh
# Export one or more .md files to compact .docx (9pt body, narrow margins).
# Mermaid fences are rendered to PNG and embedded (mmdc, else mermaid.ink).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_ASSETS="${SKILL_DIR}/assets"
REF_DOC="${SKILL_ASSETS}/kp-compact-reference.docx"
RENDER="${SKILL_DIR}/scripts/render_mermaid_for_docx.py"
PANDOC="${PANDOC:-}"

if [[ -z "$PANDOC" ]]; then
  if [[ -x /tmp/pandoc-arm64/pandoc-3.6.4-arm64/bin/pandoc ]]; then
    PANDOC=/tmp/pandoc-arm64/pandoc-3.6.4-arm64/bin/pandoc
  elif command -v pandoc >/dev/null 2>&1; then
    PANDOC="$(command -v pandoc)"
  else
    echo "ERROR: pandoc not found. Set PANDOC= or install pandoc." >&2
    exit 1
  fi
fi

if [[ ! -f "$REF_DOC" ]]; then
  echo "Building reference docx..." >&2
  (cd "$ROOT/backend" && pipenv run python "$ROOT/.cursor/skills/md-docx-export/scripts/build_reference_docx.py")
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 path/to/doc.md [more.md ...]" >&2
  exit 1
fi

PYTHON="${PYTHON:-python3}"

CLEANUP_DIRS=()
cleanup() { rm -rf "${CLEANUP_DIRS[@]:-}"; }
trap cleanup EXIT

for MD in "$@"; do
  if [[ ! -f "$MD" ]]; then
    echo "ERROR: not found: $MD" >&2
    exit 1
  fi
  OUT="${MD%.md}.docx"
  WORK="$(mktemp -d "${TMPDIR:-/tmp}/kp-md-docx.XXXXXX")"
  CLEANUP_DIRS+=("$WORK")
  BODY="${WORK}/body.md"
  IMG="${WORK}/img"

  echo "Preparing $MD ..." >&2
  "$PYTHON" "$RENDER" "$MD" "$BODY" "$IMG"

  "$PANDOC" "$BODY" \
    --from=markdown \
    --to=docx \
    --resource-path="${WORK}:${IMG}:$(dirname "$MD")" \
    --reference-doc="$REF_DOC" \
    -o "$OUT"

  echo "Wrote $OUT"
  rm -rf "$WORK"
done
