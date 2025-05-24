import requests
from typing import Optional, Dict, Any

YARN_RESOURCE_MANAGER = "http://localhost:8088/ws/v1/cluster"
SPARK_MASTER_UI = "http://localhost:4040/api/v1"


def fetch_yarn_cluster_metrics() -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{YARN_RESOURCE_MANAGER}/metrics")
        response.raise_for_status()
        return response.json().get("clusterMetrics")
    except Exception as e:
        print(f"Failed to fetch YARN metrics: {e}")
        return None


def fetch_yarn_apps(state: str = "RUNNING") -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{YARN_RESOURCE_MANAGER}/apps?state={state}")
        response.raise_for_status()
        return response.json().get("apps")
    except Exception as e:
        print(f"Failed to fetch YARN apps: {e}")
        return None


def fetch_spark_applications() -> Optional[Any]:
    try:
        response = requests.get(f"{SPARK_MASTER_UI}/applications")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch Spark applications: {e}")
        return None


def fetch_spark_environment(app_id: str) -> Optional[Any]:
    try:
        response = requests.get(f"{SPARK_MASTER_UI}/applications/{app_id}/environment")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch Spark environment: {e}")
        return None
