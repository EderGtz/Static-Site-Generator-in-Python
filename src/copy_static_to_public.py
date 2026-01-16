'''This module contains a recursive function that copies all the contents
from a source directory to a dest directory. In this case, is used
to recreate the public dir of the ssg'''
import os
import shutil

#Takes two paths: the source path that will be entirely copied, and a dest path to store it
def copy_static_dir(source_path_dir, dest_path_dir):
    #This line is util for every recursion call
    if not os.path.exists(dest_path_dir):
        os.mkdir(dest_path_dir)
    for file in os.listdir(source_path_dir):
        source_file = os.path.join(source_path_dir, file)
        dest_path = os.path.join(dest_path_dir, file)
        if os.path.isfile(source_file):
            shutil.copy(source_file, dest_path)
        else:
            copy_static_dir(source_file, dest_path)
