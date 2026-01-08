'''
This function creates TextNodes from raw markdown strings by dividing 
the md string into multiple lines using a delimiter provided. The function
also ensures that the md string is valid, and this does not handle (still)
nested inline elements, like "_hello **there**_"
'''
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if len(parts) % 2 == 0:
            raise Exception("Invalid md syntax. There is a delimiter missing")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

#The following functions work over md images and links by extracting them 
#and creating a dictionary of tuples of the image description and the link.

#Text turn into alt text and url to url
def extract_markdown_images(text):
    regex_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_pattern, text)

def extract_markdown_links(text):
    #almost exactly the same, but excluding the ! symbol to ensure is not a img
    regex_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_pattern, text)

