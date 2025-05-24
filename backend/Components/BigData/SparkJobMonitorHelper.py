import requests
from typing import List, Dict, Optional

SPARK_REST_API = "http://localhost:4040/api/v1"


def list_spark_jobs() -> Optional[List[Dict]]:
    try:
        response = requests.get(f"{SPARK_REST_API}/jobs")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching job list: {e}")
        return None


def get_job_details(job_id: int) -> Optional[Dict]:
    try:
        response = requests.get(f"{SPARK_REST_API}/jobs/{job_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching job {job_id}: {e}")
        return None


def list_spark_stages() -> Optional[List[Dict]]:
    try:
        response = requests.get(f"{SPARK_REST_API}/stages")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching stages: {e}")
        return None


def list_spark_executors() -> Optional[List[Dict]]:
    try:
        response = requests.get(f"{SPARK_REST_API}/executors")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching executors: {e}")
        return None