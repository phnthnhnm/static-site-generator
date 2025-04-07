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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images(
            "This is text without an image."
        )
        self.assertListEqual([], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links(
            "This is text without a link."
        )
        self.assertListEqual([], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_image_no_match(self):
        node = TextNode(
            "This is text without an image.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_multiple_images_only(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png)![image2](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_mixed_content(self):
        node = TextNode(
            "Text before ![image1](https://i.imgur.com/zjjcJKZ.png) and text after.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.NORMAL),
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and text after.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_no_normal_text(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_no_match(self):
        node = TextNode(
            "This is text without a link.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without a link.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_multiple_links_only(self):
        node = TextNode(
            "[link1](https://example.com)[link2](https://example.org)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode("link2", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_mixed_content(self):
        node = TextNode(
            "Text before [link1](https://example.com) and text after.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.NORMAL),
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode(" and text after.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_no_normal_text(self):
        node = TextNode(
            "[link1](https://example.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_basic(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected_nodes)

    def test_text_to_textnodes_no_formatting(self):
        text = "This is plain text with no formatting."
        expected_nodes = [
            TextNode("This is plain text with no formatting.", TextType.NORMAL),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected_nodes)

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text."
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.NORMAL),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected_nodes)

    def test_text_to_textnodes_only_italic(self):
        text = "This is _italic_ text."
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.NORMAL),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected_nodes)

    def test_text_to_textnodes_only_code(self):
        text = "This is `code` text."
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.NORMAL),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected_nodes)

    def test_text_to_textnodes_images_and_links(self):
        text = "![image](https://example.com/image.png) and [link](https://example.com)"
        expected_nodes = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected_nodes)

if __name__ == "__main__":
    unittest.main()
