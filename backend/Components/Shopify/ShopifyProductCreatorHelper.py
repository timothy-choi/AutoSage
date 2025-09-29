import requests

def create_product(shop_name: str, access_token: str, title: str, body_html: str = "", vendor: str = "", product_type: str = "", tags: list[str] = None, price: float = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/2025-07/products.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    product_data = {
        "product": {
            "title": title,
            "body_html": body_html,
            "vendor": vendor,
            "product_type": product_type
        }
    }

    if tags:
        product_data["product"]["tags"] = ",".join(tags)
    
    if price is not None:
        product_data["product"]["variants"] = [{"price": str(price)}]

    response = requests.post(url, headers=headers, json=product_data)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create product: {response.text}")
    return response.json()