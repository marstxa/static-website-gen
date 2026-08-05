from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "****"
    ITALIC = "__"
    CODE = "``"
    LINK = "[]()"
    IMAGE = "![]()"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name.lower()}, {self.url})"


# Helper function
def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    match text_node.text_type:
        case TextType.TEXT:
            leaf_node = LeafNode(None, text_node.text)
        case TextType.BOLD:
            leaf_node = LeafNode("b", text_node.text)
        case TextType.ITALIC:
            leaf_node = LeafNode("i", text_node.text)
        case TextType.CODE:
            leaf_node = LeafNode("code", text_node.text)
        case TextType.LINK:
            leaf_node = LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            leaf_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode does not have any of the values within TextType")

    return leaf_node
