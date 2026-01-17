"""Entry point for the Static Site Generator (SSG)."""

import os
import shutil
from copy_static_to_public import copy_static_dir
from generate_page import generate_pages_recursive

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"

SOURCE_MD = "./content"
TEMPLATE_HTML = "./template.html"
DEST_PATH = "./public"

def main():
    """Orchestrate the site build by copying assets and generating pages."""
    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)
    os.mkdir(DIR_PATH_PUBLIC)
    copy_static_dir(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    generate_pages_recursive(SOURCE_MD, TEMPLATE_HTML, DEST_PATH)

if __name__ == "__main__":
    main()
