import unittest

# Adjust this import based on where you save your extract_title function
from functions.extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_with_whitespace(self):
        md = "#    Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_multiline(self):
        md = """
This is some text.

## Not the title

# The Real Title

More text here.
"""
        self.assertEqual(extract_title(md), "The Real Title")

    def test_extract_title_missing(self):
        md = """
This has no h1.
## It only has an h2.
"""
        # We expect the function to raise an Exception when no h1 is found
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
