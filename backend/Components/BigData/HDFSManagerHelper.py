import subprocess
from typing import List, Optional


def hdfs_put(local_path: str, hdfs_path: str) -> bool:
    try:
        subprocess.run(["hdfs", "dfs", "-put", local_path, hdfs_path], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def hdfs_get(hdfs_path: str, local_path: str) -> bool:
    try:
        subprocess.run(["hdfs", "dfs", "-get", hdfs_path, local_path], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def hdfs_mkdir(hdfs_path: str) -> bool:
    try:
        subprocess.run(["hdfs", "dfs", "-mkdir", "-p", hdfs_path], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def hdfs_rm(path: str, recursive: bool = False) -> bool:
    try:
        cmd = ["hdfs", "dfs", "-rm"]
        if recursive:
            cmd.append("-r")
        cmd.append(path)
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def hdfs_ls(path: str) -> Optional[List[str]]:
    try:
        result = subprocess.run(["hdfs", "dfs", "-ls", path], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        return lines[1:] if len(lines) > 1 else []
    except subprocess.CalledProcessError:
        return None


def hdfs_cat(path: str) -> Optional[str]:
    try:
        result = subprocess.run(["hdfs", "dfs", "-cat", path], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None