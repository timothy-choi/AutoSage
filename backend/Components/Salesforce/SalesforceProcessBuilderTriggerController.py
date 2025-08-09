from flask import Blueprint, request, jsonify
from SalesforceProcessBuilderTriggerHelper import trigger_process_builder

salesforce_process_builder_trigger_bp = Blueprint("salesforce_process_builder_trigger", __name__)

@salesforce_process_builder_trigger_bp.route("/salesforce/process-builder/trigger", methods=["POST"])
def trigger_process_builder_controller():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_name = data.get("object_name")
    record_id = data.get("record_id")  
    fields = data.get("fields", {})

    if not instance_url or not access_token or not object_name or not fields:
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = trigger_process_builder(instance_url, access_token, object_name, record_id, fields)
    return jsonify(result), 200 if result.get("success") else 500