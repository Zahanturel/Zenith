#!/usr/bin/env python3
"""
Build static documentation from src/ and SUMMARY.md.
Output: site/ (pure HTML/CSS, no framework).
Requires: pip install markdown
"""

import os
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Requires: pip install markdown", file=sys.stderr)
    sys.exit(1)

BOOK_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = BOOK_ROOT / "src"
OUT_DIR = BOOK_ROOT / "site"
TEMPLATES_DIR = BOOK_ROOT / "templates"
STATIC_DIR = BOOK_ROOT / "static"

MD_EXTENSIONS = ["extra", "tables", "codehilite"]
MD_EXTENSION_CONFIG = {}


def parse_summary(summary_path):
    """Parse SUMMARY.md into a list of (type, data). type in ('link', 'section', 'separator')."""
    text = summary_path.read_text(encoding="utf-8")
    entries = []
    in_front_matter = False
    section_title = None
    for line in text.splitlines():
        line_strip = line.strip()
        if not line_strip or line_strip == "# Summary":
            continue
        if line_strip.startswith("# "):
            section_title = line_strip.lstrip("# ")
            continue
        if line_strip == "---":
            entries.append(("separator", None))
            continue
        # [Title](path) or - [Title](path)
        link_match = re.match(r"^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*$", line)
        if link_match:
            title, path = link_match.groups()
            if section_title and entries and entries[-1][0] == "section":
                pass  # section already added
            elif section_title:
                entries.append(("section", section_title))
                section_title = None
            entries.append(("link", (title, path.strip())))
            continue
        link_match2 = re.match(r"^\s*\[([^\]]+)\]\(([^)]+)\)\s*$", line)
        if link_match2:
            title, path = link_match2.groups()
            if section_title:
                entries.append(("section", section_title))
                section_title = None
            entries.append(("link", (title, path.strip())))
            continue
    return entries


def rel_path(from_path, to_path):
    """Relative path from from_path (file) to to_path (file). Use forward slashes for URLs."""
    from_dir = str(Path(from_path).parent) if os.path.dirname(from_path) else "."
    to_dir = str(Path(to_path).parent) if os.path.dirname(to_path) else "."
    if from_dir == "." and to_dir == ".":
        return path_to_html(to_path).replace("\\", "/")
    from_parts = Path(from_dir).parts
    to_parts = Path(to_path).parts
    common = 0
    for a, b in zip(from_parts, to_parts):
        if a == b:
            common += 1
        else:
            break
    up = len(from_parts) - common
    result = list(("..",) * up) + list(to_parts[common:])
    return str(Path(*result)).replace("\\", "/") if result else "."


def path_to_html(path):
    """Convert src-relative .md path to output .html path (forward slashes)."""
    p = path.strip().replace("\\", "/")
    if p.endswith(".md"):
        p = p[:-3] + ".html"
    return p


def render_sidebar(entries, current_html_path):
    """Generate sidebar nav HTML from parsed SUMMARY entries."""
    out = ['<nav class="sidebar-nav" aria-label="Documentation">', '<ul class="sidebar-list">']
    in_ul = False
    for typ, data in entries:
        if typ == "separator":
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append('<li class="sidebar-sep"></li>')
            continue
        if typ == "section":
            if in_ul:
                out.append("</ul>")
            out.append(f'<li class="sidebar-section-title">{data}</li>')
            out.append("<ul>")
            in_ul = True
            continue
        if typ == "link":
            title, path = data
            href = path_to_html(path)
            rel = rel_path(current_html_path, href)
            cur = current_html_path.replace("\\", "/")
            active = " active" if cur == href else ""
            out.append(f'<li><a href="{rel}" class="sidebar-link{active}">{title}</a></li>')
            continue
    if in_ul:
        out.append("</ul>")
    out.append("</ul></nav>")
    return "\n".join(out)


def extract_page_toc(html_content):
    """Extract h2/h3 from content and build page TOC."""
    h2h3 = re.findall(r'<h([23])[^>]*id="([^"]*)"[^>]*>([^<]*)</h[23]>', html_content)
    if not h2h3:
        h2h3 = re.findall(r'<h([23])[^>]*>([^<]*)</h[23]>', html_content)
        if not h2h3:
            return ""
        out = ['<nav class="page-toc" aria-label="On this page">', '<p class="page-toc-title">On this page</p>', "<ul>"]
        for level, text in h2h3:
            slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
            cls = "toc-h3" if level == "3" else "toc-h2"
            out.append(f'<li class="{cls}"><a href="#{slug}">{text}</a></li>')
        out.append("</ul></nav>")
        return "\n".join(out)
    out = ['<nav class="page-toc" aria-label="On this page">', '<p class="page-toc-title">On this page</p>', "<ul>"]
    for level, id_val, text in h2h3:
        cls = "toc-h3" if level == "3" else "toc-h2"
        out.append(f'<li class="{cls}"><a href="#{id_val}">{text}</a></li>')
    out.append("</ul></nav>")
    return "\n".join(out)


def add_ids_to_headings(html_content):
    """Ensure h2/h3 have id attributes for TOC linking."""
    def repl(m):
        tag, rest = m.group(1), m.group(2)
        if 'id="' in rest:
            return m.group(0)
        inner = re.sub(r">\s*", ">", rest)
        text_match = re.match(r">([^<]+)<", inner)
        if text_match:
            text = text_match.group(1).strip()
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            if slug:
                return f"<{tag} id=\"{slug}\"{rest}"
        return m.group(0)
    html_content = re.sub(r"<h([23])([^>]*)>", repl, html_content)
    return html_content


def markdown_to_html(md_path):
    """Convert a single markdown file to HTML body content."""
    raw = md_path.read_text(encoding="utf-8")
    html = markdown.markdown(
        raw,
        extensions=MD_EXTENSIONS,
        extension_config=MD_EXTENSION_CONFIG,
    )
    html = add_ids_to_headings(html)
    # Rewrite internal .md links to .html (leave external URLs unchanged)
    html = re.sub(r'href="(?!https?://)([^"]+?)\.md(#[^"]*)?"', r'href="\1.html\2"', html)
    return html


def build_page(entry_path, summary_entries, template, src_dir):
    """Build one HTML page. entry_path is relative to src (e.g. README.md)."""
    src_path = src_dir / entry_path
    if not src_path.exists():
        return None
    content_html = markdown_to_html(src_path)
    out_html_path = path_to_html(entry_path)
    # Base path for links to site root (e.g. "" or "../" or "../../")
    depth = len(Path(out_html_path).parts) - 1
    base = "../" * depth if depth else ""
    page_toc_html = extract_page_toc(content_html)
    sidebar_html = render_sidebar(summary_entries, out_html_path)
    title = Path(entry_path).stem
    if "chapter" in entry_path.lower() or "appendix" in entry_path.lower():
        title = title.replace("-", " ").title()
    else:
        title = Path(entry_path).stem.replace("-", " ").title()
    html = template.replace("{{content}}", content_html)
    html = html.replace("{{sidebar}}", sidebar_html)
    html = html.replace("{{page_toc}}", page_toc_html)
    html = html.replace("{{title}}", title)
    html = html.replace("{{base}}", base)
    return out_html_path, html


def main():
    src_dir = SRC_DIR
    summary_path = src_dir / "SUMMARY.md"
    if not summary_path.exists():
        print("SUMMARY.md not found", file=sys.stderr)
        sys.exit(1)

    template_path = TEMPLATES_DIR / "base.html"
    if not template_path.exists():
        print("templates/base.html not found", file=sys.stderr)
        sys.exit(1)

    template = template_path.read_text(encoding="utf-8")
    entries = parse_summary(summary_path)

    out_dir = OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect all linked .md paths from SUMMARY
    pages_to_build = []
    for typ, data in entries:
        if typ == "link":
            _, path = data
            path = path.strip()
            if path.endswith(".md") and path not in [p for _, p in pages_to_build]:
                pages_to_build.append((data[0], path))

    built = 0
    for title, path in pages_to_build:
        result = build_page(path, entries, template, src_dir)
        if result is None:
            print(f"Skip (missing): {path}", file=sys.stderr)
            continue
        out_html_path, html = result
        out_file = out_dir / out_html_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        built += 1

    # index.html: redirect to first page (README or first in SUMMARY)
    first_path = "README.md"
    for typ, data in entries:
        if typ == "link":
            first_path = data[1]
            break
    first_html = path_to_html(first_path)
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={first_html}">
<link rel="canonical" href="{first_html}">
<title>AI Autonomous Development Platform</title>
</head>
<body>Redirecting to <a href="{first_html}">documentation</a>.</body>
</html>"""
    (out_dir / "index.html").write_text(index_html, encoding="utf-8")

    # GitHub Pages: disable Jekyll
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    # Copy static assets
    if STATIC_DIR.exists():
        import shutil
        dest_static = out_dir / "static"
        if dest_static.exists():
            shutil.rmtree(dest_static)
        shutil.copytree(STATIC_DIR, dest_static)

    print(f"Built {built} pages + index.html -> {out_dir}")


if __name__ == "__main__":
    main()
