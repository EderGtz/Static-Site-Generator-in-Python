import os
import shutil
from copy_static_to_public import copy_static_dir

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)
    copy_static_dir(dir_path_static, dir_path_public)

if __name__ == "__main__":
    main()
