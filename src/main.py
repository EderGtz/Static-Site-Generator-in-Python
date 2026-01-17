import os
import shutil
from copy_static_to_public import copy_static_dir
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"

source_md = "./content"
template_html = "./template.html"
dest_path = "./public"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)
    copy_static_dir(dir_path_static, dir_path_public)
    generate_pages_recursive(source_md, template_html, dest_path)

if __name__ == "__main__":
    main()
