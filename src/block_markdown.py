def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    def remove_trailing(block):
        return block.strip()
    blocks = list(map(remove_trailing, blocks))
    
    if "" in blocks:
        blocks.remove("")
    
    return blocks