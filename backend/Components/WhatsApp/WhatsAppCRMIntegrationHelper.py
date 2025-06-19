import os
import json
from datetime import datetime
from typing import Dict, List

CRM_FILE = "logs/whatsapp_crm_log.json"
os.makedirs("logs", exist_ok=True)

def load_crm() -> Dict[str, Dict]:
    if not os.path.exists(CRM_FILE):
        return {}
    with open(CRM_FILE, "r") as f:
        return json.load(f)

def save_crm(data: Dict[str, Dict]):
    with open(CRM_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_crm_entry(from_number: str, message: str, direction: str = "inbound"):
    crm_data = load_crm()
    entry = crm_data.get(from_number, {
        "number": from_number,
        "interactions": [],
        "last_contact": None,
        "total_messages": 0
    })

    entry["interactions"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "direction": direction,
        "message": message
    })

    entry["last_contact"] = datetime.utcnow().isoformat()
    entry["total_messages"] = entry.get("total_messages", 0) + 1
    crm_data[from_number] = entry
    save_crm(crm_data)

def get_crm_contact_summary(number: str) -> Dict:
    crm_data = load_crm()
    return crm_data.get(number, {})

def list_crm_contacts(limit: int = 10) -> List[Dict]:
    crm_data = load_crm()
    all_contacts = list(crm_data.values())
    sorted_contacts = sorted(all_contacts, key=lambda x: x.get("last_contact", ""), reverse=True)
    return sorted_contacts[:limit]