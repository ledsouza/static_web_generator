import unittest
from markdown_htmlnode import markdown_to_html_node
from htmlnode import HTMLNode

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraph(self):
        markdown = "This is a paragraph."
        expected = HTMLNode("p", "This is a paragraph.")
        result = markdown_to_html_node(markdown)[0]
        self.assertEqual(result, expected)

    def test_heading(self):
        markdown = "## This is a heading"
        expected = HTMLNode("h2", "This is a heading")
        result = markdown_to_html_node(markdown)[0]
        self.assertEqual(result, expected)

    def test_code(self):
        markdown = "```\nprint('Hello, world!')\n```"
        expected = HTMLNode("code", "print('Hello, world!')")
        result = markdown_to_html_node(markdown)[0]
        self.assertEqual(result, expected)

    def test_quote(self):
        markdown = "> This is a quote."
        expected = HTMLNode("blockquote", " This is a quote.")
        result = markdown_to_html_node(markdown)[0]
        self.assertEqual(result, expected)

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        expected = HTMLNode("ul", children=[
            HTMLNode("li", "Item 1"),
            HTMLNode("li", "Item 2")
        ])
        result = markdown_to_html_node(markdown)[0]
        self.assertEqual(result, expected)

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2"
        expected = HTMLNode("ol", children=[
            HTMLNode("li", "Item 1"),
            HTMLNode("li", "Item 2")
        ])
        result = markdown_to_html_node(markdown)[0]
        self.assertEqual(result, expected)

    def test_multiple_blocks(self):
        markdown = "# Heading\n\nParagraph\n\n```\ncode\n```"
        expected = [
            HTMLNode("h1", "Heading"),
            HTMLNode("p", "Paragraph"),
            HTMLNode("code", "code")
        ]
        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()