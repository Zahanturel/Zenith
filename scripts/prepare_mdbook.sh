#!/usr/bin/env bash
# Prepare mdBook src/ by copying index.md and chapters/*.md into src/.
# Run this before 'mdbook build' or 'mdbook serve'.
set -e
BOOK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="${BOOK_ROOT}/src"
CHAPTERS_DIR="${BOOK_ROOT}/chapters"

mkdir -p "$SRC_DIR"

# Copy index.md and fix links for mdBook (chapters/XX -> XX)
if [[ -f "${BOOK_ROOT}/index.md" ]]; then
  sed 's|\](chapters/|\](|g' "${BOOK_ROOT}/index.md" > "${SRC_DIR}/index.md"
  echo "Wrote ${SRC_DIR}/index.md"
fi

# Copy references.md if present (so intro can link to it)
if [[ -f "${BOOK_ROOT}/references.md" ]]; then
  cp "${BOOK_ROOT}/references.md" "${SRC_DIR}/references.md"
  echo "Wrote ${SRC_DIR}/references.md"
fi

# Copy full-specification.md if present (single-file version for built book)
if [[ -f "${BOOK_ROOT}/full-specification.md" ]]; then
  cp "${BOOK_ROOT}/full-specification.md" "${SRC_DIR}/full-specification.md"
  echo "Wrote ${SRC_DIR}/full-specification.md"
fi

# Copy all chapter markdown files
for f in "${CHAPTERS_DIR}"/*.md; do
  if [[ -f "$f" ]]; then
    cp "$f" "${SRC_DIR}/"
    echo "Wrote ${SRC_DIR}/$(basename "$f")"
  fi
done

echo "Done. Run 'mdbook build' or 'mdbook serve' from the repo root."
