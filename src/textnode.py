from htmlnode import LeafNode
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link
)

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode():
    '''
    Purpose: Represents a single piece of text content with associated formatting and optional URL link.

    Attributes:
        text (str): The text content of the node
        text_type (str): The type of text this node contains, which is just a string like "bold" or "italic"
        url (str, optional): The URL of the link or image, if the text is a link. Default to None if nothing is passed in.
    '''
    def __init__(self, text: str, text_type: str, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        '''
        Defines equality comparison between TextNode objects. 
        Two TextNodes are considered equal if their text, text_type, and url attributes are the same.
        '''
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )
    
    def __repr__(self) -> str:
        '''
        Provides a string representation for debugging.
        '''
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    '''
    Purpose: Converts a TextNode object into an equivalent representation suitable 
    for HTML rendering (assumed to be a LeafNode object).

    Parameters:
        text_node (TextNode): The input TextNode object.
    
    Returns:
        LeafNode: An object representing a leaf node in an HTML structure.
    '''
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, href=text_node.url)
    elif text_node.text_type == text_type_image:
        return LeafNode("img", "", src=text_node.url, alt=text_node.text)
    raise ValueError("The TextNode has invalid text type")

def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts a raw text string into a list of TextNodes, parsing common markdown elements.

    Args:
        text: The input text string.

    Returns:
        A list of TextNodes representing the parsed text, including bold, italic, code, images, and links.
    """
    node = TextNode(text, text_type_text)
    first_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    second_nodes = split_nodes_delimiter(first_nodes, "*", text_type_italic)
    third_nodes = split_nodes_delimiter(second_nodes, "`", text_type_code)
    fourth_nodes = split_nodes_image(third_nodes)
    final_nodes = split_nodes_link(fourth_nodes)

    return final_nodes
