from flask import Blueprint, request, jsonify
from SalesforceRecordFetcherHelper import fetch_salesforce_records

salesforce_record_fetcher_bp = Blueprint("salesforce_record_fetcher", __name__)

@salesforce_record_fetcher_bp.route("/salesforce/records", methods=["POST"])
def get_salesforce_records():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    soql_query = data.get("soql_query")

    if not instance_url or not access_token or not soql_query:
        return jsonify({
            "success": False,
            "error": "instance_url, access_token, and soql_query are required."
        }), 400

    result = fetch_salesforce_records(instance_url, access_token, soql_query)
    return jsonify(result), 200 if result["success"] else result.get("status_code", 500)