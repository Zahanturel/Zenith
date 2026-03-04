# -*- coding: utf-8 -*-
"""Split the AADP System Design Specification .txt into chapter markdown files."""
import argparse
import os
import re

# Repo root: parent of the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_ROOT = os.path.dirname(SCRIPT_DIR)
CHAPTERS_DIR = os.path.join(BOOK_ROOT, "chapters")
DEFAULT_SOURCE = os.path.join(BOOK_ROOT, "full-specification.txt")
FULL_SPEC_FILENAME = "full-specification.md"

# (start_line_1based, end_line_1based_inclusive, filename)
# Line numbers from grep - sections start at these lines
SPLITS = [
    (45, 402, "01-executive-overview.md"),
    (403, 686, "02-system-vision.md"),
    (687, 1068, "03-core-architectural-principles.md"),
    (1069, 1428, "04-high-level-architecture.md"),
    (1429, 1757, "05-agent-architecture.md"),
    (1758, 1977, "06-model-management-system.md"),
    (1978, 2302, "07-orchestration-system.md"),
    (2303, 2631, "08-codebase-understanding-system.md"),
    (2632, 2954, "09-memory-and-knowledge-layer.md"),
    (2955, 3251, "10-safety-and-guardrail-system.md"),
    (3252, 3596, "11-planning-and-execution-cycles.md"),
    (3597, 3912, "12-task-management-system.md"),
    (3913, 4304, "13-autonomous-development-workflow.md"),
    (4305, 4641, "14-deployment-infrastructure.md"),
    (4642, 4860, "15-artifact-and-release-management.md"),
    (4861, 5164, "16-observability-and-monitoring.md"),
    (5165, 5425, "17-scalability-architecture.md"),
    (5426, 5754, "18-security-architecture.md"),
    (5755, 5947, "19-sandboxed-execution-environment.md"),
    (5948, 6208, "20-human-interaction-layer.md"),
    (6209, 6466, "21-self-improvement-and-evolution.md"),
    (6467, 6647, "22-economic-value-optimization-system.md"),
    (6648, 6875, "23-product-intelligence-and-ux.md"),
    (6876, 7172, "24-multi-project-execution-system.md"),
    (7173, 7473, "25-development-roadmap.md"),
    (7474, 7784, "26-implementation-plan.md"),
    (7785, 7976, "27-disaster-recovery-and-backup.md"),
    (7977, 8242, "28-cost-model-and-budget-control.md"),
    (8243, 8475, "29-future-extensions.md"),
    (8476, 9999, "30-appendix-a.md"),
]


def to_md(text):
    """Convert plain text to markdown: dividers and bullets."""
    text = text.replace("________________________________________", "\n---\n")
    text = re.sub(r"^•\t", "- ", text, flags=re.MULTILINE)
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        s = line
        if re.match(r"^\d+\. [A-Z]", s.strip()):
            out.append("")
            out.append("# " + s.strip())
            out.append("")
            continue
        out.append(s)
    return "\n".join(out).replace("\n\n\n---", "\n\n---").replace("---\n\n\n", "---\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Split the AADP System Design Specification .txt into chapter markdown files."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=DEFAULT_SOURCE,
        help=f"Path to source .txt file (default: full-specification.txt in repo root)",
    )
    args = parser.parse_args()
    source_path = os.path.abspath(args.source)

    if not os.path.isfile(source_path):
        print(f"Error: source file not found: {source_path}")
        return 1

    with open(source_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    os.makedirs(CHAPTERS_DIR, exist_ok=True)

    # Write single full markdown file (like the original .txt, but in .md)
    full_text = "".join(all_lines)
    full_md = to_md(full_text)
    full_path = os.path.join(BOOK_ROOT, FULL_SPEC_FILENAME)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(full_md)
    print("Wrote", full_path)

    for start, end, fname in SPLITS:
        chunk = "".join(all_lines[start - 1 : end])
        md = to_md(chunk)
        path = os.path.join(CHAPTERS_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        print("Wrote", path)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
