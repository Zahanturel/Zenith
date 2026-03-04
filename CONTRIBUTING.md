# Contributing to the AADP Book

Thank you for your interest in the AI Autonomous Development Platform (AADP) System Design Specification repository.

## Scope of contributions

This repository focuses on **tooling, structure, and publishing** for the book. Acceptable contributions include:

- **Build and CI**: mdBook configuration, scripts, GitHub Actions
- **Documentation**: README, CONTRIBUTING, CHANGELOG, and other repo docs
- **Diagrams and assets**: Mermaid diagrams in `diagrams/`, images in `images/`
- **Fixes**: Typos, broken links, or formatting in the manuscript that do not change architectural content

Please **do not** submit changes that alter the **architecture specification content** (the technical design, system layers, data models, etc.) unless you are a maintainer or have explicit agreement. The specification text is considered final for v1.0.

## How to contribute

1. **Fork the repository** and create a branch from `main` (or `master`).
2. **Make your changes** only in the areas listed above.
3. **Test locally**:
   - Run `bash scripts/prepare_mdbook.sh` (or `scripts/prepare_mdbook.ps1` on Windows).
   - Run `mdbook serve` and confirm the book builds and looks correct.
4. **Commit** with a clear message and open a **Pull Request**.

## Development setup

- **Python 3**: Required for `scripts/split_to_chapters.py`.
- **Rust / Cargo**: Required to install and run mdBook (and optionally `mdbook-mermaid`).
- Install mdBook: `cargo install mdbook`
- Optional (for Mermaid diagrams): `cargo install mdbook-mermaid`

See [README.md](README.md) for full build and preview instructions.

## Code of conduct

Be respectful and constructive. This project follows a standard code of conduct; harassment or off-topic content is not welcome.

---

*AI Autonomous Development Platform — System Design Specification*
