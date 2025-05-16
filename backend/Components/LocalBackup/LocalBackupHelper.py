import os
import shutil
from datetime import datetime
from typing import List

BACKUP_ROOT = "backups"

def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _backup_path(name: str) -> str:
    return os.path.join(BACKUP_ROOT, f"{name}_{_timestamp()}")

def backup_file(src_path: str) -> str:
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    base_name = os.path.basename(src_path)
    dest_path = _backup_path(base_name)
    shutil.copy2(src_path, dest_path)
    return dest_path

def backup_directory(src_dir: str) -> str:
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    base_name = os.path.basename(src_dir.rstrip(os.sep))
    dest_path = _backup_path(base_name)
    shutil.copytree(src_dir, dest_path)
    return dest_path

def list_backups(name_prefix: str) -> List[str]:
    if not os.path.exists(BACKUP_ROOT):
        return []
    return sorted([
        f for f in os.listdir(BACKUP_ROOT)
        if f.startswith(name_prefix)
    ])

def restore_backup(backup_name: str, dest_path: str):
    src_path = os.path.join(BACKUP_ROOT, backup_name)
    if os.path.isdir(src_path):
        shutil.copytree(src_path, dest_path)
    else:
        shutil.copy2(src_path, dest_path)

def rotate_backups(name_prefix: str, max_versions: int):
    all_versions = list_backups(name_prefix)
    if len(all_versions) <= max_versions:
        return
    for old in all_versions[:-max_versions]:
        path = os.path.join(BACKUP_ROOT, old)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)