import requests

BASE_URL = ""

def list_queues(base_url: str = BASE_URL) -> list | dict:
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        scheduler_info = response.json()["scheduler"]["schedulerInfo"]

        def collect_queues(scheduler):
            if "queues" in scheduler:
                queues = []
                for q in scheduler["queues"]["queue"]:
                    queues += collect_queues(q)
                return queues
            return [{
                "name": scheduler["queueName"],
                "capacity": scheduler.get("capacity"),
                "maxCapacity": scheduler.get("maxCapacity"),
                "state": scheduler.get("state", "UNKNOWN")
            }]

        return collect_queues(scheduler_info)
    except Exception as e:
        return {"error": str(e)}

def get_queue_info(queue_name: str, base_url: str = BASE_URL) -> dict:
    queues = list_queues(base_url)
    if isinstance(queues, dict) and "error" in queues:
        return queues
    for q in queues:
        if q["name"] == queue_name:
            return q
    return {"error": f"Queue '{queue_name}' not found"}

def get_raw_scheduler_info(base_url: str = BASE_URL) -> dict:
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}