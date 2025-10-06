import requests

API_VERSION = "2025-07"

def update_order(shop_name: str, access_token: str, order_id: str, updates: dict):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}.json"
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    payload = {"order": updates}

    response = requests.put(url, headers=headers, json=payload)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to update order {order_id}: {response.text}")
    return response.json()


def update_order_tags(shop_name: str, access_token: str, order_id: str, tags: str):
    return update_order(shop_name, access_token, order_id, {"id": order_id, "tags": tags})


def update_order_note(shop_name: str, access_token: str, order_id: str, note: str):
    return update_order(shop_name, access_token, order_id, {"id": order_id, "note": note})


def update_order_email(shop_name: str, access_token: str, order_id: str, email: str):
    return update_order(shop_name, access_token, order_id, {"id": order_id, "email": email})


def close_order(shop_name: str, access_token: str, order_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}/close.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to close order {order_id}: {response.text}")
    return response.json()


def reopen_order(shop_name: str, access_token: str, order_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}/open.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to reopen order {order_id}: {response.text}")
    return response.json()