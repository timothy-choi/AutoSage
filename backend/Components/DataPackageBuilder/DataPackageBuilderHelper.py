import os
import json
import shutil
import uuid
from typing import List, Dict

def build_data_package(
    data_files: List[str],
    metadata: Dict,
    output_dir: str = "data_package_output"
) -> str:
    if not data_files:
        raise ValueError("No data files provided.")

    package_id = str(uuid.uuid4())[:8]
    work_dir = f"{output_dir}_{package_id}"
    os.makedirs(work_dir, exist_ok=True)

    resources = []

    for file_path in data_files:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{file_path} not found")

        filename = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(work_dir, filename))
        resources.append({
            "path": filename,
            "format": filename.split(".")[-1],
            "mediatype": f"text/{filename.split('.')[-1]}",
            "name": filename
        })

    datapackage = {
        "name": metadata.get("name", "data-package"),
        "title": metadata.get("title", ""),
        "description": metadata.get("description", ""),
        "license": metadata.get("license", "CC0-1.0"),
        "resources": resources
    }

    with open(os.path.join(work_dir, "datapackage.json"), "w") as f:
        json.dump(datapackage, f, indent=2)

    zip_path = shutil.make_archive(work_dir, "zip", work_dir)
    shutil.rmtree(work_dir)

    return zip_path