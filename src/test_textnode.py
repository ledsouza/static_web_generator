import unittest
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(
            repr(node), "TextNode(This is a text node, bold, https://www.boot.dev)"
        )

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_with_different_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev2")
        self.assertNotEqual(node, node2)

    def test_eq_with_different_text(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node2", "bold", "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_with_different_text_type(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold2", "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_with_different_text_and_text_type(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node2", "bold2", "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_with_different_text_and_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node2", "bold", "https://www.boot.dev2")
        self.assertNotEqual(node, node2)

    def test_eq_with_different_text_type_and_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold2", "https://www.boot.dev2")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
