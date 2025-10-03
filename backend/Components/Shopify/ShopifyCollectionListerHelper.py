import requests

API_VERSION = "2025-07"

def list_custom_collections(shop_name: str, access_token: str, limit: int = 10, page_info: str = None, title: str = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/custom_collections.json"
    headers = {"X-Shopify-Access-Token": access_token}

    params = {"limit": limit}
    if page_info:
        params["page_info"] = page_info
    if title:
        params["title"] = title

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch custom collections: {response.text}")
    return response.json()


def list_smart_collections(shop_name: str, access_token: str, limit: int = 10, page_info: str = None, title: str = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/smart_collections.json"
    headers = {"X-Shopify-Access-Token": access_token}

    params = {"limit": limit}
    if page_info:
        params["page_info"] = page_info
    if title:
        params["title"] = title

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch smart collections: {response.text}")
    return response.json()


def search_collections_by_title(shop_name: str, access_token: str, title: str, smart: bool = False, limit: int = 10):
    if smart:
        return list_smart_collections(shop_name, access_token, limit=limit, title=title)
    return list_custom_collections(shop_name, access_token, limit=limit, title=title)