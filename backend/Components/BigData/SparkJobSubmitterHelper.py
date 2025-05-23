import subprocess
from typing import Optional, List

SPARK_SUBMIT = "/usr/local/spark/bin/spark-submit"

def submit_spark_job(
    app_path: str,
    master: str = "local[*]",
    deploy_mode: str = "client",
    app_args: Optional[List[str]] = None,
    conf: Optional[dict] = None,
    jars: Optional[List[str]] = None
) -> str:
    cmd = [SPARK_SUBMIT, "--master", master, "--deploy-mode", deploy_mode]

    if conf:
        for k, v in conf.items():
            cmd.extend(["--conf", f"{k}={v}"])

    if jars:
        cmd.extend(["--jars", ",".join(jars)])

    cmd.append(app_path)

    if app_args:
        cmd.extend(app_args)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"