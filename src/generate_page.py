"""Module for recursive HTML page generation from Markdown."""

import os
from md_to_html import markdown_to_html_node
from md_inline_converter import extract_title

def generate_page(source_file, template_path, dest_path, basepath):
    """Generate a single HTML page from a Markdown source."""
    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(source_file, "r") as f:
        md_file = f.read()
        md_converted = markdown_to_html_node(md_file).to_html()
        md_title = extract_title(md_file)

    with open(template_path, "r") as f:
        html_template = f.read()
        title_replaced = html_template.replace("{{ Title }}", md_title)
        content_replaced = title_replaced.replace("{{ Content }}", md_converted)
        href_replaced = content_replaced.replace('href="/', f'href="{basepath}')
        final_html = href_replaced.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(final_html)

#Generate all HTTP pages from a given origin path
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Recursively generate HTML pages from a directory tree."""
    source_path_content = os.listdir(dir_path_content)
    for file in source_path_content:
        source_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(source_path):
            #This is to change the md extension to html
            dest_splited = os.path.splitext(dest_path)
            directory = dest_splited[0]
            dest_path = directory + ".html"
            generate_page(source_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(source_path, template_path, dest_path, basepath)
