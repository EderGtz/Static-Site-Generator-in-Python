import unittest
from htmlnode import HTMLNode

properties_test = {
    "href": "https://www.google.com",
    "target": "_blank",
}

class TestHTMLNode(unittest.TestCase):

    def test_eq_nodes(self):
        node = HTMLNode("p", "Hello there", None, properties_test)
        node2 = HTMLNode("p", "Hello there", None, properties_test)
        self.assertEqual(node, node2)
    
    def test_noteq_nodes(self):
        node = HTMLNode("p", "Hello son", None, properties_test)
        node2 = HTMLNode("p", "Hello there", None, properties_test)
        self.assertNotEqual(node, node2)
    
    def test_tag_diff(self):
        node = HTMLNode("a", "Hello son", None, properties_test)
        node2 = HTMLNode("p", "Hello there", None, properties_test)
        self.assertNotEqual(node, node2)
    
    def test_props_diff(self):
        node = HTMLNode("a", "Hello son", None, {})
        node2 = HTMLNode("p", "Hello there", None, properties_test)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = HTMLNode("p", "Hello there", None, properties_test)
        self.assertEqual(repr(node), 
        'HTMLNode(p, Hello there, None,  href="https://www.google.com" target="_blank")')


if __name__ == "__main__":
    unittest.main()