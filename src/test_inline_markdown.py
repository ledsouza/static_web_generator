import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

class TestSplitNodeImage(unittest.TestCase):
    def test_no_image(self):
        node = TextNode("This is text without an image", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_one_image(self):
        node = TextNode("This is text with an ![image](url)", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "url"),
            ],
            new_nodes,
        )
    
    def test_two_images(self):
        node = TextNode("This is text with an ![image](url) and another ![image2](url2)", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "url"),
                TextNode(" and another ", text_type_text),
                TextNode("image2", text_type_image, "url2"),
            ],
            new_nodes,
        )

    def test_two_sequential_images(self):
        node = TextNode("This is text with an ![image](url)![image](url)", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "url"),
                TextNode("image", text_type_image, "url"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        node1 = TextNode("This is text with an ![image](url)", text_type_text)
        node2 = TextNode("This is text with an ![image](url)", text_type_text)
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "url"),
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "url"),
            ],
            new_nodes,
        )

class TestSplitNodeLink(unittest.TestCase):
    def test_no_link(self):
        node = TextNode("This is text without a link", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_one_link(self):
        node = TextNode("This is text with a [link](url)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "url"),
            ],
            new_nodes,
        )
    
    def test_two_links(self):
        node = TextNode("This is text with a [link](url) and another [link2](url2)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "url"),
                TextNode(" and another ", text_type_text),
                TextNode("link2", text_type_link, "url2"),
            ],
            new_nodes,
        )

    def test_two_sequential_links(self):
        node = TextNode("This is text with a [link](url)[link2](url2)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "url"),
                TextNode("link2", text_type_link, "url2"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        node1 = TextNode("This is text with a [link](url)", text_type_text)
        node2 = TextNode("This is text with a [link2](url2)", text_type_text)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "url"),
                TextNode("This is text with a ", text_type_text),
                TextNode("link2", text_type_link, "url2"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    
    def test_empty_text(self):
        """Tests handling of empty text input."""
        text = ""
        expected_nodes = []
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)

    def test_single_text_node(self):
        """Tests processing of plain text."""
        text = "This is plain text."
        expected_nodes = [TextNode(text, text_type_text)]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)

    def test_bold_formatting(self):
        """Tests conversion of bold text."""
        text = "This has **bold** formatting."
        expected_nodes = [
            TextNode("This has ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" formatting.", text_type_text)
        ]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)

    def test_italic_formatting(self):
        """Tests conversion of italic text."""
        text = "This has *italic* formatting."
        expected_nodes = [
            TextNode("This has ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" formatting.", text_type_text)
        ]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)

    def test_code_formatting(self):
        """Tests conversion of code text."""
        text = "This has `code` formatting."
        expected_nodes = [
            TextNode("This has ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" formatting.", text_type_text)
        ]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)

    def test_combined_formatting(self):
        """Tests combined bold, italic, and code formatting."""
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]

        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()