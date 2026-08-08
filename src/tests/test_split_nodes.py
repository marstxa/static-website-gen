import unittest

from functions.split_nodes import *
from nodes.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_text_nodes([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_text_nodes([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_text_nodes([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters_in_one_node(self):
        node = TextNode("Text with `code 1` and `code 2` inside", TextType.TEXT)
        new_nodes = split_text_nodes([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code 1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code 2", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_beginning(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_text_nodes([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("Text ending with `code`", TextType.TEXT)
        new_nodes = split_text_nodes([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_passthrough_non_text_node(self):
        node = TextNode("Already bold `code` inside", TextType.BOLD)
        new_nodes = split_text_nodes([node], "`", TextType.CODE)
        expected = [
            TextNode("Already bold `code` inside", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_mixed_node_types_list(self):
        node1 = TextNode("Plain text ", TextType.TEXT)
        node2 = TextNode("bold text", TextType.BOLD)
        node3 = TextNode(" with `code` in text", TextType.TEXT)
        new_nodes = split_text_nodes([node1, node2, node3], "`", TextType.CODE)
        expected = [
            TextNode("Plain text ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises_exception(self):
        node = TextNode("This is `unmatched code block text", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_text_nodes([node], "`", TextType.CODE)
        self.assertIn("Invalid Markdown syntax found", str(context.exception))

    def test_split_image_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) inside",
            TextType.TEXT,
        )
        new_nodes = split_image_nodes([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_multiple(self):
        node = TextNode(
            "![img1](https://i.imgur.com/1.png) middle ![img2](https://i.imgur.com/2.png) end",
            TextType.TEXT,
        )
        new_nodes = split_image_nodes([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "https://i.imgur.com/1.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://i.imgur.com/2.png"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_at_start_and_end(self):
        node = TextNode(
            "![start](https://i.imgur.com/start.png) and ![end](https://i.imgur.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_image_nodes([node])
        expected = [
            TextNode("start", TextType.IMAGE, "https://i.imgur.com/start.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "https://i.imgur.com/end.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_none_found(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_image_nodes([node])
        self.assertEqual(new_nodes, [node])

    def test_split_image_passthrough_non_text_node(self):
        node = TextNode("Already bold ![img](https://i.imgur.com/1.png)", TextType.BOLD)
        new_nodes = split_image_nodes([node])
        self.assertEqual(new_nodes, [node])

    # =========================================================================
    # Test split_link_nodes
    # =========================================================================

    def test_split_link_single(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) inside",
            TextType.TEXT,
        )
        new_nodes = split_link_nodes([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_multiple(self):
        node = TextNode(
            "Link [one](https://boot.dev) and link [two](https://google.com) finished",
            TextType.TEXT,
        )
        new_nodes = split_link_nodes([node])
        expected = [
            TextNode("Link ", TextType.TEXT),
            TextNode("one", TextType.LINK, "https://boot.dev"),
            TextNode(" and link ", TextType.TEXT),
            TextNode("two", TextType.LINK, "https://google.com"),
            TextNode(" finished", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_at_start_and_end(self):
        node = TextNode(
            "[start](https://boot.dev) then text then [end](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_link_nodes([node])
        expected = [
            TextNode("start", TextType.LINK, "https://boot.dev"),
            TextNode(" then text then ", TextType.TEXT),
            TextNode("end", TextType.LINK, "https://google.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_none_found(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_link_nodes([node])
        self.assertEqual(new_nodes, [node])

    def test_split_link_ignores_images(self):
        node = TextNode(
            "Here is an ![image](https://i.imgur.com/1.png) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_link_nodes([node])
        expected = [
            TextNode(
                "Here is an ![image](https://i.imgur.com/1.png) and a ",
                TextType.TEXT,
            ),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
