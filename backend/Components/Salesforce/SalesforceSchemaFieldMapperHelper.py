import requests

def get_salesforce_field_schema(instance_url: str, access_token: str, object_api_name: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/sobjects/{object_api_name}/describe"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        fields = response.json().get("fields", [])
        
        schema_map = {}
        for field in fields:
            schema_map[field["name"]] = {
                "label": field.get("label"),
                "type": field.get("type"),
                "required": field.get("nillable") is False,
                "picklistValues": [
                    val["value"] for val in field.get("picklistValues", []) if not val.get("inactive", False)
                ],
                "referenceTo": field.get("referenceTo"),
                "length": field.get("length"),
                "updateable": field.get("updateable"),
                "createable": field.get("createable")
            }

        return {"success": True, "fields": schema_map}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}