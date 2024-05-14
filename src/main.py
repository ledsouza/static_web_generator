import os
import shutil
from block_markdown import markdown_to_html_node


def main() -> None:
    generate_page("content/index.md", "template.html", "public/index.html")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read files from_path and template_path
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )

    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w") as html_file:
        html_file.write(template_content)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.replace("# ", "")


def copy_files(src_path: str, dst_path: str) -> None:
    """Recursively copies files and directories from src_path to dst_path."""
    try:
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)  # Copy with metadata
            print(f"Copied file: {src_path} to {dst_path}")
        elif os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            for item in os.listdir(src_path):
                src_item = os.path.join(src_path, item)
                dst_item = os.path.join(dst_path, item)
                copy_files(src_item, dst_item)  # Recursive call
        else:
            raise FileNotFoundError(f"Invalid path: {src_path}")

    except PermissionError as e:
        print(f"Error: Insufficient permissions - {e}")
    except (shutil.Error, FileNotFoundError) as e:
        print(f"Error copying files: {e}")


if __name__ == "__main__":
    main()
