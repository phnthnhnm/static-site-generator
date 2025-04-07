import os
import shutil
from block_functions import markdown_to_html_node

def copy_directory(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            os.mkdir(dest_path)
            copy_directory(src_path, dest_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()

        if line.startswith('# ') and len(line) > 2:
            return line[2:].strip()
        
    raise Exception("No h1 header found in the markdown content")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(full_html)
