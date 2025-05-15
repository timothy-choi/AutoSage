import os
import zipfile
import tarfile
from typing import List

def zip_files(files: List[str], output_path: str) -> str:
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                arcname = os.path.basename(file)
                zipf.write(file, arcname)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to create zip: {e}")

def unzip_file(zip_path: str, extract_to: str) -> List[str]:
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_to)
            return zipf.namelist()
    except Exception as e:
        raise RuntimeError(f"Failed to unzip file: {e}")

def tar_files(files: List[str], output_path: str, mode: str = 'w:gz') -> str:
    try:
        with tarfile.open(output_path, mode) as tar:
            for file in files:
                arcname = os.path.basename(file)
                tar.add(file, arcname=arcname)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to create tar archive: {e}")

def untar_file(tar_path: str, extract_to: str) -> List[str]:
    try:
        with tarfile.open(tar_path, 'r:*') as tar:
            tar.extractall(path=extract_to)
            return tar.getnames()
    except Exception as e:
        raise RuntimeError(f"Failed to extract tar archive: {e}")
    
def delete_file(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        os.remove(file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to delete file: {e}")
    
def rename_file(original_path: str, new_path: str) -> str:
    if not os.path.exists(original_path):
        raise FileNotFoundError(f"File not found: {original_path}")
    try:
        os.rename(original_path, new_path)
        return new_path
    except Exception as e:
        raise RuntimeError(f"Failed to rename file: {e}")
