"""Extended Markdown processing helpers for SSG.

Adds frontmatter parsing and section extraction so templates can compose
a page from multiple named content slots (hero, experience, projects, ...).
"""

import re
from md_blocks import markdown_to_blocks


def parse_frontmatter(md_text):
    """Extract a simple YAML-like frontmatter block at the very top of a file.

    Returns (frontmatter_dict, remaining_md_text). If no frontmatter is present,
    returns ({}, md_text).
    """
    if not md_text.startswith("---\n"):
        return {}, md_text

    end = md_text.find("\n---\n", 4)
    if end == -1:
        return {}, md_text

    raw = md_text[4:end].strip()
    remaining = md_text[end + 4:]

    frontmatter = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, remaining


def split_sections(md_text):
    """Split markdown into named sections.

    Sections are delimited by HTML comments of the form:
        <!-- section: hero -->
        ... markdown ...
        <!-- section: experience -->
        ... markdown ...

    Returns a dict mapping section name -> markdown string. Content before the
    first section marker is keyed as 'default'.
    """
    pattern = re.compile(r"<!--\s*section:\s*([a-zA-Z0-9_-]+)\s*-->")
    sections = {}
    current_name = "default"
    current_lines = []

    for line in md_text.splitlines():
        m = pattern.match(line.strip())
        if m:
            sections[current_name] = "\n".join(current_lines).strip()
            current_name = m.group(1)
            current_lines = []
        else:
            current_lines.append(line)

    sections[current_name] = "\n".join(current_lines).strip()
    return sections


def extract_title(md):
    """Retrieve the first H1 header from a Markdown string."""
    if not md:
        raise ValueError("Invalid input")
    # Skip leading blank lines (e.g. after frontmatter close)
    lines = md.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.strip("# ").rstrip()
    raise Exception("md file should start with a title in #")
