import subprocess
import shlex
import os

def run_shell_command(command: str, capture_output: bool = True, timeout: int = 10):
    try:
        args = shlex.split(command)

        result = subprocess.run(
            args,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )

        return {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip() if result.stdout else "",
            "stderr": result.stderr.strip() if result.stderr else ""
        }

    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "Command timed out"
        }
    except Exception as e:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution failed: {str(e)}"
        }
    
def run_shell_script(script_path: str, args: list = None):
    try:
        if not os.path.exists(script_path):
            return {"exit_code": -1, "stdout": "", "stderr": "Script not found"}

        command = [script_path] + (args or [])
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e)}

def list_running_processes():
    try:
        if os.name == 'nt':
            command = ["tasklist"]
        else:
            command = ["ps", "aux"]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e)}

def kill_process_by_name(process_name: str):
    try:
        if os.name == 'nt':
            command = f"taskkill /IM {process_name} /F"
        else:
            command = f"pkill -f {shlex.quote(process_name)}"

        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e)}

def check_command_available(command: str):
    try:
        result = subprocess.run(
            ["which", command] if os.name != 'nt' else ["where", command],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return {"available": True, "path": result.stdout.strip()}
        return {"available": False, "error": result.stderr.strip()}
    except Exception as e:
        return {"available": False, "error": str(e)}