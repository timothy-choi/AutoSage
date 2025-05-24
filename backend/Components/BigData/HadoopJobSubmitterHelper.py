import subprocess
from typing import List, Optional

HADOOP_BIN = "/usr/local/hadoop/bin/hadoop"


def submit_hadoop_job(
    jar_path: str,
    main_class: Optional[str],
    input_path: str,
    output_path: str,
    additional_args: Optional[List[str]] = None
) -> str:
    """
    Submit a Hadoop job using a jar file and optionally a main class.
    """
    cmd = [HADOOP_BIN, "jar", jar_path]

    if main_class:
        cmd.append(main_class)

    cmd.extend([input_path, output_path])

    if additional_args:
        cmd.extend(additional_args)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
