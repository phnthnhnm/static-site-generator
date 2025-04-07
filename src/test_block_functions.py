import unittest

from block_functions import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_markdown_to_blocks_empty_lines(self):
        markdown = """# Heading

        
This is a paragraph.


- List item 1
- List item 2"""
        expected_blocks = [
            "# Heading",
            "This is a paragraph.",
            "- List item 1\n- List item 2",
        ]
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_markdown_to_blocks_trailing_whitespace(self):
        markdown = """# Heading   

   This is a paragraph.   

- List item 1   \n- List item 2   """
        expected_blocks = [
            "# Heading",
            "This is a paragraph.",
            "- List item 1   \n- List item 2",
        ]
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_markdown_to_blocks_only_newlines(self):
        markdown = "\n\n\n"
        expected_blocks = []
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_markdown_to_blocks_single_block(self):
        markdown = "This is a single block of text."
        expected_blocks = ["This is a single block of text."]
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = """```
code block
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> Another line of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
