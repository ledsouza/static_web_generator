import re

from block_markdown import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    block_to_block_type,
    markdown_to_blocks
)
from htmlnode import HTMLNode, ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block: str):
    """Converts a Markdown block to an HTML node."""
    block_type = block_to_block_type(block)

    if block_type == block_type_paragraph:
        return handle_paragraph(block)
    elif block_type == block_type_heading:
        return handle_heading(block)
    elif block_type == block_type_code:
        return handle_code(block)
    elif block_type == block_type_quote:
        return handle_quote(block)
    elif block_type == block_type_unordered_list:
        return handle_list(block, "ul")
    elif block_type == block_type_ordered_list:
        return handle_list(block, "ol")

def handle_paragraph(block: str):
    """Handles a paragraph block."""
    tag = "p"
    value = block
    return HTMLNode(tag, value)

def handle_heading(block: str):
    """Handles a heading block."""
    heading_level = block.count("#")
    block = block.replace("#", "")
    tag = f"h{heading_level}"
    value = block.strip()
    return HTMLNode(tag, value)

def handle_code(block: str):
    """Handles a code block."""
    block = block.replace("```", "")
    tag = "code"
    value = block.strip()
    return HTMLNode(tag, value)

def handle_quote(block: str):
    """Handles a quote block."""
    block = block.replace(">", "")
    tag = "blockquote"
    value = block
    return HTMLNode(tag, value)

def handle_list(block: str, list_type: str):
    """Handles both ordered and unordered lists."""
    lines = block.split("\n")
    children = []
    for line in lines:
        if list_type == "ol":
            line = re.sub(r"^\d+\.", "", line) 
        else:  # Unordered list
            line = line.lstrip("*").lstrip("-") 
        children.append(HTMLNode(tag="li", value=line.strip()))
    return HTMLNode(tag=list_type, children=children)
