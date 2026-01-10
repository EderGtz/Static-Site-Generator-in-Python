import unittest
from md_blocks import BlockType, markdown_to_blocks, block_to_block_type

class TestMDBlocks(unittest.TestCase):

    def test_md_to_blocks_simple(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_md_to_blocks_multiple_lines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_md_to_blocks_spaces(self):
        md = """
    This is **bolded** paragraph

       This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    #testing block type converter
    def test_block_to_block_type_paragraph(self):
        text = "Hello there"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        text = "####### Hello there"
        self.assertNotEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_block_to_block_type_heading_2(self):
        text = "###### Hello there"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_block_to_block_type_heading_3(self):
        text = "######Hello there"
        self.assertNotEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        text = """```
        Hello there
        ```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_block_to_block_type_code_2(self):
        text = """```Hello there
        ```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_block_to_block_type_code_3(self):
        text = """```
        Hello there
        ``"""
        self.assertNotEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        text = "> There was a time\n> When I could sleep at 8 at clock every knight"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_block_to_block_type_quote_2(self):
        text = "> There was a time\n> When I could sleep at 8 at clock every knight"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_block_to_block_type_quote_3(self):
        text = ">There was a time\n> When I could sleep at 8 at clock every knight"
        self.assertNotEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_block_to_block_type_ul(self):
        text = "- Eggs\n- Bananas\n- Fruits"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ol(self):
        text = "1. Eggs\n2. Bananas\n3. Fruits"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)



if __name__ == "__main__":
    unittest.main()