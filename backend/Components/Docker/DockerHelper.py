import docker

def get_docker_client():
    return docker.from_env()

def create_container(client, image_name: str, uid: str, mount_path: str):
    container = client.containers.create(
        image=image_name,
        name=f"function_{uid}",
        command=None,  
        volumes={mount_path: {"bind": "/app", "mode": "rw"}},
        working_dir="/app",
        network_mode="none",
        mem_limit="256m",
        cpu_period=100000,
        cpu_quota=50000,  
        detach=True
    )

    return container

def delete_container(client, container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove(force=True)

def start_container(client, container_id):
    container = client.containers.get(container_id)
    container.start()
    return container

def run_container(client, image, mount_path):
    return client.containers.run(
        image=image,
        volumes={mount_path: {"bind": "/app", "mode": "rw"}},
        working_dir="/app",
        detach=True,
        remove=True
    )

def stop_container(client, container_id):
    container = client.containers.get(container_id)
    container.stop()
    return container

def get_container(client, container_id):
    container = client.containers.get(container_id)
    return container

def list_containers(client):
    containers = client.containers.list(all=True)
    return containers

def get_container_status(client, container_id):
    container = client.containers.get(container_id)
    return container.status

def run_in_container(container, command: str):
    exec_result = container.exec_run(cmd=command, stdout=True, stderr=True)
    return {
        "exit_code": exec_result.exit_code,
        "output": exec_result.output.decode("utf-8").strip()
    }

def container_exists(client, container_id):
        return client.containers.get(container_id) is not None

def get_container_logs(client, container_id):
    container = client.containers.get(container_id)
    return container.logs().decode("utf-8").strip()

def copy_file_to_container(client, container_id, src_path, dest_path):
    container = client.containers.get(container_id)
    with open(src_path, 'rb') as f:
        container.put_archive(dest_path, f.read())

def build_image(client, dockerfile_path, image_name):
    client.images.build(path=dockerfile_path, tag=image_name)
    
def tag_image(client, image_id, new_tag):
    client.images.get(image_id).tag(new_tag)

def push_image(client, image_name):
    client.images.push(image_name)

def pull_image(client, image_name):
    client.images.pull(image_name)

def remove_image(client, image_name):
    client.images.remove(image_name, force=True)

def list_images(client):
    images = client.images.list()
    return images

def get_image(client, image_name):
    image = client.images.get(image_name)
    return image