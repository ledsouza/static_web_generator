import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello, world!", children=[HTMLNode("p", "This is a paragraph")], id="my-div")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].value, "This is a paragraph")
        self.assertEqual(node.props["id"], "my-div")

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, world!", id="my-div", class_name="container")
        props_html = node.props_to_html()
        expected_props_html = ' id="my-div" class_name="container"'
        self.assertEqual(props_html, expected_props_html)

    def test_repr(self):
        node = HTMLNode("div", "Hello, world!", id="my-div", class_name="container")
        expected_props = {"id": "my-div", "class_name": "container"}
        repr_str = repr(node)
        expected_repr_str = f"HTMLNode(div, Hello, world!, None, {expected_props})"
        self.assertEqual(repr_str, expected_repr_str)

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode(tag="div", value="Hello, world!", id="my-div")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.props["id"], "my-div")

    def test_to_html_with_value(self):
        node = LeafNode(tag="div", value="Hello, world!", id="my-div")
        html = node.to_html()
        expected_html = '<div id="my-div">Hello, world!</div>'
        self.assertEqual(html, expected_html)

    def test_to_html_without_value(self):
        node = LeafNode(tag="div", value=None, id="my-div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode(tag="div", value="Hello, world!", id="my-div")
        expected_props = {"id": "my-div"}
        repr_str = repr(node)
        expected_repr_str = f"LeafNode(div, Hello, world!, {expected_props})"
        self.assertEqual(repr_str, expected_repr_str)

class TestParentNode(unittest.TestCase):
    def test_init(self):
        node = ParentNode("div", children=[LeafNode("p", "This is a paragraph")], id="my-div")
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].value, "This is a paragraph")
        self.assertEqual(node.props["id"], "my-div")

    def test_to_html(self):
        node = ParentNode("div", children=[LeafNode("p", "This is a paragraph")], id="my-div")
        html = node.to_html()
        expected_html = '<div id="my-div"><p>This is a paragraph</p></div>'
        self.assertEqual(html, expected_html)

    def test_to_html_2_leaf_children(self):
        node = ParentNode("div", children=[LeafNode("p", "This is a paragraph"), LeafNode("p", "This is another paragraph")], id="my-div")
        html = node.to_html()
        expected_html = '<div id="my-div"><p>This is a paragraph</p><p>This is another paragraph</p></div>'
        self.assertEqual(html, expected_html)

    def test_to_html_2_parent_children(self):
        node = ParentNode(
            "div",
            children=[
                ParentNode("p", children=[LeafNode("span", "This is a span")]),
                ParentNode("p", children=[LeafNode("span", "This is another span")]),
            ],
            id="my-div",
        )
        html = node.to_html()
        expected_html = '<div id="my-div"><p><span>This is a span</span></p><p><span>This is another span</span></p></div>'
        self.assertEqual(html, expected_html)

    def test_to_html_4_leaf_children(self):
        node = ParentNode(
            "p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        html = node.to_html()
        expected_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(html, expected_html)

    def test_to_html_no_tag(self):
        node = ParentNode(None, children=[LeafNode("p", "This is a paragraph")], id="my-div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", children=None, id="my-div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_children_with_no_value(self):
        node = ParentNode("div", children=[LeafNode("p", None)], id="my-div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = ParentNode("div", children=[LeafNode("p", "This is a paragraph")], id="my-div")
        expected_props = {"id": "my-div"}
        repr_str = repr(node)
        expected_repr_str = f"ParentNode(div, None, {node.children}, {expected_props})"
        self.assertEqual(repr_str, expected_repr_str)


if __name__ == "__main__":
    unittest.main()
