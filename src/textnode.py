"""
The classes declared here are the way to represent all different types of
inline text used in md text. This is to store the information of every
line to turn them to HTML
"""
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold "
    ITALIC = "italic "
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
#This nodes represent the types of inline text that exist in HTML and MD
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
    

