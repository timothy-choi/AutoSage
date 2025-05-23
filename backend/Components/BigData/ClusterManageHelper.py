import subprocess
from typing import Optional

HADOOP_SBIN = "/usr/local/hadoop/sbin"
SPARK_SBIN = "/usr/local/spark/sbin"


def start_daemon(script: str) -> bool:
    try:
        subprocess.run([script], shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def stop_daemon(script: str) -> bool:
    try:
        subprocess.run([script], shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def start_namenode() -> bool:
    return start_daemon(f"{HADOOP_SBIN}/hadoop-daemon.sh start namenode")


def stop_namenode() -> bool:
    return stop_daemon(f"{HADOOP_SBIN}/hadoop-daemon.sh stop namenode")


def start_datanode() -> bool:
    return start_daemon(f"{HADOOP_SBIN}/hadoop-daemon.sh start datanode")


def stop_datanode() -> bool:
    return stop_daemon(f"{HADOOP_SBIN}/hadoop-daemon.sh stop datanode")


def start_resourcemanager() -> bool:
    return start_daemon(f"{HADOOP_SBIN}/yarn-daemon.sh start resourcemanager")


def stop_resourcemanager() -> bool:
    return stop_daemon(f"{HADOOP_SBIN}/yarn-daemon.sh stop resourcemanager")


def start_nodemanager() -> bool:
    return start_daemon(f"{HADOOP_SBIN}/yarn-daemon.sh start nodemanager")


def stop_nodemanager() -> bool:
    return stop_daemon(f"{HADOOP_SBIN}/yarn-daemon.sh stop nodemanager")


def start_spark_master() -> bool:
    return start_daemon(f"{SPARK_SBIN}/start-master.sh")


def stop_spark_master() -> bool:
    return stop_daemon(f"{SPARK_SBIN}/stop-master.sh")


def start_spark_worker() -> bool:
    return start_daemon(f"{SPARK_SBIN}/start-worker.sh spark://localhost:7077")


def stop_spark_worker() -> bool:
    return stop_daemon(f"{SPARK_SBIN}/stop-worker.sh")