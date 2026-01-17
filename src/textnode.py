"""
This is an intermediary step betweeen md text and html nodes.
The classes declared here are the way to represent all different types of
inline text used in md text. This is to store the information of every
line to turn them to HTML
"""
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    """Enum representing all supported inline text types."""
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """Class representing a piece of text with its associated formatting."""
    def __init__(self, text, text_type, url = None):
        self.text = text
        #text_type is a member or TextType enum
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            other.text == self.text 
            and other.text_type == self.text_type 
            and other.url == self.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    """Convert a TextNode instance into a LeafNode for HTML output."""
    text_node_value = text_node.text

    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node_value)
        case TextType.BOLD:
            return LeafNode("b", text_node_value)
        case TextType.ITALIC:
            return LeafNode("i", text_node_value)
        case TextType.CODE:
            return LeafNode("code", text_node_value)
        case TextType.LINK:
            return LeafNode("a",text_node_value, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "",
                    {"src": text_node.url,
                    "alt": text_node_value})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")