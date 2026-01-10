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
    if md_block.startswith("#"):
        heading_counter = 0
        for i in range(len(md_block)):
            if md_block[i] == "#":
                heading_counter += 1
                continue
            if md_block[i] == " " and 1 <= heading_counter <= 6:
                return BlockType.HEADING
            #Avoiding to loop over the whole string if the first non-#
            #character is not a space
            break
    #code
    if md_block.startswith("```\n") and md_block.endswith("```"):
        return BlockType.CODE
    #quote
    block_splitted = md_block.split("\n")
    is_valid = True
    for line in block_splitted:
        if line == "":
            continue
        if not line.startswith("> "):
            is_valid = False
            break
    if is_valid is True:
        return BlockType.QUOTE
    #unordered list
    is_valid = True
    for line in block_splitted:
        if line == "":
            continue
        if not line.startswith("- "):
            is_valid = False
            break
    if is_valid is True:
        return BlockType.UNORDERED_LIST
    #ordered list
    is_valid = True
    counter = 0
    for line in block_splitted:
        if line == "":
            continue
        counter += 1
        if not line.startswith(f"{counter}. "):
            is_valid = False
            break
    if is_valid is True:
        return BlockType.ORDERED_LIST
    #If none of above are met, is a normal paragraph
    return BlockType.PARAGRAPH