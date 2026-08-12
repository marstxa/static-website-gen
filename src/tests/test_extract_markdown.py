import unittest

# Adjust the import path to match your module name inside src/functions/
from functions.extract_markdown import extract_markdown_images, extract_markdown_links
from functions.markdown_htmlnode import markdown_to_html_node


class TestExtractMarkdown(unittest.TestCase):
    # --- Image Extraction Tests ---

    def test_extract_markdown_images_single(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_markdown_images_multiple(self):
        text = "Text with ![image 1](https://i.imgur.com/1.png) and ![image 2](https://i.imgur.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [
                ("image 1", "https://i.imgur.com/1.png"),
                ("image 2", "https://i.imgur.com/2.png"),
            ],
        )

    def test_extract_markdown_images_ignores_links(self):
        text = "Here is a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_none_found(self):
        text = "This text has no images or links."
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_images_empty_alt_text(self):
        text = "An image with empty alt text ![](https://i.imgur.com/empty.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("", "https://i.imgur.com/empty.png")])

    # --- Link Extraction Tests ---

    def test_extract_markdown_links_single(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_extract_markdown_links_multiple(self):
        text = "Link [one](https://www.boot.dev) and link [two](https://www.youtube.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("one", "https://www.boot.dev"),
                ("two", "https://www.youtube.com"),
            ],
        )

    def test_extract_markdown_links_ignores_images(self):
        text = "Here is a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("link", "https://boot.dev")])

    def test_extract_markdown_links_none_found(self):
        text = "This text has no links or images."
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links_empty_anchor(self):
        text = "A link with empty anchor text [](https://boot.dev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("", "https://boot.dev")])

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**

### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading 3</h3></div>",
        )

    def test_blockquote(self):
        md = """
> This is a quote block
> with multiple lines and _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block\nwith multiple lines and <i>italic</i> text\n</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item with **bold**
- Second item
- Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b></li><li>Second item</li><li>Third item with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with _italics_
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italics</i></li><li>Third item</li></ol></div>",
        )

    def test_mixed_markdown(self):
        md = """
# Title

This is a paragraph with **bold** and `code`.

- List item 1
- List item 2

> A great quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph with <b>bold</b> and <code>code</code>.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>A great quote\n</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
