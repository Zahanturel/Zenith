# AI Autonomous Development Platform — System Design Specification (Book)

This repository contains the **AI Autonomous Development Platform (AADP) System Design Specification** as a book manuscript with a static documentation build and CI for publishing.

**Version:** See [VERSION](VERSION) (v1.0)  
**Authors:** Zahan Turel, Zenith  
**Status:** Final — Ready for implementation  
**License:** [MIT](LICENSE)

---

## Repository structure

```
aadp-book/
├── VERSION                # Book version (e.g. v1.0)
├── README.md              # This file
├── LICENSE                # MIT
├── requirements.txt       # Python deps for doc build (markdown)
├── CONTRIBUTING.md        # How to contribute (tooling/docs only)
├── CHANGELOG.md           # Tooling and repo changes
│
├── src/                   # Documentation source
│   ├── SUMMARY.md         # Navigation order (sidebar hierarchy)
│   ├── README.md          # "How to read this book"
│   ├── index.md           # Introduction and table of contents
│   ├── full-specification.md
│   ├── references.md
│   ├── book-frontmatter/  # Title page, preface
│   └── chapters/          # Chapter Markdown files (00–30)
│
├── templates/             # HTML template for static site
├── static/                # CSS (layout, print)
├── scripts/               # Build scripts (build_docs.py, etc.)
├── site/                  # Built static site (generated; see .gitignore)
└── .github/workflows/     # CI: build and deploy to GitHub Pages
```

---

## How to read the book

- **Single file:** Open [full-specification.md](src/full-specification.md) for the complete spec in one Markdown file.
- **By chapter:** Start with [index.md](src/index.md) for the table of contents and links to every chapter.
- **Built site:** Run the build (see below) and open `site/index.html` in a browser, or use any static file server (e.g. `python -m http.server` in `site/`).

The **Terminology Glossary** is in [src/chapters/00-terminology-and-front-matter.md](src/chapters/00-terminology-and-front-matter.md). Chapters 01–29 map to Sections 1–29 of the original specification; Chapter 30 is Appendix A.

---

## Building the documentation

The documentation is built by a **static generator** (no mdBook or other framework). Output is plain HTML and CSS in **site/**.

**Requirements:** Python 3 and the `markdown` package.

```bash
pip install -r requirements.txt
python scripts/build_docs.py
```

Output is in **site/**. Open `site/index.html` in a browser or serve the folder with any static server:

```bash
cd site && python -m http.server 8000
# Then open http://localhost:8000
```

**What the build does:**

- Reads **src/SUMMARY.md** for navigation order and hierarchy (front matter, chapters, appendix, references).
- Converts each linked Markdown file to HTML and wraps it in the layout template (header, sidebar, main content, optional “On this page” TOC).
- Writes **site/** with `index.html` (redirect to first page), all chapter and front-matter pages, and **site/static/** (CSS). Internal `.md` links in content are rewritten to `.html`.

---

## Rebuilding chapters from source

If you have the original specification as a single `.txt` file, you can regenerate `full-specification.md` and all files in `chapters/` using the split script.

```bash
python scripts/split_to_chapters.py
# Or: python scripts/split_to_chapters.py path/to/source.txt
```

---

## Layout and structure

The static site uses a simple, stable layout:

- **Header:** Site title, link to home; on small screens, a toggle for the sidebar.
- **Sidebar:** Persistent navigation generated from **src/SUMMARY.md** (sections: Front Matter, chapters, Full specification, References). Reflects the exact document hierarchy.
- **Main content:** Rendered Markdown (tables, code blocks, headings). Headings get IDs for in-page links.
- **On this page:** Optional right-hand TOC for H2/H3 on the current page (hidden on small screens).

Layout and print behavior are controlled only by **static/css/layout.css** and **static/css/print.css**. No JavaScript is required except a small script to toggle the sidebar on narrow viewports.

---

## CI and GitHub Pages

A GitHub Actions workflow (**.github/workflows/build-book.yml**) builds the static site and deploys it to **GitHub Pages** on every push to `main` or `master`.

### Enable the live site (fixes 404)

If the workflow succeeds but **https://&lt;username&gt;.github.io/&lt;repo&gt;/** returns **404**:

1. Open the repo on GitHub → **Settings** → **Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions** (not “Deploy from a branch”).
3. Save. The next successful run will publish the site.

### What the workflow does

- Runs on push to `main` or `master`
- Installs Python and `pip install -r requirements.txt`
- Runs `python scripts/build_docs.py` to produce **site/**
- Uploads **site/** as the Pages artifact and deploys via `actions/deploy-pages`

The site URL is **https://&lt;username&gt;.github.io/&lt;repo&gt;/**.

---

## Adding or reordering content

1. **Add a new chapter:** Add a new `.md` file under **src/chapters/** (or another folder under **src/**) and add a link to it in **src/SUMMARY.md** in the desired position. Re-run the build.
2. **Change order or sections:** Edit **src/SUMMARY.md**. Use `# Section title` for a section heading in the sidebar, `- [Title](path.md)` for items under a section, and `[Title](path.md)` for top-level links. Use `---` for a visual separator. Re-run the build.

The sidebar and all internal links are driven by **SUMMARY.md**; no other config is needed for navigation.

---

## Print

Use the browser’s **Print → Save as PDF** (or print) on any page. **static/css/print.css** hides the header toggle, sidebar, and “On this page” panel so the printed output is a clean, readable document.

---

*AI Autonomous Development Platform — System Design Specification — Version 1.0*
