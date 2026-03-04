# -*- coding: utf-8 -*-
"""
Refactor full-specification.md: remove duplicates, fix structure, improve readability.
Writes directly to src/full-specification.md.
"""
import re
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parent.parent
SRC = BOOK_ROOT / "src" / "full-specification.md"


def remove_duplicate_chapter_blocks(text):
    """Remove duplicate <div> Chapter N blocks and all \\newpage."""
    lines = text.split("\n")
    result = []
    i = 0
    seen_chapter_div = None

    while i < len(lines):
        line = lines[i]
        if line.strip() == "\\newpage":
            i += 1
            continue
        if "<div align=\"center\">" in line or '<div align="center">' in line:
            block_start = i
            j = i
            while j < len(lines) and "</div>" not in lines[j]:
                j += 1
            if j < len(lines):
                j += 1
            block = "\n".join(lines[block_start:j])
            if "**Chapter " in block:
                if seen_chapter_div is not None and block.strip() == seen_chapter_div.strip():
                    i = j
                    while i < len(lines) and lines[i].strip() in ("", "\\newpage", "---"):
                        i += 1
                    continue
                seen_chapter_div = block.strip()
                i = j
                while i < len(lines) and lines[i].strip() in ("", "\\newpage", "---"):
                    i += 1
                continue
        result.append(line)
        i += 1

    return "\n".join(result)


def collapse_excessive_newlines(text):
    """At most 2 newlines (one blank line) between content."""
    return re.sub(r"\n{3,}", "\n\n", text)


def main():
    raw = SRC.read_text(encoding="utf-8")
    text = remove_duplicate_chapter_blocks(raw)
    text = collapse_excessive_newlines(text)
    SRC.write_text(text, encoding="utf-8")
    print("Refactored", SRC)


if __name__ == "__main__":
    main()
