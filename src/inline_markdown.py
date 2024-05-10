
import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    """
    Splits TextNodes based on a delimiter for inline elements, 
    creating new TextNodes with the specified text_type.

    Args:
        old_nodes: The list of TextNodes to be split.
        delimiter: The delimiter string (e.g., "**" for bold).
        text_type: The text type to be assigned to the newly created TextNodes.

    Returns:
        A new list of TextNodes after the splitting process.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNodes containing markdown image syntax into separate TextNodes.

    Args:
        old_nodes: The list of TextNodes to be processed.

    Returns:
        A new list of TextNodes with image sections split out.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNodes containing markdown link syntax into separate TextNodes.

    Args:
        old_nodes: The list of TextNodes to be processed.

    Returns:
        A new list of TextNodes with link sections split out.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extracts image references (alt text and URL) from markdown text.

    Args:
        text: The input markdown text.
    Returns:
        A list of tuples where each tuple contains the alt text and URL of an image.
    """
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extracts link references (link text and URL) from markdown text.

    Args:
        text: The input markdown text.
    Returns:
        A list of tuples where each tuple contains the link text and URL of a link.
    """
    return re.findall(r'\[(.*?)\]\((.*?)\)', text)