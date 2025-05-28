import os
import zipfile
from typing import List


def archive_dataset(file_paths: List[str], archive_name: str) -> str:
    try:
        if not archive_name.endswith(".zip"):
            archive_name += ".zip"

        with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in file_paths:
                if os.path.exists(path):
                    archive.write(path, arcname=os.path.basename(path))

        return archive_name
    except Exception as e:
        return f"Error creating archive: {e}"