import os
import getpass
from typing import Dict
import xml.etree.ElementTree as ET

USER_CONF_BASE = os.path.expanduser(f"~/.hadoop-configs/{getpass.getuser()}")
HADOOP_CONF_DIR = os.environ.get("HADOOP_CONF_DIR", USER_CONF_BASE)
os.makedirs(HADOOP_CONF_DIR, exist_ok=True)

def write_hadoop_config(file_name: str, properties: Dict[str, str]) -> None:
    config_path = os.path.join(HADOOP_CONF_DIR, file_name)
    configuration = ET.Element("configuration")
    for key, value in properties.items():
        prop = ET.SubElement(configuration, "property")
        name = ET.SubElement(prop, "name")
        name.text = key
        val = ET.SubElement(prop, "value")
        val.text = value
    tree = ET.ElementTree(configuration)
    tree.write(config_path, encoding="utf-8", xml_declaration=True)

def read_hadoop_config(file_name: str) -> Dict[str, str]:
    config_path = os.path.join(HADOOP_CONF_DIR, file_name)
    if not os.path.exists(config_path):
        return {}
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {}
    for prop in root.findall("property"):
        name = prop.find("name")
        value = prop.find("value")
        if name is not None and value is not None:
            config[name.text] = value.text
    return config

def format_namenode(hdfs_dir: str) -> bool:
    result = os.system(f"hdfs namenode -format -force -nonInteractive -clusterId HadoopCluster")
    return result == 0