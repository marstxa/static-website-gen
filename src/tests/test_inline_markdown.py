import unittest

from functions.block_to_block_type import *

# Adjust the import based on your module structure
from functions.markdown_blocks import markdown_to_blocks


class TestInlineMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
This is a paragraph.




This is another paragraph with leading and trailing excess newlines.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "This is another paragraph with leading and trailing excess newlines.",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph without any double newlines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just a single paragraph without any double newlines."],
        )

    def test_markdown_to_blocks_whitespace_handling(self):
        md = "  Paragraph with leading spaces.  \n\n  Another paragraph with trailing spaces.  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph with leading spaces.",
                "Another paragraph with trailing spaces.",
            ],
        )

    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_invalid_no_space(self):
        # Missing space after '#' makes it a normal paragraph
        self.assertEqual(block_to_block_type("#InvalidHeading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too Many"), BlockType.PARAGRAPH)

    # =========================================================================
    # Code Block Tests
    # =========================================================================

    def test_code_block_valid(self):
        code = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_code_block_missing_newline(self):
        # Starts with ``` but no newline immediately after
        code = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.PARAGRAPH)

    # =========================================================================
    # Quote Block Tests
    # =========================================================================

    def test_quote_block_single_and_multiline(self):
        self.assertEqual(block_to_block_type("> Single line quote"), BlockType.QUOTE)

        multiline_quote = "> First line\n>Second line without space\n> Third line"
        self.assertEqual(block_to_block_type(multiline_quote), BlockType.QUOTE)

    def test_quote_block_invalid_line(self):
        # If any line misses the '>', it falls back to a paragraph
        bad_quote = "> Line 1\nLine 2 without angle bracket\n> Line 3"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    # =========================================================================
    # Unordered List Tests
    # =========================================================================

    def test_unordered_list_valid(self):
        ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        # Item missing a space after '-'
        bad_ul = "- Item 1\n-Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(bad_ul), BlockType.PARAGRAPH)

    # =========================================================================
    # Ordered List Tests
    # =========================================================================

    def test_ordered_list_valid(self):
        ol = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_number(self):
        # Must start at 1
        bad_ol = "2. First item\n3. Second item"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

    def test_ordered_list_out_of_sequence(self):
        # Must increment sequentially
        bad_ol = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space(self):
        # Missing space after the period
        bad_ol = "1.First item\n2. Second item"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

    # =========================================================================
    # Paragraph Tests
    # =========================================================================

    def test_paragraph(self):
        text = "This is a normal paragraph of text with no special markdown formatting."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
