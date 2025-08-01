from flask import Blueprint, request, jsonify
from SalesforceRecordCreatorHelper import create_salesforce_record

salesforce_record_creator_bp = Blueprint("salesforce_record_creator", __name__)

@salesforce_record_creator_bp.route("/salesforce/record/create", methods=["POST"])
def create_record():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    record_data = data.get("record_data")

    if not all([instance_url, access_token, object_api_name, record_data]):
        return jsonify({
            "success": False,
            "error": "Missing required fields: instance_url, access_token, object_api_name, and record_data."
        }), 400

    result = create_salesforce_record(instance_url, access_token, object_api_name, record_data)
    return jsonify(result), 201 if result.get("success") else result.get("status_code", 500)