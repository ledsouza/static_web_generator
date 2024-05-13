import re
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node

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
    return ParentNode("div", children)

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Splits a markdown string into separate blocks based on double newlines,
    then removes trailing whitespace and any resulting empty blocks.

    Args:
        markdown: The input markdown text.

    Returns:
        A list of strings where each string represents a block of text.
    """
    blocks = markdown.split("\n\n")

    def remove_trailing(block):
        return block.strip()
    blocks = list(map(remove_trailing, blocks))
    
    if "" in blocks:
        blocks.remove("")
    
    return blocks

def block_to_html_node(block: str) -> ParentNode:
    """
    Converts a markdown block into an equivalent HTML string representation.

    This function determines the type of markdown block (paragraph, heading, code, quote, list) and delegates the conversion to specialized handler functions.

    Args:
        block: The markdown block text to be converted.

    Returns:
        The HTML string representation of the input markdown block.

    Raises:
        ValueError: If the input block does not match any of the recognized markdown block types.
    """
    block_type = block_to_block_type(block)

    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    elif block_type == block_type_heading:
        return heading_to_html_node(block)
    elif block_type == block_type_code:
        return code_to_html_node(block)
    elif block_type == block_type_quote:
        return quote_to_html_node(block)
    elif block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    elif block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    else:
        raise ValueError("Invalid block type")
    
def block_to_block_type(block: str) -> str:
    """
    Determines the type of a markdown block based on its content.

    This function examines the structure and initial characters of a given markdown block to identify 
    its type. It supports the following block types:

    * block_type_heading: Lines starting with one to six '#' characters.
    * block_type_code: Lines enclosed by triple backticks (```).
    * block_type_quote: Lines starting with '>'.
    * block_type_unordered_list: Lines starting with '*' or '-'.
    * block_type_ordered_list: Lines starting with a digit followed by a dot (e.g., "1.").
    * block_type_paragraph: Any block not matching the above types.

    Args:
        block: The markdown block as a string.

    Returns:
        A string representing the determined block type.

    Examples:
        block_to_block_type("# Heading")  # Returns 'block_type_heading'
        block_to_block_type("```\nprint('Hello')\n```")  # Returns 'block_type_code'
        block_to_block_type("* List item")  # Returns 'block_type_unordered_list'
    """
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
    
def text_to_children(text: str) -> list[LeafNode]:
    """
    Converts raw text into a list of HTML leaf nodes (e.g., representing text, images, links).

    Args:
        text: The input raw text.

    Returns:
        A list of LeafNodes, each representing an element within the parsed text.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block: str) -> ParentNode:
    """
    Converts a paragraph of text into an HTML <p> node.

    Args:
        block: The text block representing the paragraph.

    Returns:
        A ParentNode representing the <p> tag and its child nodes.
    """
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block: str) -> ParentNode:
    """
    Converts a markdown heading into an HTML heading node (e.g., <h1>, <h2>, etc.).

    Args:
        block: The text block representing the heading, including '#' characters.

    Returns:
        A ParentNode representing the appropriate heading tag and its content.

    Raises:
        ValueError: If the heading level is invalid (greater than 6).
    """
    heading_level = block.count("#")
    if heading_level > 6:
        raise ValueError(f"Invalid heading level: {heading_level}")
    block = block.replace("#", "")
    text = block.strip()
    tag = f"h{heading_level}"
    children = text_to_children(text)
    return ParentNode(tag, children)

def code_to_html_node(block: str) -> ParentNode:
    """
    Converts a markdown code block into HTML <pre><code> nodes.

    Args:
        block: The text block representing the code, enclosed in "```".

    Returns:
        A ParentNode representing the <pre> tag, containing a <code> node with the code content.

    Raises:
        ValueError: If the code block is not properly enclosed with "```".
    """
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block.replace("```", "").strip()
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_to_html_node(block: str) -> ParentNode:
    """
    Converts a markdown quote block into an HTML <blockquote> node.

    Args:
        block: The text block representing the quote, with each line starting with '>'.

    Returns:
        A ParentNode representing the <blockquote> tag and its content.

    Raises:
        ValueError: If a line within the block does not start with '>'.
    """
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def olist_to_html_node(block: str) -> ParentNode:
    """
    Converts a markdown ordered list into an HTML <ol> node.

    Args:
        block: The text block representing the ordered list, with each item starting with a number and a period.

    Returns:
        A ParentNode representing the <ol> tag and its child <li> nodes.
    """
    items = block.split("\n")
    html_items = []
    for item in items:
        text = re.sub(r"^\d+\.", "", item).strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block: str) -> ParentNode:
    """
    Converts a markdown unordered list into an HTML <ul> node.

    Args:
        block: The text block representing the unordered list, with each item starting with '*' or '-'.

    Returns:
        A ParentNode representing the <ul> tag and its child <li> nodes.
    """
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.lstrip("*").lstrip("-").strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)
