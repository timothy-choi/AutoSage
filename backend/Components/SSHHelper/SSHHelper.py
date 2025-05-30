import paramiko
import os

def create_ssh_client(hostname, port=22, username=None, password=None, key_path=None, timeout=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key_path:
            key = paramiko.RSAKey.from_private_key_file(key_path)
            client.connect(hostname, port=port, username=username, pkey=key, timeout=timeout)
        else:
            client.connect(hostname, port=port, username=username, password=password, timeout=timeout)
        return client
    except Exception as e:
        raise Exception(f"SSH connection failed: {e}")

def run_ssh_command(client, command):
    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return {"stdout": output, "stderr": error}
    except Exception as e:
        return {"stdout": "", "stderr": str(e)}

def upload_file(client, local_path, remote_path):
    try:
        ftp = client.open_sftp()
        ftp.put(local_path, remote_path)
        ftp.close()
        return {"status": "uploaded"}
    except Exception as e:
        return {"error": str(e)}

def download_file(client, remote_path, local_path):
    try:
        ftp = client.open_sftp()
        ftp.get(remote_path, local_path)
        ftp.close()
        return {"status": "downloaded"}
    except Exception as e:
        return {"error": str(e)}

def close_ssh_client(client):
    try:
        client.close()
    except Exception:
        pass

def file_exists(client, remote_path):
    try:
        ftp = client.open_sftp()
        ftp.stat(remote_path)
        ftp.close()
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        raise Exception(f"Error checking file existence: {e}")

def list_remote_files(client, remote_path):
    try:
        ftp = client.open_sftp()
        files = ftp.listdir(remote_path)
        ftp.close()
        return files
    except Exception as e:
        raise Exception(f"Error listing remote files: {e}")
    
def remove_remote_file(client, remote_path):
    try:
        ftp = client.open_sftp()
        ftp.remove(remote_path)
        ftp.close()
        return {"status": "deleted"}
    except FileNotFoundError:
        return {"error": "file not found"}
    except Exception as e:
        raise Exception(f"Error removing remote file: {e}")