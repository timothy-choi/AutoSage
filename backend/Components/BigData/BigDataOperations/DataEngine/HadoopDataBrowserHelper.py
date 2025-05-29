from hdfs import InsecureClient

def create_hdfs_client(url="http://localhost:9870", user="hdfs"):
    return InsecureClient(url, user=user)

def list_hdfs_directory(client, path="/", recursive=False):
    try:
        return client.list(path, status=True) if not recursive else _list_recursive(client, path)
    except Exception as e:
        print(f"[HadoopDataBrowser] Failed to list directory: {e}")
        raise

def _list_recursive(client, path):
    result = []
    try:
        entries = client.list(path, status=True)
        for name, info in entries:
            full_path = f"{path.rstrip('/')}/{name}"
            result.append((full_path, info))
            if info['type'] == 'DIRECTORY':
                result.extend(_list_recursive(client, full_path))
        return result
    except Exception as e:
        print(f"[HadoopDataBrowser] Recursive listing failed at {path}: {e}")
        raise

def read_hdfs_file(client, path, encoding='utf-8'):
    try:
        with client.read(path, encoding=encoding) as reader:
            return reader.read()
    except Exception as e:
        print(f"[HadoopDataBrowser] Failed to read file {path}: {e}")
        raise

def filter_files_by_extension(file_list, extension=".csv"):
    return [file for file, info in file_list if file.endswith(extension)]
