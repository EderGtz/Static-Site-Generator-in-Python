"""This module works over inputs of md documents, and returns lists
of blocks strings
"""
from enum import Enum

#The specific types of md blocks admited
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered list"

#Takes a document and splitted it into blocks of strings
def markdown_to_blocks(text):
    blocks_splitted = text.split("\n\n")
    filtered_blocks = []
    for block in blocks_splitted:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

#Returns the type of block that was introduced
def block_to_block_type(md_block):
    #heading
    if md_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    #code. Does not consider a \n after the first ```, because you can specify the lenguage there
    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    #quote
    block_splitted = md_block.split("\n")
    if md_block.startswith("> "):
        for line in block_splitted:
            if line == "":
                continue
            if not line.startswith("> "):
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