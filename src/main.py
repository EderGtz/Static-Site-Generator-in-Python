"""Entry point for the Static Site Generator (SSG)."""

import os
import sys
import shutil
from copy_static_to_public import copy_static_dir
from generate_page import generate_pages_recursive, parse_metadata
from md_utils import parse_frontmatter, split_sections, extract_title

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./docs"

SOURCE_MD = "./content"
TEMPLATE_HTML = "./template.html"
DEST_PATH = "./docs"
DEFAULT_BASEPATH = "/"

SITE_TITLE = "Eder Gutiérrez — Backend Engineer"
SITE_DESCRIPTION = "Backend engineer building event-driven systems, integrations, and data-intensive applications."
SITE_DOMAIN = "https://edergtz.github.io"


def _compose_page_html(source_md_path, template_path, dest_path, basepath):
    """Generate a single HTML page from Markdown with optional frontmatter.

    Supports:
      - Top-level frontmatter (title, description, canonical, og_*).
      - Named <!-- section: name --> markers for multi-slot composition.
    """
    with open(source_md_path, "r") as f:
        md_text = f.read()

    frontmatter, remaining = parse_frontmatter(md_text)
    title = frontmatter.get("title", SITE_TITLE if dest_path.endswith("docs/index.html") else None)
    if not title:
        title = extract_title(remaining)

    description = frontmatter.get(
        "description",
        frontmatter.get("og_description", SITE_DESCRIPTION),
    )
    canonical = frontmatter.get("canonical")
    if not canonical:
        rel = dest_path
        # Normalize: strip leading ./ or ./
        rel = rel.lstrip("./")
        if rel.startswith("docs/"):
            rel = rel[5:]
        if rel.endswith(".html"):
            rel = rel[:-5]
        if not rel.startswith("/"):
            rel = "/" + rel
        if rel.endswith("/index"):
            rel = rel[:-6] + "/"
        canonical = SITE_DOMAIN + rel

    sections = split_sections(remaining)
    default_content = sections.pop("default", "")
    # For monolithic pages without section markers, default_content is the whole body.
    body_html = ""
    for name, md in sections.items():
        body_html += f'<section class="slot slot-{name}">{md}</section>\n'
    if default_content:
        body_html = f'<section class="slot slot-default">{default_content}</section>\n' + body_html

    md_converted = body_html  # We let the markdown renderer handle only the raw blocks inside sections;
    # For now this composes already-rendered slots. To keep it simple, render each section as markdown.

    from md_to_html import markdown_to_html_node

    rendered_slots = ""
    for name, md in sections.items():
        rendered_slots += f'<section class="slot {name}">{markdown_to_html_node(md).to_html()}</section>\n'
    if default_content:
        rendered_slots = f'<section class="slot default">{markdown_to_html_node(default_content).to_html()}</section>\n' + rendered_slots

    md_converted = rendered_slots

    with open(template_path, "r") as f:
        html_template = f.read()

    og_image = frontmatter.get("og_image", "")
    twitter_image = frontmatter.get("twitter_image", og_image)
    final_html = (
        html_template
        .replace("{{ Title }}", title)
        .replace("{{ Description }}", description)
        .replace("{{ Canonical }}", canonical)
        .replace("{{ OgImage }}", og_image)
        .replace("{{ TwitterImage }}", twitter_image)
        .replace("{{ Content }}", md_converted)
    )
    final_html = _safe_replace(final_html, basepath)
    final_html = _safe_replace(final_html, basepath, attr="src")

    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)


def _safe_replace(html, basepath, attr="href"):
    """Replace absolute attr="/... only when they target this site."""
    import re
    # Only replace absolute paths that are real site paths (start with / and don't contain : or .)
    def replacer(m):
        full = m.group(0)
        inner = m.group(1)
        # Skip URLs that are external (contain ://) or reference other files (contain .)
        if "://" in inner or inner.startswith("./") or inner.startswith("../"):
            return full
        return attr + '="' + basepath + inner.lstrip("/") + '"'
    return re.sub(r'' + attr + '="(/[^"]+)"', replacer, html)


def build():
    basepath = DEFAULT_BASEPATH
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)
    os.mkdir(DIR_PATH_PUBLIC)
    copy_static_dir(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

    resume_src = "./Eder_Gutierrez_Resume.pdf"
    resume_dest = os.path.join(DIR_PATH_PUBLIC, "resume", "Eder_Gutierrez_Resume.pdf")
    if os.path.exists(resume_src):
        os.makedirs(os.path.dirname(resume_dest), exist_ok=True)
        shutil.copy(resume_src, resume_dest)

    # Render each markdown file through _compose_page_html so frontmatter and sections work.
    for root, _, files in os.walk(SOURCE_MD):
        for file in files:
            if not file.endswith(".md"):
                continue
            source_path = os.path.join(root, file)
            rel = os.path.relpath(source_path, SOURCE_MD)
            dest_rel = rel[:-3] + ".html"
            dest_path = os.path.join(DEST_PATH, dest_rel)
            _compose_page_html(source_path, TEMPLATE_HTML, dest_path, basepath)


if __name__ == "__main__":
    build()
