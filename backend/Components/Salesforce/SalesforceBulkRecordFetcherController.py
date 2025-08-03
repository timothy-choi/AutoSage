from flask import Blueprint, request, jsonify
from SalesforceBulkRecordFetcherHelper import fetch_salesforce_bulk_records, fetch_salesforce_next_records

salesforce_bulk_record_fetcher_bp = Blueprint("salesforce_bulk_record_fetcher", __name__)

@salesforce_bulk_record_fetcher_bp.route("/salesforce/records/bulk-fetch", methods=["POST"])
def fetch_bulk_records():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    fields = data.get("fields")
    where_clause = data.get("where_clause", "")
    limit = data.get("limit", 2000)

    if not all([instance_url, access_token, object_api_name, isinstance(fields, list)]):
        return jsonify({"success": False, "error": "Missing or invalid parameters."}), 400

    result = fetch_salesforce_bulk_records(instance_url, access_token, object_api_name, fields, where_clause, limit)
    return jsonify(result), 200 if result.get("success") else 500


@salesforce_bulk_record_fetcher_bp.route("/salesforce/records/bulk-fetch/next", methods=["POST"])
def fetch_next_records():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    next_url = data.get("next_url")

    if not all([instance_url, access_token, next_url]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = fetch_salesforce_next_records(instance_url, access_token, next_url)
    return jsonify(result), 200 if result.get("success") else 500