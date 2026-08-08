import unittest

from functions.text_to_textnodes import text_to_textnodes
from nodes.textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_text(self):
        text = "Just plain text without any markdown tags."
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text without any markdown tags.", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_bold_and_italic(self):
        text = "**Bold** and _Italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("Italic", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_adjacent_formatting(self):
        text = "**Bold**_Italic_`Code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_images_and_links(self):
        text = "![img](https://site.com/a.png)[link](https://site.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "https://site.com/a.png"),
            TextNode("link", TextType.LINK, "https://site.com"),
        ]
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
