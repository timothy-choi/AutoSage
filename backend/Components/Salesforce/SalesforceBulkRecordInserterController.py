from flask import Blueprint, request, jsonify
from SalesforceBulkRecordInserterHelper import bulk_insert_salesforce_records

salesforce_bulk_record_inserter_bp = Blueprint("salesforce_bulk_record_inserter", __name__)

@salesforce_bulk_record_inserter_bp.route("/salesforce/records/bulk-insert", methods=["POST"])
def bulk_insert_records():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    records = data.get("records")

    if not all([instance_url, access_token, object_api_name, isinstance(records, list)]):
        return jsonify({
            "success": False,
            "error": "Missing or invalid fields: instance_url, access_token, object_api_name, and records."
        }), 400

    result = bulk_insert_salesforce_records(instance_url, access_token, object_api_name, records)
    return jsonify(result), 200 if result.get("success") else result.get("status_code", 500)