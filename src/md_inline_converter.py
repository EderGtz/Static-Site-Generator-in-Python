import re
from textnode import TextNode, TextType

#Converts raw strings of md into a list of TextNode objects
def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    bold_removed = split_nodes_delimiter([text_node],"**", TextType.BOLD)
    italic_removed = split_nodes_delimiter(bold_removed, "_", TextType.ITALIC)
    code_removed = split_nodes_delimiter(italic_removed, "`", TextType.CODE)
    link_removed = split_nodes_link(code_removed)
    final = split_nodes_image(link_removed)
    return final

'''
This function creates TextNodes from raw markdown strings by dividing 
the md string into multiple lines using a delimiter provided. The function
also ensures that the md string is valid, and this does not handle (still)
nested inline elements, like "_hello **there**_"
'''
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

#The regex pattern consist of two parts:
#\[([^\[\]]*)\]: Text inside [] symbols
#\(([^\(\)]*)\): Text inside () symbols, which is the link of the img
def extract_markdown_images(text):
    regex_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_pattern, text)

def extract_markdown_links(text):
    #almost exactly the same, but excluding the ! symbol to ensure is not a img
    regex_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_pattern, text)

#These functions split raw md text into TextNode's based on img and links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        extracted_images = extract_markdown_images(text)
        #The function would return an empty list if there are not img
        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue
        
        text_to_split = text
        for image_alt, image_link in extracted_images:
            #using a copy of the text so the variable is updated in every
            #iteration, making it possible to extract multiple images
            node_text, remaining_text = text_to_split.split(
                f"![{image_alt}]({image_link})", 1)
            if node_text != "":
                new_nodes.append(TextNode(node_text, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text_to_split = remaining_text
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        extracted_links = extract_markdown_links(text)
        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue
        text_to_split = text
        for link_text, link in extracted_links:
            node_text, remaining_text = text_to_split.split(
                f"[{link_text}]({link})", 1)
            if node_text != "":
                new_nodes.append(TextNode(node_text, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link))
            text_to_split = remaining_text
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes

"This function extract the h1 header from the md file, and return it"
def extract_title(md):
    if not md:
        raise ValueError("Invalid input")
    first_line = md.split("\n")[0]
    if not first_line.startswith("# "):
        raise Exception("md file should start with a tittle in #")
    return first_line.strip("# ").rstrip()