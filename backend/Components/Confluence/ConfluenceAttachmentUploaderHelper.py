import requests
import os

def upload_attachment_to_confluence_page(api_base_url, page_id, file_path, auth):
    url = f"{api_base_url}/content/{page_id}/child/attachment"
    filename = os.path.basename(file_path)

    headers = {
        "X-Atlassian-Token": "no-check"
    }

    files = {
        'file': (filename, open(file_path, 'rb'), 'application/octet-stream')
    }

    response = requests.post(url, headers=headers, files=files, auth=auth)
    response.raise_for_status()
    return response.json()

def update_attachment_on_confluence_page(api_base_url, page_id, file_path, auth):
    filename = os.path.basename(file_path)
    search_url = f"{api_base_url}/content/{page_id}/child/attachment?filename={filename}"
    search_response = requests.get(search_url, auth=auth)
    search_response.raise_for_status()
    attachments = search_response.json().get("results", [])

    if not attachments:
        raise Exception(f"Attachment '{filename}' not found on page {page_id}")

    attachment_id = attachments[0]['id']
    update_url = f"{api_base_url}/content/{page_id}/child/attachment/{attachment_id}/data"
    headers = {
        "X-Atlassian-Token": "no-check"
    }
    files = {
        'file': (filename, open(file_path, 'rb'), 'application/octet-stream')
    }

    response = requests.post(update_url, headers=headers, files=files, auth=auth)
    response.raise_for_status()
    return response.json()