import requests

API_VERSION = "2025-07"

def delete_custom_collection(shop_name: str, access_token: str, collection_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/custom_collections/{collection_id}.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to delete custom collection: {response.text}")
    return {"status": "success", "message": f"Custom collection {collection_id} deleted"}


def delete_smart_collection(shop_name: str, access_token: str, collection_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/smart_collections/{collection_id}.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to delete smart collection: {response.text}")
    return {"status": "success", "message": f"Smart collection {collection_id} deleted"}


def bulk_delete_custom_collections(shop_name: str, access_token: str, collection_ids: list):
    results = []
    for cid in collection_ids:
        try:
            results.append(delete_custom_collection(shop_name, access_token, cid))
        except Exception as e:
            results.append({"status": "error", "collection_id": cid, "error": str(e)})
    return results


def bulk_delete_smart_collections(shop_name: str, access_token: str, collection_ids: list):
    results = []
    for cid in collection_ids:
        try:
            results.append(delete_smart_collection(shop_name, access_token, cid))
        except Exception as e:
            results.append({"status": "error", "collection_id": cid, "error": str(e)})
    return results