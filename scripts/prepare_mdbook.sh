#!/usr/bin/env bash
# Prepare mdBook src/ so it works for both:
# - New layout: content already in src/ (script no-ops).
# - Old layout: index.md, chapters/, book-frontmatter/ at repo root (copy into src/).
set -e
BOOK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="${BOOK_ROOT}/src"
CHAPTERS_DIR="${BOOK_ROOT}/chapters"
FRONTMATTER_DIR="${BOOK_ROOT}/book-frontmatter"

mkdir -p "$SRC_DIR"
mkdir -p "${SRC_DIR}/book-frontmatter"
mkdir -p "${SRC_DIR}/chapters"

# Copy index.md from root if present (old layout)
if [[ -f "${BOOK_ROOT}/index.md" ]]; then
  sed 's|\](chapters/|\](|g' "${BOOK_ROOT}/index.md" > "${SRC_DIR}/index.md"
  echo "Wrote ${SRC_DIR}/index.md"
fi

# Copy references.md from root if present
if [[ -f "${BOOK_ROOT}/references.md" ]]; then
  cp "${BOOK_ROOT}/references.md" "${SRC_DIR}/references.md"
  echo "Wrote ${SRC_DIR}/references.md"
fi

# Copy full-specification.md from root if present
if [[ -f "${BOOK_ROOT}/full-specification.md" ]]; then
  cp "${BOOK_ROOT}/full-specification.md" "${SRC_DIR}/full-specification.md"
  echo "Wrote ${SRC_DIR}/full-specification.md"
fi

# Copy book front matter into src/book-frontmatter/ (matches SUMMARY paths)
if [[ -d "${FRONTMATTER_DIR}" ]]; then
  for f in "${FRONTMATTER_DIR}"/*.md; do
    if [[ -f "$f" ]]; then
      cp "$f" "${SRC_DIR}/book-frontmatter/"
      echo "Wrote ${SRC_DIR}/book-frontmatter/$(basename "$f")"
    fi
  done
fi

# Copy chapters into src/chapters/ (matches SUMMARY paths)
if [[ -d "${CHAPTERS_DIR}" ]]; then
  for f in "${CHAPTERS_DIR}"/*.md; do
    if [[ -f "$f" ]]; then
      cp "$f" "${SRC_DIR}/chapters/"
      echo "Wrote ${SRC_DIR}/chapters/$(basename "$f")"
    fi
  done
fi

echo "Done. Run 'mdbook build' or 'mdbook serve' from the repo root."
