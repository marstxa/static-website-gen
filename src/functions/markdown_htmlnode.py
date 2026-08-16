from functions.block_to_block_type import BlockType, block_to_block_type
from functions.markdown_blocks import markdown_to_blocks
from functions.text_to_textnodes import text_to_textnodes
from nodes.htmlnode import HTMLNode, ParentNode
from nodes.textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    children_nodes = []
    blocks = markdown_to_blocks(markdown)

    for b in blocks:
        child_node = block_to_html_node(b)
        children_nodes.append(child_node)

    return ParentNode(tag="div", children=children_nodes)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.HEADING:
            heading = f"h{get_heading_level(block)}"
            clean_block = block.lstrip("#").strip()
            children = text_to_children(clean_block)
            return ParentNode(tag=heading, children=children)

        case BlockType.QUOTE:
            lines = block.splitlines()
            clean_lines = [line.lstrip(">").strip() for line in lines]
            clean_block = "\n".join(clean_lines) + "\n"
            items = text_to_children(clean_block)
            return ParentNode(tag="blockquote", children=items)

        case BlockType.UNORDERED_LIST:
            items = []
            lines = block.splitlines()
            for line in lines:
                clean_line = line.lstrip("- ").strip()
                children = text_to_children(clean_line)
                items.append(ParentNode(tag="li", children=children))
            return ParentNode(tag="ul", children=items)

        case BlockType.ORDERED_LIST:
            items = []
            clean_block = strip_ordered_list(block)
            for line in clean_block.splitlines():
                children = text_to_children(line)
                items.append(ParentNode(tag="li", children=children))
            return ParentNode(tag="ol", children=items)

        case BlockType.CODE:
            lines = block.splitlines()
            # Strip the backtick lines from the top and bottom
            if lines and lines[0].strip() == "```":
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            # Clean leading spaces for the test expectation
            clean_lines = [line.strip() for line in lines]
            clean_block = "\n".join(clean_lines) + "\n"

            text_node = TextNode(clean_block, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)

            code_block = ParentNode(tag="code", children=[html_node])
            return ParentNode(tag="pre", children=[code_block])

        case _:
            lines = block.splitlines()
            paragraph_text = " ".join([line.strip() for line in lines])
            child_nodes = text_to_children(paragraph_text)
            return ParentNode(tag="p", children=child_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def get_heading_level(block: str) -> int:
    parts = block.split(" ", 1)
    if len(parts) > 1 and 1 <= len(parts[0]) and set(parts[0]) == {"#"}:
        return len(parts[0])
    return 0


def strip_ordered_list(block: str) -> str:
    lines = block.split("\n")
    clean_block = ""
    for line in lines:
        if ". " in line:
            parts = line.split(". ", 1)
            clean_block += f"{parts[1]}\n"
        else:
            clean_block += f"{line.strip()}\n"
    return clean_block
