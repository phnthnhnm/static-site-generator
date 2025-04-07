import re
from nodes import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if not delimiter:
        raise ValueError("Delimiter cannot be an empty string.")
    
    new_nodes: list[TextNode] = []
    pattern = re.escape(delimiter)  # Escape special characters in the delimiter
    regex = re.compile(f"{pattern}(.*?){pattern}")  # Match text between delimiters

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        text = node.text
        last_end = 0

        for match in regex.finditer(text):
            start, end = match.span()
            # Add text before the delimiter
            if start > last_end:
                new_nodes.append(TextNode(text[last_end:start], TextType.NORMAL))
            # Add text between the delimiters
            new_nodes.append(TextNode(match.group(1), text_type))
            last_end = end

        # Add remaining text after the last match
        if last_end < len(text):
            new_nodes.append(TextNode(text[last_end:], TextType.NORMAL))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
