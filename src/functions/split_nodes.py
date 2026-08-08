from functions.extract_markdown import extract_markdown_images, extract_markdown_links
from nodes.textnode import TextNode, TextType


def split_text_nodes(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splitted_nodes = node.text.split(delimiter)

        if len(splitted_nodes) % 2 == 0:
            raise Exception("Invalid Markdown syntax found")

        for i in range(len(splitted_nodes)):
            section = splitted_nodes[i]

            if not section:
                continue

            if i % 2 == 0:
                section_node = TextNode(section, TextType.TEXT)
                new_nodes.append(section_node)
            else:
                section_node = TextNode(section, text_type)
                new_nodes.append(section_node)

    return new_nodes


def split_image_nodes(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text_to_process = node.text
        extracted_node = extract_markdown_images(node.text)

        if not extracted_node:
            new_nodes.append(node)
            continue

        for n in extracted_node:
            image_alt, image_link = n
            section = text_to_process.split(f"![{image_alt}]({image_link})", 1)

            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            if len(section) > 1:
                text_to_process = section[1]

        if text_to_process != "":
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))

    return new_nodes


def split_link_nodes(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text_to_process = node.text
        extracted_node = extract_markdown_links(node.text)

        if not extracted_node:
            new_nodes.append(node)
            continue

        for n in extracted_node:
            link_text, link_url = n
            section = text_to_process.split(f"[{link_text}]({link_url})", 1)

            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            if len(section) > 1:
                text_to_process = section[1]

        if text_to_process != "":
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))

    return new_nodes
