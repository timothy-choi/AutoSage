import subprocess
from typing import Optional, List, Dict


def list_hadoop_jobs() -> Optional[List[str]]:
    try:
        result = subprocess.run(["mapred", "job", "-list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        return lines[2:] if len(lines) > 2 else []
    except subprocess.CalledProcessError:
        return None


def get_hadoop_job_status(job_id: str) -> Optional[str]:
    try:
        result = subprocess.run(["mapred", "job", "-status", job_id], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def kill_hadoop_job(job_id: str) -> bool:
    try:
        subprocess.run(["mapred", "job", "-kill", job_id], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_hadoop_job_counters(job_id: str) -> Optional[str]:
    try:
        result = subprocess.run(["mapred", "job", "-counter", job_id, "org.apache.hadoop.mapreduce.TaskCounter", "ALL"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def get_hadoop_job_history(job_id: str) -> Optional[str]:
    try:
        result = subprocess.run(["mapred", "job", "-history", job_id], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None