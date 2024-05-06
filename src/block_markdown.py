import re

# Block types
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")

    def remove_trailing(block):
        return block.strip()
    blocks = list(map(remove_trailing, blocks))
    
    if "" in blocks:
        blocks.remove("")
    
    return blocks

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