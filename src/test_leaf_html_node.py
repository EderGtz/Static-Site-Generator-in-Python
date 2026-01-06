import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_with_dif_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertNotEqual(node.to_html(), '<a>Click me!</a>')

    def test_no_tag_with_props(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")
    
    def test_only_value(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), "Click me!")
        
if __name__ == "__main__":
    unittest.main()
