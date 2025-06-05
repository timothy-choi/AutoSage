import os
import shutil
import subprocess
import uuid

def build_offline_installer(script_path: str, requirements_path: str, output_dir: str = "offline_installer") -> str:
    if not os.path.exists(script_path):
        raise FileNotFoundError("Script not found.")
    if not os.path.exists(requirements_path):
        raise FileNotFoundError("requirements.txt not found.")

    install_id = str(uuid.uuid4())[:8]
    work_dir = f"{output_dir}_{install_id}"
    os.makedirs(work_dir, exist_ok=True)

    shutil.copy(script_path, os.path.join(work_dir, "main.py"))
    shutil.copy(requirements_path, os.path.join(work_dir, "requirements.txt"))

    wheels_dir = os.path.join(work_dir, "wheels")
    os.makedirs(wheels_dir, exist_ok=True)

    subprocess.check_call([
        "pip", "download", "-r", requirements_path, "-d", wheels_dir
    ])

    with open(os.path.join(work_dir, "run.sh"), "w") as f:
        f.write("#!/bin/bash\n")
        f.write("python3 -m venv venv\n")
        f.write("source venv/bin/activate\n")
        f.write("pip install --no-index --find-links=wheels -r requirements.txt\n")
        f.write("python main.py\n")

    with open(os.path.join(work_dir, "run.bat"), "w") as f:
        f.write("@echo off\n")
        f.write("python -m venv venv\n")
        f.write("call venv\\Scripts\\activate\n")
        f.write("pip install --no-index --find-links=wheels -r requirements.txt\n")
        f.write("python main.py\n")

    archive_path = shutil.make_archive(work_dir, 'zip', work_dir)
    shutil.rmtree(work_dir)

    return archive_path