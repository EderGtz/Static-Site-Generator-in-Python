"""Entry point for the Static Site Generator (SSG)."""

import os
import sys
import shutil
from copy_static_to_public import copy_static_dir
from generate_page import generate_pages_recursive

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./docs"

SOURCE_MD = "./content"
TEMPLATE_HTML = "./template.html"
DEST_PATH = "./docs"
DEFAULT_BASEPATH = "/"

def main():
    """Orchestrate the site build by copying assets and generating pages."""
    basepath = DEFAULT_BASEPATH
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)
    os.mkdir(DIR_PATH_PUBLIC)
    copy_static_dir(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    # Copy resume PDF from repo root into docs/resume/
    resume_src = "./Eder_Gutierrez_Resume.pdf"
    resume_dest = os.path.join(DIR_PATH_PUBLIC, "resume", "Eder_Gutierrez_Resume.pdf")
    if os.path.exists(resume_src):
        os.makedirs(os.path.dirname(resume_dest), exist_ok=True)
        shutil.copy(resume_src, resume_dest)
    generate_pages_recursive(SOURCE_MD, TEMPLATE_HTML, DEST_PATH, basepath)

if __name__ == "__main__":
    main()
