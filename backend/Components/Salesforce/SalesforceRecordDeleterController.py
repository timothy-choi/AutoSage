from flask import Blueprint, request, jsonify
from SalesforceRecordDeleterHelper import delete_salesforce_record

salesforce_record_deleter_bp = Blueprint("salesforce_record_deleter", __name__)

@salesforce_record_deleter_bp.route("/salesforce/record/delete", methods=["POST"])
def delete_record():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    record_id = data.get("record_id")

    if not all([instance_url, access_token, object_api_name, record_id]):
        return jsonify({
            "success": False,
            "error": "Missing required fields: instance_url, access_token, object_api_name, and record_id."
        }), 400

    result = delete_salesforce_record(instance_url, access_token, object_api_name, record_id)
    return jsonify(result), 200 if result.get("success") else result.get("status_code", 500)