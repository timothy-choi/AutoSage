from flask import Blueprint, request, jsonify
from SalesforceRecordRestorerHelper import restore_salesforce_record

salesforce_record_restorer_bp = Blueprint("salesforce_record_restorer", __name__)

@salesforce_record_restorer_bp.route("/salesforce/record/restore", methods=["POST"])
def restore_record():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    record_data = data.get("record_data")

    if not all([instance_url, access_token, object_api_name, record_data]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = restore_salesforce_record(instance_url, access_token, object_api_name, record_data)
    return jsonify(result), 200 if result.get("success") else 500