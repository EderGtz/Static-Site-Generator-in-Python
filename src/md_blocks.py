"""This module works over inputs of md documents, and returns lists
of blocks strings
"""

#Takes a document and splitted it into blocks of strings
def markdown_to_blocks(text):
    text_splitted = text.split("\n\n")
    new_text = []
    for element in text_splitted:
        element = element.strip()
        if element == "":
            continue
        lines = element.split("\n")
        #Used loop comprehension to ommit inline spaces
        cleaned = "\n".join(line.strip() for line in lines)
        new_text.append(cleaned)
    return new_text
