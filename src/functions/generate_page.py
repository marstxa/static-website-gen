import os
from pathlib import Path

from functions.extract_title import extract_title
from functions.markdown_htmlnode import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str | Path, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        markdown = from_file.read()
        from_file.close()

    with open(template_path, "r") as template_file:
        template = template_file.read()
        template_file.close()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)

        if not os.path.isfile(file_path):
            dest_path = os.path.join(dest_dir_path, filename)
            # Pass base_path into the recursion
            generate_pages_recursive(file_path, template_path, dest_path, base_path)
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            dest_path = dest_path.replace(".md", ".html")
            # Pass base_path into the final page generator
            generate_page(file_path, template_path, dest_path, base_path)
