import unittest

from block_markdown import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks,
    block_to_block_type
)

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown = '''This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items'''
        expected_blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]

        result_blocks = markdown_to_blocks(markdown)

        self.assertEqual(expected_blocks, result_blocks)

    def test_markdown_to_blocks_newlines(self):
        md = """This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        block = "# Heading"
        expected_type = block_type_heading
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should identify heading")

        block = "###### Subheading"
        expected_type = block_type_heading
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should handle headings with up to 6 # symbols")

    def test_code(self):
        block = "```python\nprint('Hello, world!')\n```"
        expected_type = block_type_code
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should identify code block")

        block = "```\npython\nprint('Hello, world!')\n```"
        expected_type = block_type_code
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should identify code block with beginning line break")

    def test_quote(self):
        block = "> This is a quote."
        expected_type = block_type_quote
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should identify quote")

    def test_unordered_list(self):
        block = "* Item 1"
        expected_type = block_type_unordered_list
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should identify unordered list item")

        block = "- Item 2"
        expected_type = block_type_unordered_list
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should handle both * and - as list markers")

    def test_ordered_list(self):
        block = "1. Item in ordered list"
        expected_type = block_type_ordered_list
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should identify ordered list item")

        block = "2. Another item"
        expected_type = block_type_ordered_list
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should handle different starting numbers")

    def test_paragraph(self):
        block = "This is a paragraph."
        expected_type = block_type_paragraph
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should identify paragraph by default")

        block = "Another paragraph with no specific formatting.\nAnother paragraph"
        expected_type = block_type_paragraph
        actual_type = block_to_block_type(block)
        self.assertEqual(actual_type, expected_type, "Should handle various paragraph content")

if __name__ == "__main__":
    unittest.main()