import os
import hashlib
import magic
import mimetypes
import math
from typing import Dict, Optional
import yara
import requests

magic_detector = magic.Magic(mime=True)

def get_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def get_mime_type(file_path: str) -> str:
    return magic_detector.from_file(file_path)

def get_extension(file_path: str) -> Optional[str]:
    return os.path.splitext(file_path)[1].lower()

def is_executable(file_path: str) -> bool:
    mime = get_mime_type(file_path)
    return "application/x-executable" in mime or os.access(file_path, os.X_OK)

def is_script_file(file_path: str) -> bool:
    return get_extension(file_path) in [".sh", ".bat", ".ps1", ".py", ".pl", ".js"]

def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)

def get_entropy(file_path: str) -> float:
    with open(file_path, "rb") as f:
        data = f.read()
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    entropy = -sum((p := f / len(data)) * math.log2(p) for f in freq if f)
    return round(entropy, 4)

def scan_with_yara(file_path: str, yara_rules_path: str) -> Optional[Dict[str, str]]:
    try:
        rules = yara.compile(filepath=yara_rules_path)
        matches = rules.match(file_path)
        return {"matches": [match.rule for match in matches]}
    except Exception as e:
        return {"error": str(e)}

def scan_with_virustotal(file_path: str, api_key: str) -> Optional[Dict[str, str]]:
    try:
        import requests
        file_hash = get_file_hash(file_path)
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {"x-apikey": api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            return {
                "scan_id": data.get("data", {}).get("id", ""),
                "malicious": str(stats.get("malicious", 0)),
                "suspicious": str(stats.get("suspicious", 0))
            }
        else:
            return {"error": f"VirusTotal status: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def basic_scan(file_path: str) -> Dict[str, str]:
    return {
        "file_path": file_path,
        "file_hash": get_file_hash(file_path),
        "file_size": str(get_file_size(file_path)),
        "entropy": str(get_entropy(file_path)),
        "mime_type": get_mime_type(file_path),
        "is_executable": str(is_executable(file_path)),
        "is_script": str(is_script_file(file_path))
    }