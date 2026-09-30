import os
import shutil
import sys

from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Generating website...")
    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages recursively...")
    generate_pages_recursive("content", "template.html", dir_path_public, basepath)

    print("Success!")


if __name__ == "__main__":
    main()
