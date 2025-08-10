import requests

def link_file_to_salesforce_record(instance_url: str, access_token: str, content_document_id: str, linked_entity_id: str, visibility: str = "AllUsers") -> dict:
    url = f"{instance_url}/services/data/v58.0/sobjects/ContentDocumentLink"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "ContentDocumentId": content_document_id,
        "LinkedEntityId": linked_entity_id,
        "ShareType": "V",  
        "Visibility": visibility
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return {"success": True, "message": "File linked successfully."}
        else:
            return {"success": False, "error": response.text}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}