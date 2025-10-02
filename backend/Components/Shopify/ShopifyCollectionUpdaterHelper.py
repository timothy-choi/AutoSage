import requests

API_VERSION = "2025-07"

def update_custom_collection(shop_name: str, access_token: str, collection_id: str,
                             title: str = None, body_html: str = None,
                             image_src: str = None, sort_order: str = None,
                             published: bool = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/custom_collections/{collection_id}.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    collection_data = {"custom_collection": {"id": collection_id}}

    if title:
        collection_data["custom_collection"]["title"] = title
    if body_html:
        collection_data["custom_collection"]["body_html"] = body_html
    if image_src:
        collection_data["custom_collection"]["image"] = {"src": image_src}
    if sort_order:
        collection_data["custom_collection"]["sort_order"] = sort_order
    if published is not None:
        collection_data["custom_collection"]["published"] = published

    response = requests.put(url, headers=headers, json=collection_data)
    if response.status_code != 200:
        raise Exception(f"Failed to update collection: {response.text}")
    return response.json()