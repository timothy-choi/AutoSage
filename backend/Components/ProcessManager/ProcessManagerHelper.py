import psutil

def list_processes():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            processes.append(proc.info)
        return processes
    except Exception as e:
        return {"error": str(e)}

def get_process_details(pid: int):
    try:
        proc = psutil.Process(pid)
        return {
            "pid": proc.pid,
            "name": proc.name(),
            "status": proc.status(),
            "cmdline": proc.cmdline(),
            "create_time": proc.create_time(),
            "cpu_percent": proc.cpu_percent(interval=0.1),
            "memory_percent": proc.memory_percent(),
            "threads": proc.num_threads(),
            "open_files": [f.path for f in proc.open_files()] if proc.open_files() else [],
        }
    except psutil.NoSuchProcess:
        return {"error": f"No process with PID {pid}"}
    except Exception as e:
        return {"error": str(e)}

def terminate_process(pid: int):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        return {"status": "terminated", "pid": pid}
    except psutil.NoSuchProcess:
        return {"error": f"No process with PID {pid}"}
    except psutil.TimeoutExpired:
        return {"error": f"Process {pid} did not terminate in time"}
    except Exception as e:
        return {"error": str(e)}

def kill_process(pid: int):
    try:
        proc = psutil.Process(pid)
        proc.kill()
        return {"status": "killed", "pid": pid}
    except psutil.NoSuchProcess:
        return {"error": f"No process with PID {pid}"}
    except Exception as e:
        return {"error": str(e)}