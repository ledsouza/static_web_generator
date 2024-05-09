import re

from htmlnode import ParentNode, HTMLNode
from inline_markdown import text_to_textnodes

# Block types
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")

    def remove_trailing(block):
        return block.strip()
    blocks = list(map(remove_trailing, blocks))
    
    if "" in blocks:
        blocks.remove("")
    
    return blocks

def block_to_html_node(block: str):
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
    else:
        raise ValueError("Invalid block type")
    
def block_to_block_type(block: str):
    if re.search(r"^#{1,6}", block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if block.startswith(">"):
        return block_type_quote
    if block.startswith("* ") or block.startswith("- "):
        return block_type_unordered_list
    if re.search(r"^\d.", block):
        return block_type_ordered_list
    else:
        return block_type_paragraph
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

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
