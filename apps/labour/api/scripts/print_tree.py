import sys
from pathlib import Path

def print_py_tree(directory, prefix="", is_last=True):
    """
    Recursively print a directory tree of Python files.
    
    Args:
        directory (Path): The directory to print
        prefix (str): Prefix for the current line
        is_last (bool): Whether this is the last item in its parent directory
    """
    branch = "└── " if is_last else "├── "
    
    dir_name = directory.name
    
    print(f"{prefix}{branch}{dir_name}/")
    
    new_prefix = prefix + ("    " if is_last else "│   ")
    
    items = list(directory.iterdir())
    
    dirs = sorted([item for item in items if item.is_dir() and not item.name.startswith(".")])
    files = sorted([item for item in items if item.is_file() and item.suffix == '.py'])
    
    for i, dir_path in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1) and len(files) == 0
        print_py_tree(dir_path, new_prefix, is_last_dir)
    
    for i, file_path in enumerate(files):
        is_last_file = i == len(files) - 1
        file_branch = "└── " if is_last_file else "├── "
        print(f"{new_prefix}{file_branch}{file_path.name}")

def main():
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path('.')
    
    if not root_dir.is_dir():
        print(f"Error: '{root_dir}' is not a valid directory")
        sys.exit(1)
    
    print(f"Python files in {root_dir.absolute()}:")
    print_py_tree(root_dir)

if __name__ == "__main__":
    main()