from boxsdk import Client

def add_collaborator(client: Client, folder_id: str, email: str, role: str = "editor"):
    folder = client.folder(folder_id=folder_id).get()
    collaboration = folder.collaborate_with_login(email, role)
    return collaboration

def remove_collaborator(client: Client, collaboration_id: str):
    collab = client.collaboration(collaboration_id=collaboration_id).get()
    collab.delete()
    return {"message": f"Collaboration {collaboration_id} removed successfully."}

def list_collaborators(client: Client, folder_id: str):
    folder = client.folder(folder_id=folder_id).get()
    collaborators = folder.get_collaborations()
    return [{"id": c.id, "role": c.role, "login": c.accessible_by.login} for c in collaborators]

def update_collaborator_role(client: Client, collaboration_id: str, new_role: str):
    collab = client.collaboration(collaboration_id=collaboration_id).update_info({"role": new_role})
    return collab