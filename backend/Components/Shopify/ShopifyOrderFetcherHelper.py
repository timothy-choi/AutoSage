import requests

API_VERSION = "2025-07"

def fetch_orders(shop_name: str, access_token: str, status: str = "any", limit: int = 10, page_info: str = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/orders.json"
    headers = {"X-Shopify-Access-Token": access_token}

    params = {"limit": limit, "status": status}
    if page_info:
        params["page_info"] = page_info

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch orders: {response.text}")
    return response.json()


def fetch_order_by_id(shop_name: str, access_token: str, order_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch order {order_id}: {response.text}")
    return response.json()


def fetch_orders_by_customer(shop_name: str, access_token: str, customer_id: str, limit: int = 10):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/orders.json"
    headers = {"X-Shopify-Access-Token": access_token}
    params = {"customer_id": customer_id, "limit": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch orders for customer {customer_id}: {response.text}")
    return response.json()


def fetch_orders_by_date_range(shop_name: str, access_token: str, created_at_min: str, created_at_max: str, limit: int = 10):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/orders.json"
    headers = {"X-Shopify-Access-Token": access_token}
    params = {
        "created_at_min": created_at_min,
        "created_at_max": created_at_max,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch orders by date: {response.text}")
    return response.json()