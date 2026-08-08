import unittest

# Adjust the import path to match your module name inside src/functions/
from functions.extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
)


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


if __name__ == "__main__":
    unittest.main()
