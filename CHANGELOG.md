# Changelog

All notable changes to the AADP book repository (tooling, structure, and publishing) are documented in this file. The specification content itself is versioned separately (see [VERSION](VERSION) and the document header in the chapters).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- Repository structure: `docs/`, `chapters/`, `diagrams/`, `images/`, `scripts/`.
- Portable `scripts/split_to_chapters.py` with CLI source path (default: `full-specification.txt` in repo root).
- MdBook setup: `book.toml`, `src/SUMMARY.md`, `scripts/prepare_mdbook.sh` and `scripts/prepare_mdbook.ps1`.
- Mermaid support via optional `mdbook-mermaid` preprocessor; high-level architecture diagram in Chapter 4 converted to Mermaid; `diagrams/high-level-architecture.mmd` added.
- GitHub Actions workflow `.github/workflows/build-book.yml`: build on push, publish to GitHub Pages.
- `VERSION` file (v1.0), `LICENSE` (MIT), `CONTRIBUTING.md`, `CHANGELOG.md`.
- README updated with repository structure, rebuild chapters, build book, and local preview instructions.

### Changed

- `split_to_chapters.py` moved from repo root to `scripts/`.
- Chapter 4 ASCII architecture diagram replaced with Mermaid flowchart.

### Fixed

- (None yet)

---

## [1.0] — 2026-03-04

- Initial manuscript: full specification split into 31 chapters, single-file `full-specification.md`, index and references.

[Unreleased]: https://github.com/your-org/aadp-book/compare/v1.0...HEAD
[1.0]: https://github.com/your-org/aadp-book/releases/tag/v1.0
