import os
import getpass
from typing import Dict

USER_SPARK_CONF_DIR = os.path.expanduser(f"~/.spark-configs/{getpass.getuser()}")
os.makedirs(USER_SPARK_CONF_DIR, exist_ok=True)


def write_spark_defaults(properties: Dict[str, str]) -> None:
    path = os.path.join(USER_SPARK_CONF_DIR, "spark-defaults.conf")
    with open(path, "w") as f:
        for key, value in properties.items():
            f.write(f"{key} {value}\n")


def read_spark_defaults() -> Dict[str, str]:
    path = os.path.join(USER_SPARK_CONF_DIR, "spark-defaults.conf")
    if not os.path.exists(path):
        return {}

    props = {}
    with open(path, "r") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    props[parts[0]] = parts[1]
    return props


def write_spark_env(vars: Dict[str, str]) -> None:
    path = os.path.join(USER_SPARK_CONF_DIR, "spark-env.sh")
    with open(path, "w") as f:
        for key, value in vars.items():
            f.write(f"export {key}={value}\n")


def read_spark_env() -> Dict[str, str]:
    path = os.path.join(USER_SPARK_CONF_DIR, "spark-env.sh")
    if not os.path.exists(path):
        return {}

    env_vars = {}
    with open(path, "r") as f:
        for line in f:
            if line.startswith("export "):
                parts = line[len("export "):].strip().split("=", 1)
                if len(parts) == 2:
                    env_vars[parts[0]] = parts[1]
    return env_vars