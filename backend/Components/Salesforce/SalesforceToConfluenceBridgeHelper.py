import requests

def fetch_salesforce_records(instance_url, access_token, object_type, fields, limit=50):
    soql_query = f"SELECT {', '.join(fields)} FROM {object_type} LIMIT {limit}"
    url = f"{instance_url}/services/data/v60.0/query?q={soql_query}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Salesforce query failed: {response.text}")

    return response.json().get("records", [])

def format_records_as_confluence_table(records, fields):
    header_row = "".join(f"<th>{field}</th>" for field in fields)
    data_rows = ""

    for record in records:
        row = "".join(f"<td>{record.get(field, '')}</td>" for field in fields)
        data_rows += f"<tr>{row}</tr>"

    table_html = f"""
    <table>
        <thead><tr>{header_row}</tr></thead>
        <tbody>{data_rows}</tbody>
    </table>
    """
    return table_html.strip()

def update_confluence_page(base_url, auth, page_id, title, html_content):
    url = f"{base_url}/wiki/api/v2/pages/{page_id}"
    headers = {"Authorization": f"Basic {auth}", "Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch Confluence page info: {response.text}")

    page_info = response.json()
    version = page_info["version"]["number"] + 1
    space_key = page_info["space"]["key"]

    update_url = f"{base_url}/wiki/api/v2/pages/{page_id}"
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "spaceId": page_info["spaceId"],
        "status": "current",
        "version": {"number": version},
        "body": {
            "storage": {
                "value": html_content,
                "representation": "storage"
            }
        }
    }

    update_headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    update_response = requests.put(update_url, headers=update_headers, json=payload)
    if update_response.status_code not in [200, 202]:
        raise Exception(f"Failed to update Confluence page: {update_response.text}")

    return update_response.json()