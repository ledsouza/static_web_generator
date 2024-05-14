import os
import shutil


def main() -> None:
    path = "static"
    destination = "public"
    copy_files(path, destination)

def copy_files(src_path, dst_path):
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