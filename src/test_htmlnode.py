import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a div", [], {"class": "container"})
        node2 = HTMLNode("div", "This is a div", [], {"class": "container"})
        self.assertEqual(node, node2)
    
    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", [], {"class": "container"})
        self.assertEqual(node.props_to_html(), 'class="container"')

    def test_props_to_html_empty(self):
        node = HTMLNode("div", "This is a div", [], {})
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()
