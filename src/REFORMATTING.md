# Reformatting Guide — Full Specification

The file **full-specification-reformatted.md** is generated from **full-specification.md** using the script `scripts/reformat_spec.py`. No technical content is changed; only structure, layout, and formatting are improved.

## What the script does

- **Single front matter** — One title page, one Copyright/Metadata section, one Preface, one Table of Contents (replaces the original repeated blocks).
- **Chapter title pages** — Each chapter has one centered title page (chapter number, title, short description), followed by `\newpage`, then the chapter content. Duplicate chapter title pages are removed.
- **Heading hierarchy** — Chapter content uses `# Chapter N — Title` (H1). Principle sections use `## Principle N — Title` (H2). Spacing is added after headings so a heading never immediately follows another heading or a page break without a blank line.
- **Spacing** — Blank lines before `**Figure N — ...**` and `**Table N — ...**`; consistent spacing around horizontal rules (`---`).
- **Page breaks** — Multiple consecutive `\newpage` are collapsed to one. Each chapter’s content starts after a single `\newpage` following its title page.

## How to regenerate

From the repository root:

```bash
python scripts/reformat_spec.py
```

Output is written to `src/full-specification-reformatted.md`.

## Typography and print

The print stylesheet enforces:

- **H1** — Chapter title; large spacing above; page break before each chapter in print.
- **H2** — Major section; medium spacing.
- **H3** — Subsystem; smaller spacing.
- **H4 / H5** — Component and technical detail.
- **Figures and tables** — `page-break-inside: avoid` so they are not split across pages.
- **Horizontal rules** — Used for visual separation between architecture layers.

## Conventions in the reformatted document

- **Figures** — `**Figure N — Title**` on its own line, then the diagram (e.g. Mermaid block), then optional caption. Vertical spacing before and after.
- **Tables** — `**Table N — Title**` then the markdown table. Header row in bold in the theme.
- **Data models** — Code blocks with spacing before and after; schema names as `#### Name` (H4/H5).
- **Glossary (Chapter 0)** — Table format: Term | Definition; alphabetical order.
- **Table of Contents** — Part titles (PART I–IV) and chapter list; page numbers are generated in PDF output.

## Constraints

- **No technical changes** — Meanings, data models, subsystem definitions, and architectural content are preserved.
- **Only structural/formatting changes** — Restructure, reformat, improve hierarchy and readability.
