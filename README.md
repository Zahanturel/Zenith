# AI Autonomous Development Platform — System Design Specification (Book)

This repository contains the **AI Autonomous Development Platform (AADP) System Design Specification** as a book manuscript with build tooling, diagram support, and CI for publishing.

**Version:** See [VERSION](VERSION) (v1.0)  
**Authors:** Zahan Turel, Zenith  
**Status:** Final — Ready for implementation  
**License:** [MIT](LICENSE)

---

## Repository structure

```
aadp-book/
├── book.toml              # MdBook configuration
├── index.md               # Introduction and table of contents (source)
├── full-specification.md  # Single-file version of the full spec
├── references.md          # References and further reading
├── book-frontmatter/      # Title page, preface (copied to src/)
├── theme/                 # Custom CSS and Pandoc header for PDF
├── VERSION                # Book version (e.g. v1.0)
├── README.md              # This file
├── LICENSE                # MIT
├── CONTRIBUTING.md        # How to contribute (tooling/docs only)
├── CHANGELOG.md           # Tooling and repo changes
├── book.yml               # Legacy/book metadata (chapter list)
│
├── src/                   # MdBook source (generated; do not edit by hand)
│   └── SUMMARY.md         # Chapter order for mdBook (only file committed here)
│
├── chapters/              # 31 chapter Markdown files (00–30)
│   ├── 00-terminology-and-front-matter.md
│   ├── 01-executive-overview.md
│   └── ... 30-appendix-a.md
│
├── diagrams/              # Mermaid and other diagram sources
│   └── high-level-architecture.mmd
│
├── images/                # Images (screenshots, figures)
│
├── docs/                  # Reserved for additional documentation
│
└── scripts/               # Build and maintenance scripts
    ├── split_to_chapters.py   # Regenerate chapters + full-spec from .txt
    ├── prepare_mdbook.sh      # Copy index + chapters + front matter into src/ (Unix)
    └── prepare_mdbook.ps1     # Same for Windows
```

---

## How to read the book

- **Single file:** Open [full-specification.md](full-specification.md) for the complete spec in one Markdown file.
- **By chapter:** Start with [index.md](index.md) for the table of contents and links to every chapter.
- **Built book:** After building with mdBook (see below), open the generated HTML in `book/` or use `mdbook serve` for a local preview.

The **Terminology Glossary** is in [chapters/00-terminology-and-front-matter.md](chapters/00-terminology-and-front-matter.md). Chapters 01–29 map to Sections 1–29 of the original specification; Chapter 30 is Appendix A.

---

## Rebuilding chapters from source

If you have the original specification as a single `.txt` file, you can regenerate `full-specification.md` and all files in `chapters/` using the split script.

**Usage:**

```bash
# Use default source: full-specification.txt in the repo root
python scripts/split_to_chapters.py

# Or pass a custom source file path
python scripts/split_to_chapters.py path/to/source.txt
```

The script writes:

1. **full-specification.md** in the repo root (full content as Markdown).
2. All chapter files in **chapters/** (00 through 30).

If `full-specification.txt` is not present, place your source `.txt` in the repo root or pass its path as the first argument.

---

## Building the book

**Website (HTML)**

```bash
# Prepare source (copy index, chapters, front matter into src/)
bash scripts/prepare_mdbook.sh   # or ./scripts/prepare_mdbook.ps1 on Windows
mdbook build
```

Output is in the **book/** directory. Open `book/index.html` in a browser or use `mdbook serve` for live preview.

**PDF (printable book)**

After building the website, generate a PDF with [mdbook-pandoc](https://github.com/max-heller/mdbook-pandoc):

```bash
mdbook build
mdbook-pandoc book
```

The PDF is written to **book/pandoc/pdf/AI-Autonomous-Development-Platform.pdf** (or **book/** when only the pandoc renderer is used). You need [Pandoc](https://pandoc.org/) and a LaTeX engine (e.g. [TeX Live](https://www.tug.org/texlive/)) installed. Install the renderer with:

```bash
cargo install mdbook-pandoc
```

If you use the browser’s **Print → Save as PDF** on the built HTML instead, open the print dialog, go to **More settings**, and turn **off** “Headers and footers” so the browser does not add date, URL, or title in the margins.

---

## Installation and build details

The book is built with [mdBook](https://rust-lang.github.io/mdBook/). You need **Rust/Cargo** installed to run mdBook.

**Install mdBook and optional tools:**

```bash
cargo install mdbook
cargo install mdbook-mermaid   # optional, for Mermaid diagrams
cargo install mdbook-pandoc   # optional, for PDF output
```

The prepare step copies `index.md`, `full-specification.md`, `references.md`, `book-frontmatter/*.md`, and `chapters/*.md` into `src/`. You must run it before building after any change to those source files.

---

## Previewing locally

To serve the book locally with live reload:

```bash
# Prepare and then serve (prepare only needed once per change to chapters/index)
bash scripts/prepare_mdbook.sh
mdbook serve
```

Then open **http://localhost:3000** in your browser. Edits to files in `src/` (after re-running the prepare script if you changed `chapters/` or `index.md`) will trigger a rebuild.

---

## CI and GitHub Pages

The repository includes a GitHub Actions workflow that:

- Runs on every push to `main` or `master`
- Installs mdBook and mdbook-mermaid
- Prepares the book source and runs `mdbook build`
- Publishes the generated **book/** directory to **GitHub Pages**

To enable the published site:

1. In your GitHub repo: **Settings → Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Push to `main` (or `master`); the workflow will build and deploy the book

The site URL will be `https://<username>.github.io/<repo>/` (or your custom domain if configured).

---

## Book tooling summary

| Tool        | Purpose |
|------------|---------|
| **mdBook** | Build the book to HTML; use `mdbook build` and `mdbook serve`. |
| **book.yml** | Chapter list for reference; compatible with GitBook/MkDocs if you switch later. |
| **scripts/split_to_chapters.py** | Regenerate chapters and full-spec from a single `.txt` source. |
| **scripts/prepare_mdbook.\*** | Copy `index.md` and `chapters/*.md` into `src/` before building. |

---

*AI Autonomous Development Platform — System Design Specification — Version 1.0*
