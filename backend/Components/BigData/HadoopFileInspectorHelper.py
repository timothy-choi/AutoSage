from hdfs import InsecureClient

def create_hdfs_client(host="http://localhost", port=9870, user="hdfs"):
    return InsecureClient(f"{host}:{port}", user=user)

def list_hdfs_directory(client, path="/"):
    try:
        return client.list(path, status=True)
    except Exception as e:
        return {"error": str(e)}

def get_file_info(client, path):
    try:
        return client.status(path)
    except Exception as e:
        return {"error": str(e)}

def list_all_files_recursive(client, path="/"):
    try:
        contents = []
        for name, info in client.list(path, status=True):
            full_path = f"{path.rstrip('/')}/{name}"
            contents.append({"path": full_path, **info})
            if info["type"] == "DIRECTORY":
                contents.extend(list_all_files_recursive(client, full_path))
        return contents
    except Exception as e:
        return {"error": str(e)}