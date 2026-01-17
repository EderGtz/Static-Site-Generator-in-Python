"""This module converts a full markdown document into a single parent node
of HTML, including child HTML nodes that represent nested tags"""

from md_blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode
from md_inline_converter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(md_document):
    """Convert a full Markdown document into a single parent HTML node."""
    md_document_blocks = markdown_to_blocks(md_document)
    children = []
    for block in md_document_blocks:
        html_node = create_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def md_inline_to_html(text):
    """Convert inline Markdown text into a list of HTML nodes."""
    nodes = text_to_textnodes(text)
    list_of_nodes = []
    for node in nodes:
        list_of_nodes.append(text_node_to_html_node(node))
    return list_of_nodes

def create_html_node(text):
    """Dispatch a Markdown block to its corresponding HTML node creator."""
    block_type = block_to_block_type(text)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(text)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(text)
    elif block_type == BlockType.CODE:
        return code_to_html_node(text)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(text)
    elif block_type == BlockType.UNORDERED_LIST:
        return unorderedlist_to_html_node(text)
    elif block_type == BlockType.ORDERED_LIST:
        return orderedlist_to_html_node(text)
    else:
        raise ValueError("No compatible format")

def paragraph_to_html_node(text):
    """Convert a paragraph block into a <p> HTML node."""
    children = md_inline_to_html(text.replace("\n", " "))
    return ParentNode("p", children=children)

def heading_to_html_node(text):
    """Convert a heading block into an <hX> HTML node."""
    h_counter = 0
    for letter in text:
        if letter != "#":
            break
        h_counter += 1
    heading_text = text[h_counter:].lstrip()
    children = md_inline_to_html(heading_text)
    return ParentNode(f"h{h_counter}", children=children)

def code_to_html_node(text):
    """Convert a code block into <pre><code> HTML nodes."""        
    text = text[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(text):
    """Convert a blockquote block into a <blockquote> HTML node."""
    lines = text.split("\n")
    final = []
    for quote in lines:
        #quote = quote.replace(">", "")
        quote = quote.lstrip(" >")
        final.append(quote)
    final = (" ".join(final))
    children = md_inline_to_html(final)
    return ParentNode("blockquote", children=children) 

def unorderedlist_to_html_node(text):
    """Convert an unordered list block into a <ul> HTML node."""
    children = []
    items = text.split("\n")
    for li_content in items:
        text_of_element = li_content[2:]
        current_children = md_inline_to_html(text_of_element)
        children.append(ParentNode("li", current_children))
    return ParentNode("ul", children)

def orderedlist_to_html_node(text):
    """Convert an ordered list block into an <ol> HTML node."""
    children = []
    items = text.split("\n")
    for li_content in items:
        i = 1
        for letter in li_content:
            if letter == " ":
                break
            i += 1
        current_children = md_inline_to_html(li_content[i:])
        children.append(ParentNode("li", current_children))
    return ParentNode("ol", children)
