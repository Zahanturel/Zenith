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
├── book.yml               # Legacy/book metadata (chapter list)
├── theme/                 # Custom CSS and Pandoc header for PDF
├── VERSION                # Book version (e.g. v1.0)
├── README.md              # This file
├── LICENSE                # MIT
├── CONTRIBUTING.md        # How to contribute (tooling/docs only)
├── CHANGELOG.md           # Tooling and repo changes
│
├── src/                   # MdBook source (standard layout)
│   ├── SUMMARY.md         # Chapter order for mdBook
│   ├── index.md           # Introduction and table of contents
│   ├── full-specification.md
│   ├── references.md
│   ├── book-frontmatter/  # Title page, preface
│   └── chapters/          # 31 chapter Markdown files (00–30)
│
├── diagrams/              # Mermaid and other diagram sources
├── images/                # Images (screenshots, figures)
├── docs/                  # Reserved for additional documentation
└── scripts/               # Build and maintenance scripts
```

---

## How to read the book

- **Single file:** Open [full-specification.md](src/full-specification.md) for the complete spec in one Markdown file.
- **By chapter:** Start with [index.md](src/index.md) for the table of contents and links to every chapter.
- **Built book:** After building with mdBook (see below), open the generated HTML in `book/` or use `mdbook serve` for a local preview.

The **Terminology Glossary** is in [src/chapters/00-terminology-and-front-matter.md](src/chapters/00-terminology-and-front-matter.md). Chapters 01–29 map to Sections 1–29 of the original specification; Chapter 30 is Appendix A.

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

Book source lives in **src/** (SUMMARY.md, index.md, chapters/, etc.). Run `mdbook build` from the repo root.

---

## Previewing locally

To serve the book locally with live reload:

```bash
mdbook serve
```

Then open **http://localhost:3000** in your browser. Edits to files in **src/** will trigger a rebuild.

---

## CI and GitHub Pages

The repository uses a GitHub Actions workflow that builds the book and deploys it to **GitHub Pages** on every push to `main` or `master`.

### Enable the live site (required — fixes 404)

If the workflow shows a green check but **https://&lt;username&gt;.github.io/&lt;repo&gt;/** returns **404**, the publishing source is wrong:

1. Open your repo on GitHub → **Settings** → **Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions** (not “Deploy from a branch”).
3. Save. The next successful run of the workflow will publish the site.

Until **Source** is **GitHub Actions**, GitHub may be serving the branch (e.g. repo root), which has no `index.html`, so you get 404 even though the workflow succeeded.

### What the workflow does

- Runs on every push to `main` or `master`
- Installs mdBook and mdbook-mermaid, runs `mdbook build`
- Verifies `book/index.html` exists, then uploads the **book/** directory as the Pages artifact
- Deploys via `actions/deploy-pages`

The site URL is **https://&lt;username&gt;.github.io/&lt;repo&gt;/** (e.g. `https://zahanturel.github.io/Zenith/`). After setting Source to GitHub Actions, the site will load on the next push.

---

## Book tooling summary

| Tool        | Purpose |
|------------|---------|
| **mdBook** | Build the book to HTML; use `mdbook build` and `mdbook serve`. |
| **book.yml** | Chapter list for reference; compatible with GitBook/MkDocs if you switch later. |
| **scripts/split_to_chapters.py** | Regenerate chapters and full-spec from a single `.txt` source. |

---

*AI Autonomous Development Platform — System Design Specification — Version 1.0*
