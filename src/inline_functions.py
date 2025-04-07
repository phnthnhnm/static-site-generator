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

def split_nodes_by_extractor(
    old_nodes: list[TextNode],
    extractor: callable,
    text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        text = node.text
        extracted_items = extractor(text)

        if not extracted_items:
            new_nodes.append(node)
            continue

        last_end = 0

        for item_text, url in extracted_items:
            start = text.find(f"[{item_text}]({url})", last_end)
            if text_type == TextType.IMAGE:
                start = text.find(f"![{item_text}]({url})", last_end)
            end = start + len(f"[{item_text}]({url})")

            if text_type == TextType.IMAGE:
                end = start + len(f"![{item_text}]({url})")

            if start > last_end:
                segment = text[last_end:start]
                if segment:
                    new_nodes.append(TextNode(segment, TextType.NORMAL))

            new_nodes.append(TextNode(item_text, text_type, url))
            last_end = end

        if last_end < len(text):
            segment = text[last_end:]
            if segment:
                new_nodes.append(TextNode(segment, TextType.NORMAL))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_extractor(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_extractor(old_nodes, extract_markdown_links, TextType.LINK)

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.NORMAL)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

