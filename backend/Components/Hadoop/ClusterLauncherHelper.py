import subprocess
from typing import List, Optional

HADOOP_SBIN = "/usr/local/hadoop/sbin"
SPARK_SBIN = "/usr/local/spark/sbin"


def start_hadoop_cluster() -> bool:
    """Start HDFS and YARN daemons."""
    try:
        subprocess.run([f"{HADOOP_SBIN}/start-dfs.sh"], shell=True, check=True)
        subprocess.run([f"{HADOOP_SBIN}/start-yarn.sh"], shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def stop_hadoop_cluster() -> bool:
    """Stop HDFS and YARN daemons."""
    try:
        subprocess.run([f"{HADOOP_SBIN}/stop-yarn.sh"], shell=True, check=True)
        subprocess.run([f"{HADOOP_SBIN}/stop-dfs.sh"], shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def start_spark_cluster() -> bool:
    """Start Spark master and workers."""
    try:
        subprocess.run([f"{SPARK_SBIN}/start-all.sh"], shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def stop_spark_cluster() -> bool:
    """Stop Spark master and workers."""
    try:
        subprocess.run([f"{SPARK_SBIN}/stop-all.sh"], shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def run_command(command: str) -> Optional[str]:
    """Utility to run a shell command and capture output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode()}"