import requests

def download_file_from_salesforce(instance_url: str, access_token: str, content_document_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    query_url = f"{instance_url}/services/data/v58.0/query"
    query = (
        f"SELECT Id, Title, VersionData, FileExtension "
        f"FROM ContentVersion WHERE ContentDocumentId = '{content_document_id}' "
        f"ORDER BY VersionNumber DESC LIMIT 1"
    )

    try:
        query_response = requests.get(query_url, headers=headers, params={"q": query})
        if query_response.status_code != 200:
            return {"success": False, "error": query_response.text}

        records = query_response.json().get("records")
        if not records:
            return {"success": False, "error": "No ContentVersion found."}

        content_version = records[0]
        version_id = content_version["Id"]
        title = content_version["Title"]
        extension = content_version["FileExtension"]

        file_name = f"{title}.{extension}" if extension else title
        download_url = f"{instance_url}/services/data/v58.0/sobjects/ContentVersion/{version_id}/VersionData"

        file_response = requests.get(download_url, headers=headers)
        if file_response.status_code != 200:
            return {"success": False, "error": file_response.text}

        return {
            "success": True,
            "file_name": file_name,
            "content_type": file_response.headers.get("Content-Type", "application/octet-stream"),
            "file_data": file_response.content
        }

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}