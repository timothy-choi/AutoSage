from flask import Blueprint, request, jsonify
from SalesforceDeletedRecordRetrieverHelper import retrieve_deleted_salesforce_records

salesforce_deleted_record_retriever_bp = Blueprint("salesforce_deleted_record_retriever", __name__)

@salesforce_deleted_record_retriever_bp.route("/salesforce/records/deleted", methods=["POST"])
def get_deleted_salesforce_records():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not all([instance_url, access_token, object_api_name, start_time, end_time]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = retrieve_deleted_salesforce_records(instance_url, access_token, object_api_name, start_time, end_time)
    return jsonify(result), 200 if result.get("success") else 500