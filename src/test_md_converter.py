import unittest
from md_inline_converter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_title
)  
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],new_nodes)
    
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual([
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ], new_nodes)
    
    def test_delim_double_bold(self):
        node = TextNode("**bold** and **another bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD)
        ], new_nodes)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ], new_nodes)
    
    def test_delim_bold_and_italic_intercalated(self):
        node = TextNode("**bold** and _italic_ and **bold again**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual([
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold again", TextType.BOLD)
        ], new_nodes)

    #Testing functions to transform links and images from md to dict of tuples
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_2_images(self):
        matches = extract_markdown_images(
            "his is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    def test_extract_markdown_2_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches
        )
#Testing split images function
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_img(self):
        node = TextNode("This is text without images",TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text without images", TextType.TEXT),],
            new_nodes,)

    def test_split_images_img_at_beggining(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) this was the img",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" this was the img", TextType.TEXT)
            ],
            new_nodes,)
        
    def test_split_images_image_node(self):
        nodes = [
            TextNode("Hello", TextType.TEXT),
            TextNode("already an image", TextType.IMAGE, "some_url"),
        ] 
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([
            TextNode("Hello", TextType.TEXT),
            TextNode("already an image", TextType.IMAGE, "some_url")
        ],new_nodes)

#Testing split links function
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
            "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
        ),
    ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode("This is text without images",TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text without images", TextType.TEXT),],
            new_nodes,)

    def test_split_links_link_at_beggining(self):
        node = TextNode(
            "[Link to boot dev](https://www.boot.dev) this was a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" this was a link", TextType.TEXT)
            ],
            new_nodes,)

    #Test the final function, which transforms raw text into TextNode object list
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected_nodes, text_to_textnodes(text))
    
    def test_text_link_to_textnodes(self):
        text = "[Link to boot dev](https://www.boot.dev) this was a link"
        self.assertListEqual(
            [TextNode("Link to boot dev", TextType.LINK, "https://www.boot.dev"), 
            TextNode(" this was a link", TextType.TEXT, None)]
        ,text_to_textnodes(text))

    def test_text_image_to_textnodes(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png) this was the img"
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" this was the img", TextType.TEXT)
            ],text_to_textnodes(text))
    
    def test_text_simple_to_textnodes(self):
        text = "%This% @is@ ?some? $random$ *text*. +Nothing+ 'else', -nothing- (less)"
        self.assertListEqual(
            [
                TextNode("%This% @is@ ?some? $random$ *text*. +Nothing+ 'else', -nothing- (less)", TextType.TEXT, None)
            ]
        , text_to_textnodes(text))
    
    def test_extract_title(self):
        text = "# Tolkien Fan Club"
        self.assertEqual("Tolkien Fan Club", extract_title(text))
    
    def test_extract_title_larger_input(self):
        text = """# Tolkien Fan Club 
![JRR Tolkien sitting](/images/tolkien.png)"""
        self.assertEqual("Tolkien Fan Club", extract_title(text))

if __name__ == "__main__":
    unittest.main()