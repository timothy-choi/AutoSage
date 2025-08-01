from flask import Blueprint, request, jsonify
from SalesforceRecordUpdaterHelper import update_salesforce_record

salesforce_record_updater_bp = Blueprint("salesforce_record_updater", __name__)

@salesforce_record_updater_bp.route("/salesforce/record/update", methods=["POST"])
def update_record():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    record_id = data.get("record_id")
    update_data = data.get("update_data")

    if not all([instance_url, access_token, object_api_name, record_id, update_data]):
        return jsonify({
            "success": False,
            "error": "Missing required fields: instance_url, access_token, object_api_name, record_id, and update_data."
        }), 400

    result = update_salesforce_record(instance_url, access_token, object_api_name, record_id, update_data)
    return jsonify(result), 200 if result.get("success") else result.get("status_code", 500)