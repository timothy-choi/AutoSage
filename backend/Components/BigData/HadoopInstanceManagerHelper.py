import os
import shutil
import uuid
from typing import Dict, Optional

HADOOP_BASE_DIR = os.path.expanduser("~/.hadoop-instances")
os.makedirs(HADOOP_BASE_DIR, exist_ok=True)

_instances: Dict[str, str] = {}


def create_hadoop_instance(config_template_dir: str) -> str:
    instance_id = str(uuid.uuid4())
    instance_path = os.path.join(HADOOP_BASE_DIR, instance_id)
    shutil.copytree(config_template_dir, instance_path)
    _instances[instance_id] = instance_path
    return instance_id


def delete_hadoop_instance(instance_id: str) -> bool:
    path = _instances.pop(instance_id, None)
    if path and os.path.exists(path):
        shutil.rmtree(path)
        return True
    return False


def list_hadoop_instances() -> Dict[str, str]:
    return _instances.copy()


def update_hadoop_instance_config(instance_id: str, file_name: str, updates: Dict[str, str]) -> bool:
    from xml.etree import ElementTree as ET

    path = _instances.get(instance_id)
    if not path:
        return False

    file_path = os.path.join(path, file_name)
    if not os.path.exists(file_path):
        return False

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for key, value in updates.items():
            found = False
            for prop in root.findall("property"):
                name = prop.find("name")
                if name is not None and name.text == key:
                    prop.find("value").text = value
                    found = True
                    break
            if not found:
                new_prop = ET.SubElement(root, "property")
                ET.SubElement(new_prop, "name").text = key
                ET.SubElement(new_prop, "value").text = value

        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        return True
    except Exception:
        return False