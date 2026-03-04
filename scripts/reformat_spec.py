#!/usr/bin/env python3
"""
Reformat full-specification.md into a professional architecture book.
- Single title page, copyright, preface, TOC
- One chapter title page per chapter, then new page for content
- Remove duplicate chapter title divs
- Heading hierarchy: ensure spacing after headings, Principle N as ##
- Spacing around figures, tables, code blocks
"""

import re
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent.parent
    src = base / "src" / "full-specification.md"
    out = base / "src" / "full-specification-reformatted.md"

    raw = src.read_text(encoding="utf-8")
    lines = raw.split("\n")
    result = []
    prev_heading = False
    prev_newpage = False
    last_chapter_div = None
    last_chapter_number = None

    def ensure_space():
        nonlocal prev_heading, prev_newpage
        if prev_heading or prev_newpage:
            if result and result[-1].strip():
                result.append("")
        prev_heading = False
        prev_newpage = False

    # Find start: first chapter title page (Chapter 0)
    start_i = 0
    for idx, line in enumerate(lines):
        if "<div align=\"center\">" in line:
            block = "\n".join(lines[idx:min(idx+14, len(lines))])
            if "**Chapter 0**" in block:
                start_i = idx
                break

    i = start_i

    while i < len(lines):
        line = lines[i]

        # Chapter title page: centered div that contains "**Chapter"
        if "<div align=\"center\">" in line:
            j = i
            while j < len(lines) and "</div>" not in lines[j]:
                j += 1
            if j >= len(lines):
                result.append(line)
                i += 1
                continue
            j += 1
            block = "\n".join(lines[i:j])
            if "**Chapter " not in block:
                result.append(line)
                i += 1
                continue
            chapter_match = re.search(r"\*\*Chapter (\d+)\*\*", block)
            if chapter_match and last_chapter_number is not None and last_chapter_number == chapter_match.group(1):
                i = j
                while i < len(lines) and lines[i].strip() in ("", "\\newpage", "---"):
                    i += 1
                continue
            if block == last_chapter_div:
                i = j
                while i < len(lines) and lines[i].strip() in ("", "\\newpage", "---"):
                    i += 1
                continue
            last_chapter_div = block
            if chapter_match:
                last_chapter_number = chapter_match.group(1)
            ensure_space()
            for k in range(i, j):
                result.append(lines[k])
            result.append("")
            result.append("\\newpage")
            result.append("")
            prev_newpage = True
            i = j
            while i < len(lines) and lines[i].strip() in ("", "\\newpage", "---"):
                i += 1
            continue

        # "Principle N — Title" -> ##
        if re.match(r"^Principle \d+ — .+$", line.strip()) and not line.strip().startswith("#"):
            ensure_space()
            result.append("")
            result.append("## " + line.strip())
            result.append("")
            prev_heading = True
            i += 1
            continue

        if line.strip().startswith("#") and result and result[-1].strip() and not result[-1].strip().startswith("#"):
            result.append("")
        if line.strip().startswith("#"):
            prev_heading = True
        if re.match(r"^\s*\*\*Figure \d+", line) or re.match(r"^\s*\*\*Table \d+", line):
            ensure_space()
            result.append("")
        if line.strip() == "---" and result and result[-1].strip() and result[-1].strip() != "---":
            result.append("")
        result.append(line)
        if line.strip() == "---" and i + 1 < len(lines) and lines[i+1].strip() and lines[i+1].strip() != "---":
            result.append("")
        i += 1

    text = "\n".join(result)
    text = re.sub(r"(\s*\\\\newpage\s*){3,}", "\n\n\\newpage\n\n", text)
    text = re.sub(r"(\\\\newpage\s*){2,}", "\\newpage\n\n", text)

    # Normalize chapter headings: "# N. Title" -> "# Chapter N — Title"
    def chapter_heading_repl(m):
        n = m.group(1)
        title = m.group(2)
        return f"# Chapter {n} — {title}"
    text = re.sub(r"^# (\d+)\. (.+)$", chapter_heading_repl, text, flags=re.MULTILINE)

    # Prepend new front matter
    front = r"""<div align="center">

# AI Autonomous Development Platform

## System Design Specification

**Document Version:** 1.0  
**Last Updated:** 4th March 2026  
**Document Status:** Final  
**Author:** Zahan Turel  

Confidentiality: Internal / Restricted

</div>

\newpage

---

## Copyright and Metadata

**Authors:** Zahan Turel  
**Reviewed:** All critical and structural issues addressed. Ready for implementation.

---

## Preface

### Purpose of this document

This specification describes the architecture of the **AI Autonomous Development Platform (AADP)**—a system designed to support large-scale autonomous software engineering through multi-agent collaboration, deep codebase understanding, and governed deployment pipelines. The document serves as the single source of truth for system design, data models, and architectural decisions.

### How to read this book

- **Front to back:** Readers new to the platform should start with the Terminology and Front Matter (Chapter 0), then the Executive Overview (Chapter 1), and proceed through the chapters in order. Each chapter builds on concepts introduced earlier.
- **By topic:** Use the Table of Contents below to jump to specific subsystems (e.g., Orchestration, Agent Architecture, Safety and Guardrails).
- **Reference:** The Terminology Glossary in Chapter 0 defines key terms used consistently throughout.

### Intended audience

- **Architects and technical leads** defining or reviewing the system design
- **Engineers** implementing or integrating with the platform
- **Product and project stakeholders** who need a clear picture of system scope and behavior
- **Compliance and security reviewers** assessing governance and safety measures

The specification is written to be precise enough for implementation while remaining accessible to readers with a software-engineering or systems background.

\newpage

---

## Table of Contents

**PART I — FRONT MATTER AND OVERVIEW**

- Chapter 0 — Terminology and Front Matter
- Chapter 1 — Executive Overview
- Chapter 2 — System Vision
- Chapter 3 — Core Architectural Principles
- Chapter 4 — High Level Architecture

**PART II — CORE ARCHITECTURE**

- Chapter 5 — Agent Architecture
- Chapter 6 — Model Management System
- Chapter 7 — Orchestration System
- Chapter 8 — Codebase Understanding System
- Chapter 9 — Memory and Knowledge Layer
- Chapter 10 — Safety and Guardrail System

**PART III — SUBSYSTEMS AND EXECUTION**

- Chapter 11 — Planning and Execution Cycles
- Chapter 12 — Task Management System
- Chapter 13 — Autonomous Development Workflow
- Chapter 14 — Deployment Infrastructure
- Chapter 15 — Artifact and Release Management
- Chapter 16 — Observability and Monitoring
- Chapter 17 — Scalability Architecture
- Chapter 18 — Security Architecture
- Chapter 19 — Sandboxed Execution Environment
- Chapter 20 — Human Interaction Layer
- Chapter 21 — Self-Improvement and Evolution Layer
- Chapter 22 — Economic / Value Optimization System
- Chapter 23 — Product Intelligence and UX Optimization
- Chapter 24 — Multi-Project Execution System

**PART IV — STRATEGY AND ROADMAP**

- Chapter 25 — Development Roadmap
- Chapter 26 — Implementation Plan
- Chapter 27 — Disaster Recovery and Backup
- Chapter 28 — Cost Model and Budget Control
- Chapter 29 — Future Extensions

**Appendix**

- Appendix A — Architectural Review Notes

---

*Page numbers are omitted in this markdown source; they will be generated in PDF output.*

\newpage

"""
    full = front + text
    out.write_text(full, encoding="utf-8")
    print("Wrote", out)
    return 0


if __name__ == "__main__":
    main()
