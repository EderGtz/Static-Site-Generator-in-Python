"""Module for recursive HTML page generation from Markdown."""

import os
from md_to_html import markdown_to_html_node
from md_inline_converter import extract_title

SITE_DESCRIPTION = "Backend engineer building event-driven systems, integrations, and data-intensive applications."
SITE_DOMAIN = "https://edergtz.github.io"


def parse_metadata(md_content):
    """Extract optional <!-- key: value --> metadata lines from the top of a markdown file.

    Only consumes pure comment lines before the first non-comment, non-blank line.
    Supported keys: description, canonical, og_title, og_description.
    """
    meta = {}
    for line in md_content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            inner = stripped[4:-3].strip()
            if ":" in inner:
                key, value = inner.split(":", 1)
                meta[key.strip()] = value.strip()
        else:
            break
    return meta


def compute_canonical(dest_path):
    """Derive a production canonical URL from the output path under docs/."""
    rel = dest_path
    if rel.startswith("docs/"):
        rel = rel[5:]
    if rel.endswith(".html"):
        rel = rel[:-5]
    if not rel.startswith("/"):
        rel = "/" + rel
    if rel.endswith("/index"):
        rel = rel[:-6] + "/"
    return SITE_DOMAIN + rel


def generate_page(source_file, template_path, dest_path, basepath):
    """Generate a single HTML page from a Markdown source."""
    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(source_file, "r") as f:
        md_file = f.read()
        md_converted = markdown_to_html_node(md_file).to_html()
        md_title = extract_title(md_file)
        md_meta = parse_metadata(md_file)

    description = md_meta.get("description", SITE_DESCRIPTION)
    canonical = md_meta.get("canonical", compute_canonical(dest_path))
    og_title = md_meta.get("og_title", md_title)
    og_description = md_meta.get("og_description", description)

    with open(template_path, "r") as f:
        html_template = f.read()
        final_html = (
            html_template
            .replace("{{ Title }}", og_title)
            .replace("{{ Description }}", description)
            .replace("{{ Canonical }}", canonical)
            .replace("{{ Content }}", md_converted)
        )
        # basepath replacement affects absolute asset/path references only
        final_html = final_html.replace('href="/', 'href="' + basepath)
        final_html = final_html.replace('src="/', 'src="' + basepath)

    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Recursively generate HTML pages from a directory tree."""
    source_path_content = os.listdir(dir_path_content)
    for file in source_path_content:
        source_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(source_path):
            if not source_path.endswith(".md"):
                continue
            dest_splited = os.path.splitext(dest_path)
            directory = dest_splited[0]
            dest_path = directory + ".html"
            generate_page(source_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(source_path, template_path, dest_path, basepath)
