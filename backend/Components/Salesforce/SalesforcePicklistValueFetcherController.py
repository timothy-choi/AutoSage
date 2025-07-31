from flask import Blueprint, request, jsonify
from SalesforcePicklistValueFetcherHelper import fetch_picklist_values

salesforce_picklist_value_fetcher_bp = Blueprint("salesforce_picklist_value_fetcher", __name__)

@salesforce_picklist_value_fetcher_bp.route("/salesforce/picklist-values", methods=["POST"])
def get_picklist_values():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    field_api_name = data.get("field_api_name")

    if not all([instance_url, access_token, object_api_name, field_api_name]):
        return jsonify({
            "success": False,
            "error": "All of instance_url, access_token, object_api_name, and field_api_name are required."
        }), 400

    result = fetch_picklist_values(instance_url, access_token, object_api_name, field_api_name)
    return jsonify(result), 200 if result.get("success") else result.get("status_code", 500)