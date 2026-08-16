import os
import os.path

from functions.extract_title import extract_title
from functions.markdown_htmlnode import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
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
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)

        if not os.path.isfile(file_path):
            dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(file_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            dest_path = dest_path.replace(".md", ".html")
            generate_page(file_path, template_path, dest_path)
