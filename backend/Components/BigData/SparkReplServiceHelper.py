import sys
import io
from typing import Optional, Dict
from SparkSessionManagerHelper import get_spark_session


def execute_python_code(session_id: str, code: str) -> Dict[str, str]:
    session = get_spark_session(session_id)
    if not session:
        return {"error": "Session not found"}

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stdout_capture = io.StringIO()
    sys.stderr = stderr_capture = io.StringIO()

    try:
        exec(code, {"spark": session, "sc": session.sparkContext})
        output = stdout_capture.getvalue()
        error = stderr_capture.getvalue()
    except Exception as e:
        output = stdout_capture.getvalue()
        error = str(e)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return {"output": output.strip(), "error": error.strip()}


def evaluate_expression(session_id: str, expression: str) -> Dict[str, str]:
    session = get_spark_session(session_id)
    if not session:
        return {"error": "Session not found"}

    try:
        result = eval(expression, {"spark": session, "sc": session.sparkContext})
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}


def get_variable_value(session_id: str, var_name: str) -> Dict[str, str]:
    session = get_spark_session(session_id)
    if not session:
        return {"error": "Session not found"}

    local_env = {"spark": session, "sc": session.sparkContext}
    try:
        exec(f"_val = {var_name}", local_env)
        return {"value": str(local_env["_val"])}
    except Exception as e:
        return {"error": str(e)}