from fastapi import APIRouter, Depends, status
import DockerHelper

router = APIRouter()

@router.post("/docker/containers", status_code=status.HTTP_201_CREATED)
async def create_container(
    image_name: str,
    uid: str,
    mount_path: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        container = DockerHelper.create_container(client, image_name, uid, mount_path)
        return {"container_id": container.id}
    except Exception as e:
        raise e
    
@router.delete("/docker/containers/{container_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_container(
    container_id: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        DockerHelper.delete_container(client, container_id)
        return {"message": "Container deleted successfully"}
    except Exception as e:
        raise e
    
@router.post("/docker/containers/{container_id}/start", status_code=status.HTTP_200_OK)
async def start_container(
    container_id: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        container = DockerHelper.start_container(client, container_id)
        return {"container_id": container.id}
    except Exception as e:
        raise e
    
@router.post("/docker/containers/{container_id}/run", status_code=status.HTTP_200_OK)
async def run_container(
    image: str,
    mount_path: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        container = DockerHelper.run_container(client, image, mount_path)
        return {"container_id": container.id}
    except Exception as e:
        raise e
    
@router.post("/docker/containers/{container_id}/stop", status_code=status.HTTP_200_OK)
async def stop_container(
    container_id: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        container = DockerHelper.stop_container(client, container_id)
        return {"container_id": container.id}
    except Exception as e:
        raise e
    
@router.get("/docker/containers/{container_id}", status_code=status.HTTP_200_OK)
async def get_container(
    container_id: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        container = DockerHelper.get_container(client, container_id)
        return {"container_id": container.id}
    except Exception as e:
        raise e
    
@router.get("/docker/containers", status_code=status.HTTP_200_OK)
async def list_containers(
    client = Depends(DockerHelper.get_docker_client)):
    try:
        containers = DockerHelper.list_containers(client)
        return [{"container_id": container.id} for container in containers]
    except Exception as e:
        raise e
    
@router.get("/docker/containers/{container_id}/status", status_code=status.HTTP_200_OK)
async def get_container_status(
    container_id: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        status = DockerHelper.get_container_status(client, container_id)
        return {"status": status}
    except Exception as e:
        raise e
    
@router.post("/docker/containers/{container_id}/exec", status_code=status.HTTP_200_OK)
async def run_in_container(
    container_id: str,
    command: str):
    try:
        result = DockerHelper.run_in_container(container_id, command)
        return {"exit_code": result["exit_code"], "output": result["output"]}
    except Exception as e:
        raise e
    
@router.get("/docker/containers/{container_id}/logs", status_code=status.HTTP_200_OK)
async def get_container_logs(
    container_id: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        logs = DockerHelper.get_container_logs(client, container_id)
        return {"logs": logs}
    except Exception as e:
        raise e
    
@router.post("/docker/containers/{container_id}/copy", status_code=status.HTTP_200_OK)
async def copy_file_to_container(
    container_id: str,
    src_path: str,
    dest_path: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        DockerHelper.copy_file_to_container(client, container_id, src_path, dest_path)
        return {"message": "File copied successfully"}
    except Exception as e:
        raise e
    
@router.post("/docker/images/build", status_code=status.HTTP_201_CREATED)
async def build_image(
    dockerfile_path: str,
    image_name: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        DockerHelper.build_image(client, dockerfile_path, image_name)
        return {"message": "Image built successfully"}
    except Exception as e:
        raise e
    
@router.post("/docker/images/tag", status_code=status.HTTP_200_OK)
async def tag_image(
    image_id: str,
    new_tag: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        DockerHelper.tag_image(client, image_id, new_tag)
        return {"message": "Image tagged successfully"}
    except Exception as e:
        raise e
    
@router.post("/docker/images/push", status_code=status.HTTP_200_OK)
async def push_image(
    image_name: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        DockerHelper.push_image(client, image_name)
        return {"message": "Image pushed successfully"}
    except Exception as e:
        raise e

@router.post("/docker/images/pull", status_code=status.HTTP_200_OK)
async def pull_image(
    image_name: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        DockerHelper.pull_image(client, image_name)
        return {"message": "Image pulled successfully"}
    except Exception as e:
        raise e
    
@router.delete("/docker/images/{image_name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_image(
    image_name: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        DockerHelper.remove_image(client, image_name)
        return {"message": "Image removed successfully"}
    except Exception as e:
        raise e
    
@router.get("/docker/images", status_code=status.HTTP_200_OK)
async def list_images(
    client = Depends(DockerHelper.get_docker_client)):
    try:
        images = DockerHelper.list_images(client)
        return [{"image_id": image.id} for image in images]
    except Exception as e:
        raise e
    
@router.get("/docker/images/{image_name}", status_code=status.HTTP_200_OK)
async def get_image(
    image_name: str,
    client = Depends(DockerHelper.get_docker_client)):
    try:
        image = DockerHelper.get_image(client, image_name)
        return {"image_id": image.id}
    except Exception as e:
        raise e