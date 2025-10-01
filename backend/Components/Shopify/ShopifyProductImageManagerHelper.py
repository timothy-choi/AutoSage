import requests

API_VERSION = "2025-07"

def add_image(shop_name: str, access_token: str, product_id: str, image_src: str = None, alt: str = None, position: int = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}/images.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    image_data = {"image": {}}
    if image_src:
        image_data["image"]["src"] = image_src
    if alt:
        image_data["image"]["alt"] = alt
    if position:
        image_data["image"]["position"] = position

    response = requests.post(url, headers=headers, json=image_data)
    if response.status_code != 201:
        raise Exception(f"Failed to add image: {response.text}")
    return response.json()


def update_image(shop_name: str, access_token: str, product_id: str, image_id: str, alt: str = None, position: int = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}/images/{image_id}.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    image_data = {"image": {"id": image_id}}
    if alt:
        image_data["image"]["alt"] = alt
    if position:
        image_data["image"]["position"] = position

    response = requests.put(url, headers=headers, json=image_data)
    if response.status_code != 200:
        raise Exception(f"Failed to update image: {response.text}")
    return response.json()


def delete_image(shop_name: str, access_token: str, product_id: str, image_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}/images/{image_id}.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to delete image: {response.text}")
    return {"status": "success", "message": "Image deleted successfully"}


def list_images(shop_name: str, access_token: str, product_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}/images.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to list images: {response.text}")
    return response.json()