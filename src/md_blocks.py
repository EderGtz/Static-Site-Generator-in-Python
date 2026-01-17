"""Module for parsing and classifying Markdown blocks, returning lists of block str."""

from enum import Enum

class BlockType(Enum):
    """Enum representing supported Markdown block categories."""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(text):
    """Split raw Markdown text into a list of cleaned block strings."""
    blocks_splitted = text.split("\n\n")
    filtered_blocks = []
    for block in blocks_splitted:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(md_block):
    """Determine the BlockType of a specific Markdown block string."""
    #heading
    if md_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    #code. Does not consider a \n after the first ```, because you can specify the lenguage there
    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    #quote
    block_splitted = md_block.split("\n")
    if md_block.startswith(">"):
        for line in block_splitted:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    #unordered list
    if md_block.startswith("- "):
        for line in block_splitted:
            if line == "":
                continue
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    #ordered list
    if md_block.startswith("1. "):
        counter = 1
        for line in block_splitted:
            if line == "":
                continue
            if not line.startswith(f"{counter}. "):
                return BlockType.PARAGRAPH
            counter += 1
        return BlockType.ORDERED_LIST
    #If none of above are met, is a normal paragraph
    return BlockType.PARAGRAPH
