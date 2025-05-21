import os
import shutil
from typing import List, Optional

def list_directory(path: str) -> List[str]:
    return os.listdir(path)

def create_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def delete_file(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)

def delete_directory(path: str) -> None:
    if os.path.isdir(path):
        shutil.rmtree(path)

def move_file(src: str, dst: str) -> None:
    shutil.move(src, dst)

def copy_file(src: str, dst: str) -> None:
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

def get_file_size(path: str) -> Optional[int]:
    if os.path.isfile(path):
        return os.path.getsize(path)
    return None

def get_absolute_path(path: str) -> str:
    return os.path.abspath(path)

def rename_path(src: str, dst: str) -> None:
    os.rename(src, dst)

def is_directory(path: str) -> bool:
    return os.path.isdir(path)

def is_file(path: str) -> bool:
    return os.path.isfile(path)

def path_exists(path: str) -> bool:
    return os.path.exists(path)

def get_metadata(path: str) -> Optional[dict]:
    try:
        stat = os.stat(path)
        return {
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "accessed": stat.st_atime,
            "mode": stat.st_mode
        }
    except Exception:
        return None
    
def copy_directory(src: str, dst: str) -> None:
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        raise ValueError(f"{src} is not a directory.")