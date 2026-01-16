import os
from md_to_html import markdown_to_html_node
from md_inline_converter import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise Exception("The source file does not exists")
    
    #In case the given dest does not exists, it is created
    dest_directories = os.path.dirname(dest_path)
    if not os.path.exists(dest_directories):
        os.makedirs(dest_directories, exist_ok=True)

    with open(from_path, "r") as f:
        md_file = f.read()
        md_converted = markdown_to_html_node(md_file).to_html()
        md_title = extract_title(md_file)

        with open(template_path, "r") as f:
            html_template = f.read()
            title_replaced = html_template.replace("{{ Title }}", md_title)
            final_html = title_replaced.replace("{{ Content }}", md_converted)
            with open(dest_path, "w") as f:
                f.write(final_html)
