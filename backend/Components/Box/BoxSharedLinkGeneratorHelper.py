from boxsdk import Client
from typing import Optional

def create_shared_link(
    client: Client,
    item_id: str,
    item_type: str = "file",
    access: str = "open",
    permissions: Optional[dict] = None
):
    permissions = permissions or {"can_download": True}
    
    if item_type == "file":
        item = client.file(file_id=item_id).get()
    elif item_type == "folder":
        item = client.folder(folder_id=item_id).get()
    else:
        raise ValueError("item_type must be 'file' or 'folder'")

    updated_item = item.update_info({
        "shared_link": {
            "access": access,
            "permissions": permissions
        }
    })
    return {"shared_link": updated_item.shared_link["url"]}

def revoke_shared_link(client: Client, item_id: str, item_type: str = "file"):
    if item_type == "file":
        item = client.file(file_id=item_id).get()
    elif item_type == "folder":
        item = client.folder(folder_id=item_id).get()
    else:
        raise ValueError("item_type must be 'file' or 'folder'")

    updated_item = item.update_info({"shared_link": None})
    return {"message": f"Shared link revoked for {item_type} {item_id}"}