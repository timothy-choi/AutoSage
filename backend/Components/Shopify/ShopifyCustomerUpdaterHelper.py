import requests

API_VERSION = "2025-07"

def update_customer(shop_name: str, access_token: str, customer_id: str,
                    first_name: str = None, last_name: str = None,
                    email: str = None, phone: str = None,
                    tags: str = None, addresses: list = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/{API_VERSION}/customers/{customer_id}.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    customer_data = {"customer": {"id": customer_id}}

    if first_name:
        customer_data["customer"]["first_name"] = first_name
    if last_name:
        customer_data["customer"]["last_name"] = last_name
    if email:
        customer_data["customer"]["email"] = email
    if phone:
        customer_data["customer"]["phone"] = phone
    if tags:
        customer_data["customer"]["tags"] = tags
    if addresses:
        customer_data["customer"]["addresses"] = addresses

    response = requests.put(url, headers=headers, json=customer_data)
    if response.status_code != 200:
        raise Exception(f"Failed to update customer: {response.text}")
    return response.json()