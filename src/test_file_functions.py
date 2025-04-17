import unittest
from src.file_functions import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_valid_h1_header(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_h1_with_leading_and_trailing_spaces(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_no_h1_header(self):
        markdown = "## Subheader\nSome content"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(
            str(context.exception), "No h1 header found in the markdown content"
        )

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(
            str(context.exception), "No h1 header found in the markdown content"
        )

    def test_multiple_h1_headers(self):
        markdown = "# First Header\n# Second Header"
        self.assertEqual(extract_title(markdown), "First Header")


if __name__ == "__main__":
    unittest.main()
