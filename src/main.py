import os
import shutil


def main() -> None:
    path = "static"
    destination = "public"
    copy_files(path, destination)

def copy_files(path, destination):
    if not os.path.exists(destination) and not os.path.isfile(path):
        os.mkdir(destination)
    if os.path.exists(path) and os.path.isfile(path):
        shutil.copy(path, destination)
        print(f"{path} copied into {destination}")
    elif os.path.exists(path) and not os.path.isfile(path):
        new_paths = os.listdir(path)
        for new_path in new_paths:
            copy_files(os.path.join(path, new_path), os.path.join(destination, new_path))

if __name__ == "__main__":
    main()