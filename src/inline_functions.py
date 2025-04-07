import re
from nodes import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_by_pattern(old_nodes, extract_function, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        matches = extract_function(original_text)

        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        for match in matches:
            sections = []
            if text_type == TextType.IMAGE:
                sections = original_text.split(f"![{match[0]}]({match[1]})", 1)
            else:
                sections = original_text.split(f"[{match[0]}]({match[1]})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(match[0], text_type, match[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_by_pattern(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_by_pattern(old_nodes, extract_markdown_links, TextType.LINK)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
