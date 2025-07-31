from flask import Blueprint, request, jsonify
from SalesforceAPIVersionFetcherHelper import fetch_salesforce_api_versions

salesforce_api_version_fetcher_bp = Blueprint("salesforce_api_version_fetcher", __name__)

@salesforce_api_version_fetcher_bp.route("/salesforce/api-versions", methods=["POST"])
def get_api_versions():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")

    if not instance_url or not access_token:
        return jsonify({
            "success": False,
            "error": "Both instance_url and access_token are required"
        }), 400

    result = fetch_salesforce_api_versions(instance_url, access_token)
    return jsonify(result), 200 if result["success"] else 401