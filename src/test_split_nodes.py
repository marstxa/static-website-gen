import unittest

from split_delimiter import split_nodes_delimiter  # Adjust import based on your filename
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters_in_one_node(self):
        node = TextNode("Text with `code 1` and `code 2` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
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
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("Text ending with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_passthrough_non_text_node(self):
        node = TextNode("Already bold `code` inside", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Already bold `code` inside", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_mixed_node_types_list(self):
        node1 = TextNode("Plain text ", TextType.TEXT)
        node2 = TextNode("bold text", TextType.BOLD)
        node3 = TextNode(" with `code` in text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
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
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Invalid Markdown syntax found", str(context.exception))


if __name__ == "__main__":
    unittest.main()
