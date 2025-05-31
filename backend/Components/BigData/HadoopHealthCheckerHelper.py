import requests

def check_namenode_health(host="localhost", port=9870):
    try:
        url = f"http://{host}:{port}/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        status = data["beans"][0].get("State")
        return {"namenode_status": status}
    except Exception as e:
        return {"error": f"NameNode check failed: {str(e)}"}

def check_yarn_health(host="localhost", port=8088):
    try:
        url = f"http://{host}:{port}/ws/v1/cluster/info"
        response = requests.get(url)
        response.raise_for_status()
        info = response.json().get("clusterInfo", {})
        return {
            "state": info.get("state"),
            "ha_state": info.get("haState"),
            "resource_manager": info.get("resourceManagerVersion")
        }
    except Exception as e:
        return {"error": f"YARN check failed: {str(e)}"}

def check_hdfs_summary(host="localhost", port=9870):
    try:
        url = f"http://{host}:{port}/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["beans"][0]
        return {
            "total": data.get("CapacityTotal"),
            "used": data.get("CapacityUsed"),
            "remaining": data.get("CapacityRemaining"),
            "under_replicated_blocks": data.get("UnderReplicatedBlocks")
        }
    except Exception as e:
        return {"error": f"HDFS summary check failed: {str(e)}"}