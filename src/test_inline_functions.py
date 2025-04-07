import unittest

from inline_functions import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.NORMAL)]
        delimiter = "**"
        text_type = TextType.BOLD

        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.NORMAL),
        ]

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_italic(self):
        old_nodes = [TextNode("This is text with a *italicized phrase* in the middle", TextType.NORMAL)]
        delimiter = "*"
        text_type = TextType.ITALIC

        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("italicized phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.NORMAL),
        ]

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", TextType.NORMAL)]
        delimiter = "`"
        text_type = TextType.CODE

        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_empty_string(self):
        old_nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.NORMAL)]
        delimiter = ""
        text_type = TextType.BOLD

        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)
            
    def test_split_nodes_delimiter_no_match(self):
        old_nodes = [TextNode("This is text without delimiters", TextType.NORMAL)]
        delimiter = "**"
        text_type = TextType.BOLD

        expected = [
            TextNode("This is text without delimiters", TextType.NORMAL),
        ]

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_matches(self):
        old_nodes = [TextNode("This is text with **bolded phrase** and *italicized phrase* in the middle", TextType.NORMAL)]
        delimiter = "**"
        text_type = TextType.BOLD

        expected = [
            TextNode("This is text with ", TextType.NORMAL),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" and *italicized phrase* in the middle", TextType.NORMAL),
        ]

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
