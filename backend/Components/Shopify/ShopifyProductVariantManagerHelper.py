import requests

def add_variant(shop_name: str, access_token: str, product_id: str, option1: str, price: float, sku: str = None, inventory_quantity: int = 0):
    url = f"https://{shop_name}.myshopify.com/admin/api/2025-07/products/{product_id}/variants.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    variant_data = {
        "variant": {
            "option1": option1,
            "price": str(price),
            "sku": sku,
            "inventory_quantity": inventory_quantity
        }
    }

    response = requests.post(url, headers=headers, json=variant_data)
    if response.status_code != 201:
        raise Exception(f"Failed to add variant: {response.text}")
    return response.json()


def update_variant(shop_name: str, access_token: str, variant_id: str, option1: str = None, price: float = None, sku: str = None, inventory_quantity: int = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/2025-07/variants/{variant_id}.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    variant_data = {"variant": {"id": variant_id}}

    if option1 is not None:
        variant_data["variant"]["option1"] = option1
    if price is not None:
        variant_data["variant"]["price"] = str(price)
    if sku is not None:
        variant_data["variant"]["sku"] = sku
    if inventory_quantity is not None:
        variant_data["variant"]["inventory_quantity"] = inventory_quantity

    response = requests.put(url, headers=headers, json=variant_data)
    if response.status_code != 200:
        raise Exception(f"Failed to update variant: {response.text}")
    return response.json()


def delete_variant(shop_name: str, access_token: str, product_id: str, variant_id: str):
    url = f"https://{shop_name}.myshopify.com/admin/api/2025-07/products/{product_id}/variants/{variant_id}.json"
    headers = {"X-Shopify-Access-Token": access_token}

    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to delete variant: {response.text}")
    return {"status": "success", "message": "Variant deleted successfully"}