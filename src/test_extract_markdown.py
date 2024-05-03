import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = """
        # Hello, world!
        
        This is a paragraph with an image ![alt text](https://www.example.com/image.jpg)
        """
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt text", "https://www.example.com/image.jpg")])

    def test_extract_markdown_links(self):
        text = """
        # Hello, world!
        
        This is a paragraph with a link [link text](https://www.example.com)
        """
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link text", "https://www.example.com")])