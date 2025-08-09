import requests
import base64

def upload_file_to_salesforce(instance_url: str, access_token: str, file_name: str, file_data: bytes, linked_record_id: str) -> dict:
    content_base64 = base64.b64encode(file_data).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    content_version_url = f"{instance_url}/services/data/v58.0/sobjects/ContentVersion"
    content_payload = {
        "Title": file_name,
        "PathOnClient": file_name,
        "VersionData": content_base64
    }

    try:
        cv_response = requests.post(content_version_url, headers=headers, json=content_payload)
        if cv_response.status_code != 201:
            return {"success": False, "error": cv_response.text}

        content_version_id = cv_response.json().get("id")

        query_url = f"{instance_url}/services/data/v58.0/query"
        query = f"SELECT ContentDocumentId FROM ContentVersion WHERE Id = '{content_version_id}'"
        query_response = requests.get(query_url, headers=headers, params={"q": query})

        if query_response.status_code != 200:
            return {"success": False, "error": query_response.text}

        content_document_id = query_response.json()["records"][0]["ContentDocumentId"]

        link_url = f"{instance_url}/services/data/v58.0/sobjects/ContentDocumentLink"
        link_payload = {
            "ContentDocumentId": content_document_id,
            "LinkedEntityId": linked_record_id,
            "ShareType": "V"
        }
        link_response = requests.post(link_url, headers=headers, json=link_payload)

        if link_response.status_code != 201:
            return {"success": False, "error": link_response.text}

        return {
            "success": True,
            "content_version_id": content_version_id,
            "content_document_id": content_document_id,
            "link_id": link_response.json().get("id")
        }

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}