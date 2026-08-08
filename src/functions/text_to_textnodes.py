from functions.split_nodes import *
from nodes.textnode import TextNode, TextType


def text_to_textnodes(text):

    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_image_nodes(new_nodes)
    new_nodes = split_link_nodes(new_nodes)
    new_nodes = split_text_nodes(new_nodes, "**", TextType.BOLD)
    new_nodes = split_text_nodes(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_text_nodes(new_nodes, "`", TextType.CODE)

    return new_nodes
