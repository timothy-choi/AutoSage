import os
import stat
from typing import Dict, Optional
import pwd
import grp

def check_permissions(path: str) -> Dict[str, bool]:
    return {
        "exists": os.path.exists(path),
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
        "executable": os.access(path, os.X_OK),
        "is_file": os.path.isfile(path),
        "is_dir": os.path.isdir(path)
    }

def get_file_mode(path: str) -> str:
    mode = os.stat(path).st_mode
    return stat.filemode(mode)

def get_file_owner(path: str) -> Dict[str, Optional[str]]:
    file_stat = os.stat(path)
    uid = file_stat.st_uid
    gid = file_stat.st_gid
    return {
        "owner": pwd.getpwuid(uid).pw_name,
        "group": grp.getgrgid(gid).gr_name,
        "uid": uid,
        "gid": gid
    }

def is_symlink(path: str) -> bool:
    return os.path.islink(path)

def get_symlink_target(path: str) -> Optional[str]:
    if os.path.islink(path):
        return os.readlink(path)
    return None

def get_file_size(path: str) -> Optional[int]:
    return os.path.getsize(path)