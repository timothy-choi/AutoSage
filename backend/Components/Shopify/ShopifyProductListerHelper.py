import requests

API_VERSION = "2025-07"

def list_products(shop_name: str, access_token: str, limit: int = 10, page_info: str = None, collection_id: str = None, vendor: str = None, title: str = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products.json"
    headers = {"X-Shopify-Access-Token": access_token}

    params = {"limit": limit}
    if page_info:
        params["page_info"] = page_info
    if collection_id:
        params["collection_id"] = collection_id
    if vendor:
        params["vendor"] = vendor
    if title:
        params["title"] = title

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch products: {response.text}")

    return response.json()


def list_products_in_collection(shop_name: str, access_token: str, collection_id: str, limit: int = 10):
    return list_products(shop_name, access_token, limit=limit, collection_id=collection_id)


def list_products_by_vendor(shop_name: str, access_token: str, vendor: str, limit: int = 10):
    return list_products(shop_name, access_token, limit=limit, vendor=vendor)


def search_products_by_title(shop_name: str, access_token: str, title: str, limit: int = 10):
    return list_products(shop_name, access_token, limit=limit, title=title)