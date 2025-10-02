import requests

API_VERSION = "2025-07"

def create_custom_collection(shop_name: str, access_token: str, title: str, body_html: str = None, image_src: str = None, sort_order: str = "best-selling", published: bool = True):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/custom_collections.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    collection_data = {
        "custom_collection": {
            "title": title,
            "sort_order": sort_order,
            "published": published
        }
    }

    if body_html:
        collection_data["custom_collection"]["body_html"] = body_html
    if image_src:
        collection_data["custom_collection"]["image"] = {"src": image_src}

    response = requests.post(url, headers=headers, json=collection_data)
    if response.status_code != 201:
        raise Exception(f"Failed to create collection: {response.text}")
    return response.json()