from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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
