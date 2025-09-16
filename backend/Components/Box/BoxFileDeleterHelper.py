import requests

BOX_API_BASE = "https://api.box.com/2.0"

def delete_file(file_id: str, access_token: str):
    url = f"{BOX_API_BASE}/files/{file_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"message": f"File {file_id} deleted successfully."}
    else:
        return {"error": response.json(), "status_code": response.status_code}