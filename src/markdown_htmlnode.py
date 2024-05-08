
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
from htmlnode import HTMLNode

def block_to_htmlnode(block):
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

def handle_paragraph(block):
    """Handles a paragraph block."""
    tag = "p"
    value = block
    return HTMLNode(tag, value)

def handle_heading(block):
    """Handles a heading block."""
    heading_level = block.count("#")
    block.remove("#")
    tag = f"h{heading_level}"
    value = block.strip()
    return HTMLNode(tag, value)

def handle_code(block):
    """Handles a code block."""
    block.remove("```")
    tag = "code"
    value = block.strip()
    return HTMLNode(tag, value)

def handle_quote(block):
    """Handles a quote block."""
    block.remove(">")
    tag = "blockquote"
    value = block
    return HTMLNode(tag, value)

def handle_list(block, list_type):
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
