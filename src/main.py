import os
import shutil
import sys

from functions.copy_static import copy_files_recursive
from functions.generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main() -> None:
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    print("Deleting docs directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    # 2. Pass the base_path down into your recursive function
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, base_path)


if __name__ == "__main__":
    main()
