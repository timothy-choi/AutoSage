import requests

def update_product(shop_name: str, access_token: str, product_id: str, title: str = None, body_html: str = None, vendor: str = None, product_type: str = None, tags: list[str] = None, price: float = None):
    url = f"https://{shop_name}.myshopify.com/admin/api/2025-07/products/{product_id}.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    product_data = {"product": {"id": product_id}}

    if title is not None:
        product_data["product"]["title"] = title
    if body_html is not None:
        product_data["product"]["body_html"] = body_html
    if vendor is not None:
        product_data["product"]["vendor"] = vendor
    if product_type is not None:
        product_data["product"]["product_type"] = product_type
    if tags is not None:
        product_data["product"]["tags"] = ",".join(tags)
    if price is not None:
        product_data["product"]["variants"] = [{"price": str(price)}]

    response = requests.put(url, headers=headers, json=product_data)
    if response.status_code != 200:
        raise Exception(f"Failed to update product: {response.text}")
    return response.json()