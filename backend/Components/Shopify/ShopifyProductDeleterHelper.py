import requests
from datetime import datetime, timedelta

API_VERSION = "2025-07"

def delete_product(shop_name: str, access_token: str, product_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to delete product: {response.text}")
    return {"status": "success", "message": f"Product {product_id} deleted successfully"}


def bulk_delete_products(shop_name: str, access_token: str, product_ids: list):
    results = []
    for pid in product_ids:
        try:
            result = delete_product(shop_name, access_token, pid)
            results.append(result)
        except Exception as e:
            results.append({"status": "error", "product_id": pid, "error": str(e)})
    return results


def delete_products_by_tag(shop_name: str, access_token: str, tag: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products.json?tag={tag}"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch products: {response.text}")

    products = response.json().get("products", [])
    product_ids = [p["id"] for p in products]

    return bulk_delete_products(shop_name, access_token, product_ids)


def delete_products_older_than(shop_name: str, access_token: str, days: int):
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch products: {response.text}")

    products = response.json().get("products", [])
    old_products = [p["id"] for p in products if datetime.strptime(p["created_at"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None) < cutoff_date]

    return bulk_delete_products(shop_name, access_token, old_products)


def soft_delete_product(shop_name: str, access_token: str, product_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    data = {"product": {"id": product_id, "status": "draft"}}
    response = requests.put(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to soft delete product: {response.text}")
    return {"status": "success", "message": f"Product {product_id} unpublished (soft deleted)"}